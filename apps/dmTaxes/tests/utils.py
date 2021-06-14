
from apps.dmTaxes.models import CanadaTaxManagement


def create_taxes(data=None):
    data = {
        'state': 'Quebec',
        'hst': 2.9,
        'gst': 8,
    }
    try:
        dt = CanadaTaxManagement.objects.create(**data)
    except Exception as e:
        return type(e)
    return dt
