from argparse import ArgumentParser
from collections import defaultdict
from operator import itemgetter
from urllib.parse import urljoin

import gspread
import jsonlines

proposal_fields_getter = itemgetter(
    "title",
    "average_review_score",
    "review_count",
    "no_count",
    "speaking_language",
    "track",
    "audience_python_level",
)


def aggregate(proposals, app_url, exclude_set):
    # proposals: https://github.com/ftnext/pycon.jp.2021.review/issues/47
    # 入力されるproposalsはAPIが返した順を保持しつつ、投稿者でまとまるように加工する
    one_proposal_seen_submitter_uuid_set = set()  # type: set[str]
    multiple_submitter_uuid_set = set()  # type: set[str]
    each_max_score_proposals = []  # 投稿者ごとに最大スコアのプロポーザル
    rest_proposals = defaultdict(list)  # 投稿者ID: [最大ではないスコアのプロポーザル, ...]（スコア順）
    for p in proposals:
        if p["sessionize_id"] in exclude_set:
            continue
        if p["submit_user_id"] not in one_proposal_seen_submitter_uuid_set:
            each_max_score_proposals.append(p)
            one_proposal_seen_submitter_uuid_set.add(p["submit_user_id"])
            continue
        rest_proposals[p["submit_user_id"]].append(p)
        multiple_submitter_uuid_set.add(p["submit_user_id"])

    submitter_uuid_int_map = {
        uuid: i
        for i, uuid in enumerate(
            sorted(p["submit_user_id"] for p in each_max_score_proposals),
            start=1,
        )
    }
    # 69名から応募とあるが、サンプルプロポーザルが除けていなかったと思われる
    # https://pyconjp.blogspot.com/2021/07/pyconjp-2020-proposals-details.html
    assert len(each_max_score_proposals) == 68, len(each_max_score_proposals)

    for p in each_max_score_proposals:
        yield (
            submitter_uuid_int_map[p["submit_user_id"]],
            *proposal_fields_getter(p),
            urljoin(app_url, f"proposal/{p['sessionize_id']}"),
        )
        if p["submit_user_id"] in multiple_submitter_uuid_set:
            for rp in rest_proposals[p["submit_user_id"]]:
                yield submitter_uuid_int_map[
                    rp["submit_user_id"]
                ], *proposal_fields_getter(rp), urljoin(
                    app_url, f"proposal/{p['sessionize_id']}"
                )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "input", help="JSON lines file of review scores (sorted by scores)"
    )
    parser.add_argument("spreadsheet_id")
    parser.add_argument("worksheet_title")
    parser.add_argument("service_account_file")
    parser.add_argument("review_app_url")
    parser.add_argument("--exclude", type=int, nargs="*")
    args = parser.parse_args()

    with jsonlines.open(args.input) as reader:
        proposals = list(reader)

    headers = [
        "投稿者ID",
        "タイトル",
        "平均レビュースコア",
        "レビュー総数",
        "Noの数",
        "発表言語",
        "Track",
        "Python level",
        "レビューアプリURL",
    ]
    aggregated_proposals = aggregate(
        proposals,
        args.review_app_url,
        set(args.exclude) if args.exclude else set(),
    )
    rows = list(aggregated_proposals)
    # 応募85本 https://pyconjp.blogspot.com/2021/07/pyconjp-2020-proposals-details.html
    assert len(rows) == 85, len(rows)

    gspread_client = gspread.service_account(
        filename=args.service_account_file
    )
    spreadsheet = gspread_client.open_by_key(args.spreadsheet_id)

    worksheet = spreadsheet.add_worksheet(
        title=args.worksheet_title, rows="1", cols="1"
    )
    worksheet.update("A1", [headers] + rows)
