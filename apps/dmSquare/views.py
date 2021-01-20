import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def inventory_update(request):

    print(request.body)
    return HttpResponse('Ok')
