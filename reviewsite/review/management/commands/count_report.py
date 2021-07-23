from collections import Counter
import os

from django.core.management.base import BaseCommand
from django.db.models import Count
from postslack import post_slack

from review.models import Proposal


class Command(BaseCommand):
    help = (
        "Count proposals group by review count "
        "like 0 reviews: x, 1 review: y ..."
    )

    def handle(self, *args, **options):
        review_counts_dicts = Proposal.objects.annotate(
            rcount=Count("reviews")
        ).values("rcount")
        counter = Counter(
            [review_count["rcount"] for review_count in review_counts_dicts]
        )
        report_sentences = [
            f"{review_count}人がレビューしたプロポーザルは{proposal_count}件です"
            for review_count, proposal_count in sorted(counter.items())
        ]
        message = "\n".join(report_sentences)

        channel = os.environ.get("COUNT_REPORT_SLACK_CHANNEL")
        if channel:
            # 投稿先Slackチャンネルが環境変数で指定されている場合
            post_slack(channel, message)
        else:
            # 投稿先Slackチャンネルが未指定の場合はコマンドラインに出力
            self.stdout.write(self.style.SUCCESS(message))
