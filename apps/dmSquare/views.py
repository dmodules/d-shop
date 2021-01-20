import json
import uuid
from datetime import datetime
from dateutil.tz import tzlocal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from settings import SQUARE_TOKEN, SQUARE_ENV
from square.client import Client
from dshop.models import ProductVariableVariant

client = Client(
    access_token=SQUARE_TOKEN,
    environment=SQUARE_ENV,
)

@csrf_exempt
def inventory_update(request):

    data = request.body
    data = json.loads(data)
    square_id = data['data']['object']['inventory_counts'][0]['catalog_object_id']
    quantity = data['data']['object']['inventory_counts'][0]['quantity']
    created_at = data['created_at'].split('.')[0]

    result = client.inventory.retrieve_inventory_changes(
        catalog_object_id="WXO4P6ZKCS2IYEUZC4S6NKHZ"
    )
    square_data = result.body
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
    idempotency_key = str(uuid.uuid1())
    product_code = str(product_code)
    quantity = str(quantity)
    occured_at = datetime.now(tzlocal()).isoformat()
    result = client.inventory.batch_change_inventory(
        body={
            "idempotency_key": idempotency_key,
            "changes": [
                {
                    "type": "ADJUSTMENT",
                    "adjustment": {
                        "from_state": "IN_STOCK",
                        "to_state": "SOLD",
                        "location_id": "LBH3XBZ3XNHEP",
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
