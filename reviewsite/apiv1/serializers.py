from rest_framework import serializers
from review.models import Proposal, Review


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


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.ReadOnlyField(source="reviewer.username")
    proposal_id = serializers.ReadOnlyField(source="proposal.sessionize_id")

    class Meta:
        model = Review
        fields = [
            "reviewer_name",
            "proposal_id",
            "score",
            "comment",
            "created_at",
            "updated_at",
        ]
