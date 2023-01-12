import django_rq
from django.db import models

from JrachkaTop.ticket_service_api.tasks import task_convert_order_to_pdf


class Printer(models.Model):
    class CheckType(models.TextChoices):
        KITCHEN = "Kitchen", "kitchen"
        CLIENT = "Client", "client"

    name = models.CharField(max_length=128)
    api_key = models.CharField(max_length=128, unique=True)
    check_type = models.CharField(
        max_length=64, choices=CheckType.choices, default=CheckType.KITCHEN
    )
    point_id = models.IntegerField(help_text="Related shop id")

    def __str__(self):
        return self.name


class Check(models.Model):
    class CheckType(models.TextChoices):
        KITCHEN = "Kitchen", "kitchen"
        CLIENT = "Client", "client"

    class CheckStatus(models.TextChoices):
        NEW = "New", "new"
        RENDERED = "Rendered", "rendered"
        PRINTED = "Printed", "printed"

    printer_id = models.ForeignKey(
        Printer, on_delete=models.PROTECT, blank=True, null=True
    )
    type = models.CharField(
        max_length=64, choices=CheckType.choices, default=CheckType.KITCHEN
    )
    order = models.JSONField()
    status = models.CharField(
        max_length=64, choices=CheckStatus.choices, default=CheckStatus.NEW
    )
    pdf_file = models.FileField(upload_to="media/pdf", blank=True, null=True)

    def __str__(self):
        return self.status

    def save(self, *args, **kwargs):
        creating = True if not self.pk else False
        super().save(*args, **kwargs)
        if creating:
            django_rq.enqueue(task_convert_order_to_pdf, data=self.order, check=self)

    def change_check_status(self, new_status: str):
        self.status = new_status
        self.save()
