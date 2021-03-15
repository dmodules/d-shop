# from haystack.query import SearchQuerySet
import json
from django.conf import settings
from django.contrib import messages
from django.core.files import File as d_file
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from filer.fields.file import File

from .models import dmJobDescription, dmJobApplication
from .serializers import JobSerializer

class JobListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        jobs = dmJobDescription.objects.filter(is_active=True)
        job_data = []
        for job in jobs:
            data = {
                'id': job.id,
                'title': job.title,
                'slug': job.slug,
                'location': job.location,
                'description': job.description[0:200]
            }
            job_data.append(data)
        return render(request, 'job_list.html', {"data": job_data})


class JobDescView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        job = dmJobDescription.objects.filter(slug=kwargs['job_slug']).first()
        if job:
            return render(request, 'job_desc.html', {'data': job})
        return render(request, 'job_desc.html')

    def post(self, request, *args, **kwargs):
        cv = request.FILES.get('cv', None)
        job = dmJobDescription.objects.filter(slug=kwargs['job_slug']).first()
        if not cv:
            msg = "Veuillez télécharger le fichier CV"
            messages.error(request, msg)
            return render(request, 'job_desc.html', {'data': job})
        if job:
            doc = request.FILES['cv'].file.read()         # Uploaded File
            temp_file = NamedTemporaryFile(delete=True)   # Create Temp File
            temp_file.write(doc)                          # Write to temp file
            core_file = d_file(temp_file, 'rb')           # Create Django core file
            # Create filer File object
            cv_file = File.objects.create(file=core_file, name=request.FILES['cv'].name)
            data = {
                'name' : request.POST.get('name', None),
                'email' : request.POST.get('email', None),
                'phone' : request.POST.get('phone', None),
                'message' : request.POST.get('message', None),
                'document' : cv_file,
                'job' : job
            }
            dmJobApplication.objects.create(**data)
            msg = "Votre demande d'emploi pour le "+job.title+" a bien été enregistrée"
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
        return render(request, 'job_desc.html')



