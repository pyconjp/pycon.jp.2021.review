from rest_framework import serializers
from review.models import Proposal


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        exclude = ["created_at", "updated_at"]


class ProposalReviewScoreSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField()
    average_review_score = serializers.FloatField()
    no_count = serializers.IntegerField()

    class Meta:
        model = Proposal
        fields = [
            "sessionize_id",
            "title",
            "track",
            "audience_python_level",
            "speaking_language",
            "submit_user_id",
            "review_count",
            "average_review_score",
            "no_count",
        ]
