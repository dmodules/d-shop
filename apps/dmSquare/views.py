import json
import uuid
from datetime import datetime
from dateutil.tz import tzlocal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from settings import SQUARE_TOKEN, SQUARE_ENVIRONMENT, SQUARE_LOCATION_ID
from square.client import Client
from dshop.models import ProductVariableVariant

client = Client(
    access_token=SQUARE_TOKEN,
    environment=SQUARE_ENVIRONMENT,
)

@csrf_exempt
def inventory_update(request):

    data = request.body
    data = json.loads(data)
    if 'data' not in data:
        return HttpResponse('ERROR')
    if 'object' not in data['data']:
        return HttpResponse('ERROR')
    if 'inventory_counts' not in data['data']['object']:
        return HttpResponse('ERROR')
    square_id = data['data']['object']['inventory_counts'][0]['catalog_object_id']
    quantity = data['data']['object']['inventory_counts'][0]['quantity']
    created_at = data['created_at'].split('.')[0]

    result = client.inventory.retrieve_inventory_changes(
        catalog_object_id=square_id
    )
    square_data = result.body
    if 'changes' in square_data:
        for change in square_data['changes']:
            if 'adjustment' in change:
                if 'source' in change['adjustment']:
                    inventory_updated = change['adjustment']['created_at'].split('.')[0]
                    if inventory_updated == created_at:
                        print("Stock updated by D-shop API so ignore this webhook.")
                        return HttpResponse('Ok')

    # Update Stock
    pvv = ProductVariableVariant.objects.filter(product_code=square_id)
    if pvv:
        pvv = pvv[0]
        pvv.stock = quantity
        pvv.save()
        print("Stock updated")
    return HttpResponse('Ok')

def square_update_stock(quantity, product_code):
    print("Update quantity in square..")
    idempotency_key = str(uuid.uuid1())
    product_code = str(product_code)
    quantity = str(quantity)
    occured_at = datetime.now(tzlocal()).isoformat()
    print(product_code, quantity, occured_at, idempotency_key)
    result = client.inventory.batch_change_inventory(
        body={
            "idempotency_key": idempotency_key,
            "changes": [
                {
                    "type": "ADJUSTMENT",
                    "adjustment": {
                        "from_state": "IN_STOCK",
                        "to_state": "SOLD",
                        "location_id": SQUARE_LOCATION_ID,
                        "catalog_object_id": product_code,
                        "quantity": quantity,
                        "occurred_at": occured_at
                    }
                }]
        }
    )

    if result.is_success():
        print(result.body)
    elif result.is_error():
        print(result.errors)

    return
