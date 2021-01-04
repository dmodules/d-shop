from djng.forms import NgModelFormMixin
from djng.styling.bootstrap3.forms import Bootstrap3Form


class FilterForm(NgModelFormMixin, Bootstrap3Form):
    scope_prefix = "filters"
