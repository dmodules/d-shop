from django.conf.urls import url

from .views import inventory_update

urlpatterns = [
    url(r'^inventory-update/', inventory_update),
]
