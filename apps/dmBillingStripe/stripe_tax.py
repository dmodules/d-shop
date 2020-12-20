import stripe
from settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_tax(tax):
    hst = gst = qst = pst = None
    if tax.hst:
        hst = stripe.TaxRate.create(display_name=tax.state + " : HST",
                                    percentage=tax.hst,
                                    inclusive=False)
        hst = hst.id
    if tax.gst:
        gst = stripe.TaxRate.create(display_name=tax.state + " : GST",
                                    percentage=tax.gst,
                                    inclusive=False)
        gst = gst.id
    if tax.qst:
        qst = stripe.TaxRate.create(display_name=tax.state + " : QST",
                                    percentage=tax.qst,
                                    inclusive=False)
        qst = qst.id
    if tax.pst:
        pst = stripe.TaxRate.create(display_name=tax.state + " : PST",
                                    percentage=tax.pst,
                                    inclusive=False)
        pst = pst.id
    return hst, gst, qst, pst


def update_tax(tax):
    if tax.hst:
        stripe.TaxRate.modify(tax.stripe_hst,
                              display_name=tax.state + " : HST")
    if tax.gst:
        stripe.TaxRate.modify(tax.stripe_gst,
                              display_name=tax.state + " : GST")
    if tax.qst:
        stripe.TaxRate.modify(tax.stripe_qst,
                              display_name=tax.state + " : QST")
    if tax.pst:
        stripe.TaxRate.modify(tax.stripe_pst,
                              display_name=tax.state + " : PST")
    return
