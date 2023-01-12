from django.urls import path

from JrachkaTop.ticket_service_api.views import (
    CheckAPIView,
    CreateCheckAPIView,
    NewChecksListAPIView,
)

urlpatterns = [
    path("create_checks/", CreateCheckAPIView.as_view()),
    path("new_checks/<str:printer_api>/", NewChecksListAPIView.as_view()),
    path("check/<int:id>/", CheckAPIView.as_view()),
]
