from django.db.models import Avg, Count, Q, Value
from django.db.models.functions import Coalesce
from rest_framework import status, views
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


class ReviewListAPIView(views.APIView):
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination

    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            self._paginator = self.pagination_class()
        return self._paginator

    def get(self, request, *args, **kwargs):
        reviews = Review.objects.select_related(
            "reviewer", "proposal"
        ).order_by("pk")
        page = self.paginator.paginate_queryset(reviews, request, view=self)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
