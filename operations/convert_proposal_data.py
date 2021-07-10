from argparse import ArgumentParser

import jsonlines
from openpyxl import load_workbook

SPEAKING_LANGUAGE_VALUE_MAP = {"Japanese": "ja", "English": "en"}
SLIDE_LANGUAGE_VALUE_MAP = {
    "Japanese only": "ja",
    "English only": "en",
    "Both": "bo",
}


class ValueSelector:
    def __init__(self, header_index_map):
        self.map = header_index_map

    def refer(self, row, key):
        index = self.map[key]
        return row[index].value


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input", help="Excel file downloaded from Sessionize")
    parser.add_argument("output", help="JSON lines file")
    args = parser.parse_args()

    workbook = load_workbook(args.input, read_only=True)
    worksheet = workbook["Sessions and speakers"]
    row_generator = worksheet.rows

    header = next(row_generator)
    header_index_map = {cell.value: index for index, cell in enumerate(header)}
    selector = ValueSelector(header_index_map)

    proposals = []
    for row in row_generator:
        if selector.refer(row, "Status") != "Nominated":
            continue
        proposal = {
            "sessionize_id": selector.refer(row, "Session Id"),
            "title": selector.refer(row, "Title"),
            "description": selector.refer(row, "Description"),
            "elevator_pitch": selector.refer(row, "Elevator Pitch"),
            "track": selector.refer(row, "Track"),
            "audience_python_level": selector.refer(row, "Level"),
            "audience_prior_knowledge": selector.refer(row, "オーディエンスに求める前提知識"),
            "audience_take_away": selector.refer(
                row, "オーディエンスが持って帰れる具体的な知識やノウハウ"
            ),
            "motivation_and_why": selector.refer(
                row, "この題材を話すのに自分がふさわしいと考える理由やこのトークをするモチベーション"
            ),
            "materials_url": selector.refer(
                row, "このトピックについて過去の登壇で使った資料やソースコードのURL"
            ),
            "speaking_language": SPEAKING_LANGUAGE_VALUE_MAP[
                selector.refer(row, "Language")
            ],
            "slide_language": SLIDE_LANGUAGE_VALUE_MAP[
                selector.refer(
                    row, "発表資料の言語 / Language of presentation material"
                )
            ],
            "reviewer_not_displayed_to": None,
            "submit_user_id": selector.refer(row, "Speaker Id"),
        }
        proposals.append(proposal)

    with jsonlines.open(args.output, mode="w") as writer:
        writer.write_all(proposals)
