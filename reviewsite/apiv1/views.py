from django.db.models import Avg, Count, Q, Value
from django.db.models.functions import Coalesce
from rest_framework import generics, status, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from review.models import Proposal, Review

from .serializers import (
    ProposalReviewScoreSerializer,
    ProposalSerializer,
    ReviewSerializer,
)


class ProposalCreateAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = ProposalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ProposalReviewScoreListAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        proposals = Proposal.objects.annotate(
            review_count=Count("reviews"),
            average_review_score=Coalesce(Avg("reviews__score"), Value(0.0)),
            no_count=Count(
                "reviews", filter=Q(reviews__score=Review.ReviewScore.NO)
            ),
        ).order_by(
            "-average_review_score",
            "-review_count",
            "no_count",
            "sessionize_id",
        )
        serializer = ProposalReviewScoreSerializer(
            instance=proposals, many=True
        )
        return Response(serializer.data, status.HTTP_200_OK)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100


class ReviewListAPIView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Review.objects.select_related("reviewer", "proposal").order_by(
        "pk"
    )
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination
