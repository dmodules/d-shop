from django.conf.urls import url

from .views import AdminCountsView
from .views import AdminMonthlySalesView, AdminWeeklySalesView
from .views import AdminByLocationView
from .views import AdminBestsellersView, AdminStocksView
from .views import AdminLogsView

urlpatterns = [
    url(r'^counts/$', AdminCountsView.as_view()),
    url(r'^monthly-sales/$', AdminMonthlySalesView.as_view()),
    url(r'^weekly-sales/$', AdminWeeklySalesView.as_view()),
    url(r'^bylocation/$', AdminByLocationView.as_view()),
    url(r'^bestsellers/$', AdminBestsellersView.as_view()),
    url(r'^stocks/$', AdminStocksView.as_view()),
    url(r'^logs/$', AdminLogsView.as_view()),
]
