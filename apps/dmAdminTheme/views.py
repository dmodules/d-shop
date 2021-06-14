from datetime import datetime, timedelta

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response as RestResponse

from shop.models.defaults.order import Order
from dshop.models import OrderItem
from shop.money import Money

from dshop.models import Customer
from dshop.models import \
    Product, \
    ProductDefault, \
    ProductVariable, \
    ProductVariableVariant

from .models import dmAdminLogs


months = [
    _("Months"),
    _("January"),
    _("February"),
    _("March"),
    _("April"),
    _("May"),
    _("June"),
    _("July"),
    _("August"),
    _("September"),
    _("October"),
    _("November"),
    _("December")
]


class AdminCountsView(APIView):
    """
    Get statistics counts data for admin panel
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or\
           not request.user.is_active or not request.user.is_staff:
            return RestResponse({"valid": False})
        # ==========================================================---
        f = timezone.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        thismonth = 0
        lastmonth = 0
        # ===---
        s = f
        if s.month+1 > 12:
            e = s.replace(month=s.month+1 - 12).replace(year=s.year+1)
        else:
            e = s.replace(month=s.month+1)
        thismonth = Customer.objects.filter(
            recognized=2,
            date_joined__gte=s,
            date_joined__lt=e
        ).count()
        # ===---
        s = f.replace(month=12 + f.month-1 if f.month-1 < 1 else f.month-1)
        if s.month+1 > 12:
            e = s.replace(month=s.month+1 - 12).replace(year=s.year+1)
        else:
            e = s.replace(month=s.month+1)
        lastmonth = Customer.objects.filter(
            recognized=2,
            date_joined__gte=s,
            date_joined__lt=e
        ).count()
        # ===---
        division = lastmonth if lastmonth > 0 else 1
        percent = ((thismonth - lastmonth) * 100) / division
        data_customers = {
            "thismonth": thismonth,
            "lastmonth": lastmonth,
            "percent": round(percent)
        }
        # ==========================================================---
        thismonth = 0
        lastmonth = 0
        # ===---
        s = f
        if s.month+1 > 12:
            e = s.replace(month=s.month+1 - 12).replace(year=s.year+1)
        else:
            e = s.replace(month=s.month+1)
        thismonth = Order.objects.filter(
            created_at__gte=s,
            created_at__lt=e
        ).count()
        # ===---
        s = f.replace(month=12 + f.month-1 if f.month-1 < 1 else f.month-1)
        if s.month+1 > 12:
            e = s.replace(month=s.month+1 - 12).replace(year=s.year+1)
        else:
            e = s.replace(month=s.month+1)
        lastmonth = Order.objects.filter(
            created_at__gte=s,
            created_at__lt=e
        ).count()
        # ===---
        division = lastmonth if lastmonth > 0 else 1
        percent = ((thismonth - lastmonth) * 100) / division
        data_orders = {
            "thismonth": thismonth,
            "lastmonth": lastmonth,
            "percent": round(percent)
        }
        # ==========================================================---
        thismonth = 0
        lastmonth = 0
        # ===---
        s = f
        if s.month+1 > 12:
            e = s.replace(month=s.month+1 - 12).replace(year=s.year+1)
        else:
            e = s.replace(month=s.month+1)
        thismonth_orders = Order.objects.filter(
            created_at__gte=s,
            created_at__lt=e
        )
        for o in thismonth_orders:
            thismonth += o.total
        # ===---
        s = f.replace(month=12 + f.month-1 if f.month-1 < 1 else f.month-1)
        if s.month+1 > 12:
            e = s.replace(month=s.month+1 - 12).replace(year=s.year+1)
        else:
            e = s.replace(month=s.month+1)
        lastmonth_orders = Order.objects.filter(
            created_at__gte=s,
            created_at__lt=e
        )
        for o in lastmonth_orders:
            lastmonth += o.total
        # ===---
        thismonth = float(thismonth)
        lastmonth = float(lastmonth)
        division = lastmonth if lastmonth > 0 else 1
        percent = ((thismonth - lastmonth) * 100) / division
        data_incomes = {
            "thismonth": Money(thismonth),
            "lastmonth": Money(lastmonth),
            "percent": round(percent)
        }
        # ==========================================================---
        data_awaitings = Order.objects.filter(
            status="payment_confirmed"
        ).count()
        # ==========================================================---
        return RestResponse({
            "customers": data_customers,
            "orders": data_orders,
            "incomes": data_incomes,
            "awaitings": data_awaitings,
            "valid": True
        })


class AdminMonthlySalesView(APIView):
    """
    Get incomes data per month for admin panel
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or\
           not request.user.is_active or not request.user.is_staff:
            return RestResponse({"valid": False})
        # ==========================================================---
        f = timezone.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        # ===---
        data_monthlysales = {
            "labels": [],
            "datasets": [
                {
                    "label": _("Current Year"),
                    "data": [],
                    "backgroundColor": "#066bf9",
                    "barPercentage": 0.25
                },
                {
                    "label": _("Last Year"),
                    "data": [],
                    "backgroundColor": "#ccc",
                    "barPercentage": 0.25
                }
            ]
        }
        # ===---
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
            s = f.replace(month=i)
            if s.month+1 > 12:
                e = s.replace(month=s.month+1 - 12).replace(year=s.year+1)
            else:
                e = s.replace(month=s.month+1)
            thisyear_month = Order.objects.filter(
                created_at__gte=s,
                created_at__lt=e
            )
            thisyear_incomes = 0
            for o in thisyear_month:
                thisyear_incomes += o.total
            # ===---
            s = f.replace(month=i).replace(year=s.year-1)
            if s.month+1 > 12:
                e = s.replace(month=s.month+1 - 12).replace(year=s.year+1)
            else:
                e = s.replace(month=s.month+1)
            lastyear_month = Order.objects.filter(
                created_at__gte=s,
                created_at__lt=e
            )
            lastyear_incomes = 0
            for o in lastyear_month:
                lastyear_incomes += o.total
            # ===---
            data_monthlysales["labels"].append(months[s.month])
            data_monthlysales["datasets"][0]["data"].append(
                float(thisyear_incomes)
            )
            data_monthlysales["datasets"][1]["data"].append(
                float(lastyear_incomes)
            )
        # ==========================================================---
        return RestResponse({
            "monthlysales": data_monthlysales,
            "valid": True
        })


class AdminWeeklySalesView(APIView):
    """
    Get incomes data per day for admin panel
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or\
           not request.user.is_active or not request.user.is_staff:
            return RestResponse({"valid": False})
        # ==========================================================---
        f = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # ===---
        data_weeklysales = {
            "labels": [
                _("Monday"),
                _("Tuesday"),
                _("Wednesday"),
                _("Thursday"),
                _("Friday"),
                _("Saturday"),
                _("Sunday")
            ],
            "datasets": [
                {
                    "label": _("Current Week Incomes"),
                    "data": [],
                    "borderColor": "#066bf9",
                    "backgroundColor": "#066bf9",
                    "fill": False
                },
                {
                    "label": _("Last Week Incomes"),
                    "data": [],
                    "borderColor": "#ccc",
                    "backgroundColor": "#ccc",
                    "fill": False
                }
            ]
        }
        # ===---
        f = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        f = f - timedelta(f.weekday())
        for i in [0, 1, 2, 3, 4, 5, 6]:
            s = f + timedelta(i)
            thisweek_day = Order.objects.filter(
                created_at__gte=s,
                created_at__lt=s + timedelta(1)
            )
            thisweek_incomes = 0
            for o in thisweek_day:
                thisweek_incomes += o.total
            data_weeklysales["datasets"][0]["data"].append(
                float(thisweek_incomes)
            )
        # ===---
        f = f - timedelta(f.weekday()) - timedelta(7)
        for i in [0, 1, 2, 3, 4, 5, 6]:
            s = f + timedelta(i)
            lastweek_day = Order.objects.filter(
                created_at__gte=s,
                created_at__lt=s + timedelta(1)
            )
            lastweek_incomes = 0
            for o in lastweek_day:
                lastweek_incomes += o.total
            data_weeklysales["datasets"][1]["data"].append(
                float(lastweek_incomes)
            )
        # ==========================================================---
        return RestResponse({
            "weeklysales": data_weeklysales,
            "valid": True
        })


class AdminByLocationView(APIView):
    """
    Get by location data for admin panel
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or\
           not request.user.is_active or not request.user.is_staff:
            return RestResponse({"valid": False})
        # ==========================================================---
        bylocation = []
        # ==========================================================---
        return RestResponse({
            "bylocation": bylocation,
            "valid": True
        })


class AdminBestsellersView(APIView):
    """
    Get bestsellers product of the current month data for admin panel
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or\
           not request.user.is_active or not request.user.is_staff:
            return RestResponse({"valid": False})
        # ==========================================================---
        bestsellers = []
        all_selled = []
        for item in OrderItem.objects.filter(
            order__created_at__year=datetime.now().year,
            order__created_at__month=datetime.now().month
        ):
            already = False
            for x in all_selled:
                if x["product_name"] == str(item):
                    x["product_quantity"] += item.quantity
                    x["product_amount"] += item._line_total
                    already = True
            if not already:
                if type(item.product) == ProductDefault:
                    unitprice = ProductDefault.objects.filter(
                        product_code=item.product_code
                    ).first().unit_price
                elif type(item.product) == ProductVariable:
                    unitprice = ProductVariableVariant.objects.filter(
                        product_code=item.product_code
                    ).first().unit_price
                all_selled.append({
                    "product_name": str(item),
                    "product_price": unitprice,
                    "product_quantity": item.quantity,
                    "product_amount": item._line_total
                })
        bestsellers = sorted(
            all_selled, key=lambda h: (int(h["product_quantity"])),
            reverse=True
        )[:2]
        for b in bestsellers:
            b["product_amount"] = Money(b["product_amount"])
        # ==========================================================---
        return RestResponse({
            "bestsellers": bestsellers,
            "valid": True
        })


class AdminStocksView(APIView):
    """
    Get stocks data for admin panel
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or\
           not request.user.is_active or not request.user.is_staff:
            return RestResponse({"valid": False})
        # ==========================================================---
        total = 0
        lowofstock_count = 0
        outofstock_count = 0
        for p in Product.objects.all():
            if type(p) == ProductDefault:
                total += 1
                if p.quantity <= 0:
                    outofstock_count += 1
                elif p.quantity <= 3:
                    lowofstock_count += 1
            elif type(p) == ProductVariable:
                for v in p.variants.all():
                    total += 1
                    if v.quantity <= 0:
                        outofstock_count += 1
                    elif v.quantity <= 3:
                        lowofstock_count += 1
        # ===---
        lowofstock = {
            "labels": [_("Low of Stock"), _("Total")],
            "datasets": [
                {
                    "data": [lowofstock_count, total],
                    "backgroundColor": ["#066bf9", "#eee"],
                    "fill": True
                }
            ]
        }
        outofstock = {
            "labels": [_("Out of Stock"), _("Total")],
            "datasets": [
                {
                    "data": [outofstock_count, total],
                    "backgroundColor": ["#066bf9", "#eee"],
                    "fill": True
                }
            ]
        }
        # ==========================================================---
        return RestResponse({
            "total": total,
            "lowofstock": lowofstock,
            "outofstock": outofstock,
            "valid": True
        })


class AdminLogsView(APIView):
    """
    Get logs data for admin panel
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or \
           not request.user.is_active or not request.user.is_staff:
            return RestResponse({"valid": False})
        # ==========================================================---
        logs = []
        for log in dmAdminLogs.objects.all()[0:5]:
            title_action = ""
            if log.user_action == 1:
                title_action = _("created")
            elif log.user_action == 2:
                title_action = _("updated")
            elif log.user_action == 3:
                title_action = _("deleted")
            # ===---
            if log.user is not None:
                user_text = str(_("by"))+" "+log.user.email
            else:
                user_text = ""
            # ===---
            logs.append({
                "title": log.title + " " + str(title_action),
                "content": "\""+log.content+"\"",
                "date": log.created_at.astimezone(
                            timezone.get_current_timezone()
                        ).strftime("%Y-%m-%d %H:%M"),
                "user": user_text,
                "action": log.user_action
            })
        # ==========================================================---
        return RestResponse({
            "logs": logs,
            "valid": True
        })
