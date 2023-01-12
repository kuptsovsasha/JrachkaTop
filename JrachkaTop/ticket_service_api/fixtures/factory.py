import factory.fuzzy
from factory.django import DjangoModelFactory

from JrachkaTop.ticket_service_api.models import Printer


class PrinterFactory(DjangoModelFactory):
    """Generate printer object with unique name and api key"""

    class Meta:
        model = Printer

    name = factory.Sequence(lambda n: "Printer #%s" % n)
    api_key = factory.Sequence(lambda n: "api_key#%s" % n)
