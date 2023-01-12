from django.contrib import admin

from .models import Check, Printer

# Register your models here.


class PrinterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "check_type",
        "point_id",
    )
    list_filter = (
        "check_type",
        "point_id",
    )


class CheckAdmin(admin.ModelAdmin):
    list_display = (
        "printer_id",
        "type",
        "status",
    )
    list_filter = ("type", "status", "printer_id")


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
