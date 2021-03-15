from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<job_slug>[\w-]+)$', views.JobDescView.as_view(), name="jobs_desc"),
    url(r'^', views.JobListView.as_view(), name="jobs"),
]

