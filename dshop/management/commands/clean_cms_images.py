import sys
from django.core.management.base import BaseCommand

from dshop.models import dmBlocTextMedia
from dshop.models import dmBlocTextCarrouselImage
from dshop.models import dmBlocSliderChild
from dshop.models import dmInfolettre
from dshop.models import dmBlocEtapesChild
from dshop.models import dmBlockSalesChild
from dshop.models import dmBlockCalltoaction
from dshop.models import dmTestimonialParent
from dshop.models import dmTestimonialChild


class Command(BaseCommand):
    def handle(self, **options): # noqa
        try:
            dmBlocTextMedia.objects.all().delete()
            dmBlocTextCarrouselImage.objects.all().delete()
            dmBlocSliderChild.objects.all().delete()
            dmInfolettre.objects.all().delete()
            dmBlocEtapesChild.objects.all().delete()
            dmBlockSalesChild.objects.all().delete()
            dmBlockCalltoaction.objects.all().delete()
            dmTestimonialParent.objects.all().delete()
            dmTestimonialChild.objects.all().delete()
        except Exception as e:
            print("Error")
            print(e)
