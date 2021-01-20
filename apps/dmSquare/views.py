import json
from django.http import HttpResponse

def inventory_update(request):

    print(request.body)
    return HttpResponse('Ok')
