import json
import uuid
import pytz
from datetime import datetime
from dateutil.tz import tzlocal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from settings import SQUARE_TOKEN, SQUARE_ENVIRONMENT, SQUARE_LOCATION_ID
from square.client import Client
from dshop.models import ProductVariableVariant
from apps.dmSquare.models import dmStockLog

client = Client(
    access_token=SQUARE_TOKEN,
    environment=SQUARE_ENVIRONMENT,
)

@csrf_exempt
def inventory_update(request):    # noqa: C901

    data = request.body
    data = json.loads(data)
    print("In webhook call.")
    print(data)
    if 'data' not in data:
        return HttpResponse('ERROR')
    if 'object' not in data['data']:
        return HttpResponse('ERROR')
    if 'inventory_counts' not in data['data']['object']:
        return HttpResponse('ERROR')
    for actual_data in data['data']['object']['inventory_counts']:
        if actual_data['state'] == 'IN_STOCK':
            square_id = actual_data['catalog_object_id']
            quantity = actual_data['quantity']
            created_at = data['created_at'].split('.')[0]
            break

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
        print("Product to be updated: " + str(pvv))
        print("product quantity before: " + str(pvv.quantity))
        # Create Stock Log entry
        today = pytz.utc.localize(datetime.utcnow())
        try:
            data = {
                "product_name": pvv.product.product_name,
                "product_square_code": pvv.product.square_id,
                "variant_square_code": square_id,
                "old_quantity": pvv.quantity,
                "new_quantity": quantity,
                "stock_update_date": today,
                "update_from": 2
            }
            dmStockLog.objects.create(**data)
        except Exception as e:
            print("Webhook: Failed to create dmStockLog: " + str(e))
        if quantity < 0:
            quantity = 0
        pvv.quantity = quantity
        pvv.save()
        print("product quantity after: " + str(pvv.quantity))
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

    # Create Stock Log entry
    pvv = ProductVariableVariant.objects.filter(product_code=product_code)

    if pvv:
        pvv = pvv[0]
        today = pytz.utc.localize(datetime.utcnow())
        try:
            data = {
                "product_name": pvv.product.product_name,
                "product_square_code": pvv.product.square_id,
                "variant_square_code": product_code,
                "old_quantity": pvv.quantity + int(quantity),
                "new_quantity": pvv.quantity,
                "stock_update_date": today,
                "update_from": 1
            }
            dmStockLog.objects.create(**data)
        except Exception as e:
            print("Failed to create dmStockLog: " + str(e))
    else:
        print("Failed to create Stock log")

    if result.is_success():
        print(result.body)
    elif result.is_error():
        print(result.errors)

    return
