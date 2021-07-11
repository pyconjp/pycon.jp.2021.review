from threading import Thread

from django.conf import settings
from postslack import post_slack


def post_review_log_slack_async(review, request):
    name = request.user.username
    log_message = (
        f"{name}さんが「{review.proposal.title}」を{review.score}と評価しました。\n"
        f"コメント：{review.comment}\n"
        f"{request.build_absolute_uri()}"
    )
    thread = Thread(
        target=post_slack,
        args=(settings.SLACK_LOG_POST_CHANNEL, log_message),
    )
    thread.start()
