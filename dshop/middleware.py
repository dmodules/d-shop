from __future__ import unicode_literals

from copy import deepcopy

from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.utils.six import string_types

from django.urls import resolve, Resolver404
from django.utils.deprecation import MiddlewareMixin


class AdminReorderMiddleware(MiddlewareMixin):
    """
    Used to reorder admin panel.
    """

    def init_config(self, request, app_list):
        self.request = request
        self.app_list = app_list
        self.config = getattr(settings, "ADMIN_REORDER", None)
        if not self.config:
            raise ImproperlyConfigured("ADMIN_REORDER config is not defined.")
        if not isinstance(self.config, (tuple, list)):
            raise ImproperlyConfigured(
                "ADMIN_REORDER config parameter must be \
                 tuple or list. Got {config}"
                .format(config=self.config))
        admin_index = admin.site.index(request)
        try:
            app_list = admin_index.context_data["app_list"]
        except KeyError:
            pass
        self.models_list = []
        for app in app_list:
            for model in app["models"]:
                model["model_name"] = self.get_model_name(
                    app["app_label"], model["object_name"])
                self.models_list.append(model)

    def get_app_list(self):
        ordered_app_list = []
        for app_config in self.config:
            app = self.make_app(app_config)
            if app:
                ordered_app_list.append(app)
        return ordered_app_list

    def make_app(self, app_config):
        if not isinstance(app_config, (dict, string_types)):
            raise TypeError(
                "ADMIN_REORDER list item must be dict or string. Got %s" %
                repr(app_config))
        if isinstance(app_config, string_types):
            return self.find_app(app_config)
        else:
            return self.process_app(app_config)

    def find_app(self, app_label):
        for app in self.app_list:
            if app["app_label"] == app_label:
                return app

    def get_model_name(self, app_name, model_name):
        if "." not in model_name:
            model_name = "%s.%s" % (app_name, model_name)
        return model_name

    def process_app(self, app_config):
        if "app" not in app_config:
            raise NameError(
                "ADMIN_REORDER list item must define a 'app' name. Got %s" %
                repr(app_config))
        app = self.find_app(app_config["app"])
        if app:
            app = deepcopy(app)
            if "label" in app_config:
                app["name"] = app_config["label"]
            if "models" in app_config:
                models_config = app_config.get("models")
                models = self.process_models(models_config)
                if models:
                    app["models"] = models
                else:
                    return None
            return app

    def process_models(self, models_config):
        if not isinstance(models_config, (dict, list, tuple)):
            raise TypeError(
                "'models' config for ADMIN_REORDER list item \
                  must be dict or list/tuple. Got %s"
                % repr(models_config))
        ordered_models_list = []
        for model_config in models_config:
            model = None
            if isinstance(model_config, dict):
                model = self.process_model(model_config)
            else:
                model = self.find_model(model_config)
            if model:
                ordered_models_list.append(model)
        return ordered_models_list

    def find_model(self, model_name):
        for model in self.models_list:
            if model["model_name"] == model_name:
                return model

    def process_model(self, model_config):
        for key in (
            "model",
            "label",
        ):
            if key not in model_config:
                return
        model = self.find_model(model_config["model"])
        if model:
            model["name"] = model_config["label"]
            return model

    def process_template_response(self, request, response):
        try:
            url = resolve(request.path_info)
        except Resolver404:
            return response
        if not url.app_name == "admin" and url.url_name not in [
                "index", "app_list"
        ]:
            return response
        try:
            app_list = response.context_data["app_list"]
        except KeyError:
            return response
        self.init_config(request, app_list)
        ordered_app_list = self.get_app_list()
        response.context_data["app_list"] = ordered_app_list
        return response
