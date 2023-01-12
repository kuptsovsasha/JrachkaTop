import django_rq
from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.response import Response

from JrachkaTop.ticket_service_api.models import Check
from JrachkaTop.ticket_service_api.serializer import (
    CreateCheckSerializer,
    NewChecksListSerializer,
)


class CreateCheckAPIView(generics.CreateAPIView):
    """Create check object
    for both type printer if they exist"""

    queryset = Check.objects.all()
    serializer_class = CreateCheckSerializer


class NewChecksListAPIView(generics.ListAPIView):
    """Return list with checks which was not printed yet.
    Base of printer API key"""

    serializer_class = NewChecksListSerializer

    def get_queryset(self):
        api_key = self.kwargs["printer_api"]
        queryset = Check.objects.filter(
            printer_id__api_key=api_key, status=Check.CheckStatus.RENDERED
        )
        return queryset


class CheckAPIView(generics.GenericAPIView):
    """Return generated pdf file from requested check object."""

    queryset = Check.objects.all()
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        check = self.get_object()
        if not check:
            return Response(
                {"error": "Check didn't exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not check.pdf_file:
            return Response(
                {"error": "Pdf file not created for this check"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        check.change_check_status("Printed")
        return FileResponse(check.pdf_file.file)
