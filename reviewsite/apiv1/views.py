from rest_framework import status, views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import ProposalSerializer


class ProposalCreateAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = ProposalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
