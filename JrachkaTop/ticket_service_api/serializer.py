from typing import Tuple

from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from JrachkaTop.ticket_service_api.models import Check, Printer


class CreateCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ("order",)

    def validate(self, attrs):
        order = attrs.get("order")
        point_id = order.get("point_id")
        order_id = order.get("order_id")
        if not point_id or not order_id:
            raise ValidationError("point_id and order_id is required")

        printer_kitchen, printer_client = self.get_printers(point_id)
        if printer_kitchen is None and printer_client is None:
            raise ValidationError(
                {"printer_error": "this point didn't have any printer"}
            )
        is_order_exist = Check.objects.filter(order__order_id=order_id).exists()
        if is_order_exist:
            raise ValidationError(
                {"check_error": "check with this order_id already exist"}
            )

        printers = []
        if printer_kitchen:
            printers.append(printer_kitchen)
        if printer_client:
            printers.append(printer_client)

        attrs["printers"] = printers
        return attrs

    def create(self, validated_data):
        printers = validated_data.pop("printers")
        created_checks = []
        for printer in printers:
            check = Check.objects.create(
                order=validated_data.get("order"),
                type=printer.check_type,
                printer_id=printer,
            )
            created_checks.append(check)
        return created_checks[0]

    @staticmethod
    def get_printers(point: int) -> tuple[Printer, Printer]:
        printer_kitchen = Printer.objects.filter(
            Q(point_id=point) & Q(check_type=Check.CheckType.KITCHEN)
        ).first()
        printer_client = Printer.objects.filter(
            Q(point_id=point) & Q(check_type=Check.CheckType.CLIENT)
        ).first()
        return printer_kitchen, printer_client


class NewChecksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"
