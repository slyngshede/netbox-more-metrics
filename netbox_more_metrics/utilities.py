import decimal
import re
import sys

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


def enable_metrics():
    if hasattr(settings, "METRICS_ENABLED") and not settings.METRICS_ENABLED:
        return False

    # Enable metrics on the devserver
    if "runserver" in sys.argv:
        return True

    # Enable metrics if not running manage.py.
    regex = re.compile(r"(?:\.\/)?manage\.py", flags=re.IGNORECASE)
    if not any(filter(regex.match, sys.argv)):
        return True

    return False


class CustomFieldJSONEncoder(DjangoJSONEncoder):
    """
    Override Django's built-in JSON encoder to save decimal values as JSON numbers.
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)