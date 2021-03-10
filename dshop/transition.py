
import os
import json
from django.contrib.auth.models import AnonymousUser
from django.core.management import call_command
from django.db import models
from django.http.request import HttpRequest
from django.template import loader
from django.utils.six.moves.urllib.parse import urlparse

from post_office import mail
from post_office.models import EmailTemplate
from django.core.mail import send_mail

from settings import SHOP_VENDOR_EMAIL
from settings import NOTIFICATION_TARGET
from settings import CC_EMAILS
from shop.conf import app_settings
from shop.models.order import BaseOrder
from shop.models.notification import Notification
from shop.serializers.order import OrderDetailSerializer
from shop.serializers.delivery import DeliverySerializer
from shop.signals import email_queued


class EmulateHttpRequest(HttpRequest):
    """
    Emulate a request to be used in email context.
    """
    def __init__(self, customer, stored_request):
        super(EmulateHttpRequest, self).__init__()
        try:
            parsedurl = urlparse(stored_request.get('absolute_base_uri'))
            self.path = self.path_info = parsedurl.path
            self.environ = {}
            self.META['PATH_INFO'] = parsedurl.path
            self.META['SCRIPT_NAME'] = ''
            self.META['HTTP_HOST'] = parsedurl.netloc
            self.META['HTTP_X_FORWARDED_PROTO'] = parsedurl.scheme
            self.META['QUERY_STRING'] = parsedurl.query
            self.META['HTTP_USER_AGENT'] = stored_request.get('user_agent')
            self.META['REMOTE_ADDR'] = stored_request.get('remote_ip')
            self.method = 'GET'
            self.LANGUAGE_CODE = self.COOKIES[
                'django_language'] = stored_request.get('language')
            self.customer = customer
            self.user = customer.is_anonymous and AnonymousUser or customer.user
            self.current_page = None
        except Exception as e:
            print(e)


def transition_change_notification(order, miniorder=None):
    """
    A function to prepare an email to be queued if a notification exist
    in the admin panel for the current transition of the :param order.

    At the end, will force all queued email to be send.
    """

    if not isinstance(order, BaseOrder):
        raise TypeError("Object order must inherit from class BaseOrder")
    emails_in_queue = False

    print(order.status)

    if order.status not in NOTIFICATION_TARGET:
        return

    target = NOTIFICATION_TARGET[order.status]
    print(target)

    emulated_request = EmulateHttpRequest(order.customer,
                                          order.stored_request)
    customer_serializer = app_settings.CUSTOMER_SERIALIZER(order.customer)
    render_context = {'request': emulated_request, 'render_label': 'email'}
    if miniorder is not None:
        order_serializer = miniorder
    else:
        order_serializer = None

    language = order.stored_request.get('language')
    context = {
        'customer': customer_serializer.data,
        'order': order_serializer,
        'ABSOLUTE_BASE_URI':
        emulated_request.build_absolute_uri().rstrip('/'),
        'render_language': language,
    }
    try:
        latest_delivery = order.delivery_set.latest('pk')
        context['latest_delivery'] = DeliverySerializer(
            latest_delivery, context=render_context
        ).data
    except (AttributeError, models.ObjectDoesNotExist):
        pass

    try:
        template = NOTIFICATION_TARGET[order.status]['email_template']
        template = loader.get_template(template)
        html_message = template.render(context)
    except EmailTemplate.DoesNotExist as e:
        template = None
        print("Error in notification: " + str(e))

    # Temperory comment for testing
    '''if target['to_vendor']:
        cc_emails = ''
        if target['cc_emails']:
            cc_emails = CC_EMAILS
        send_mail(
            SHOP_VENDOR_EMAIL,
            html_message=html_message,
            context=context,
            render_on_delivery=True
        )'''
    from settings import EMAIL_HOST_USER
    if target['to_customer']:
        # Once email will be working, need to add subject and body
        send_mail(
            'Subject: test mail',
            '',
            EMAIL_HOST_USER,
            [order.customer.email, ],
            html_message=html_message,
        )

    emails_in_queue = True
    if emails_in_queue:
        email_queued()

def quotation_new_notification(quotation):
    emails_in_queue = False
    emulated_request = EmulateHttpRequest(quotation.customer, quotation.stored_request)
    customer_serializer = app_settings.CUSTOMER_SERIALIZER(quotation.customer)
    render_context = {'request': emulated_request, 'render_label': 'email'}
    language = quotation.stored_request.get('language')
    quotation_items = []
    for item in quotation.quotation.all():
        data = {}
        data['name'] = item.product_name
        if item.product_type == 1:
            data['code'] = item.product_code
        else:
            data['code'] = item.variant_code
        data['quantity'] = item.quantity
        if item.variant_attribute:
            data['attributes'] = "(" + item.variant_attribute + ")"
        else:
            data['attributes'] = ""
        quotation_items.append(data)
    quotation_data = {
        'id': quotation.id,
        'number': quotation.number,
        'items': quotation_items
    }
    try:
       shipping = quotation.customer.shippingaddress_set.all()[0].as_text()
    except Exception as e:
        print(e)
    
    context = {
        'customer': customer_serializer.data,
        'quotation': quotation_data,
        'shipping': shipping,
        'render_language': language,
    }
    if quotation.extra:
        context['phone'] = json.loads(quotation.extra)["phone"] if json.loads(quotation.extra)["phone"] != "" else None
    else:
        context['phone'] = ""
    attachments = {}
    template = EmailTemplate.objects.get(name='customer_quotation_receipt')
    mail.send(
        [SHOP_VENDOR_EMAIL],
        template=template,
        context=context,
        attachments=attachments,
        render_on_delivery=True
    )
    emails_in_queue = True
    if emails_in_queue:
        email_queued()
        call_command('send_queued_mail')


