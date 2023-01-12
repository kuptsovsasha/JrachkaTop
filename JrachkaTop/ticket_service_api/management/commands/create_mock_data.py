from django.core.management import BaseCommand

from JrachkaTop.ticket_service_api.fixtures.factory import PrinterFactory
from JrachkaTop.ticket_service_api.models import Printer


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--points", action="append", type=int)

    def handle(self, *args, **options):
        points = options["points"]

        for point in range(points[0]):
            for check_type in Printer.CheckType.choices:
                PrinterFactory(point_id=point, check_type=check_type[0])
