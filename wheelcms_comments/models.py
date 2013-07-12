from django.db import models
from django import forms

from wheelcms_axle.models import Configuration as BaseConfiguration
from wheelcms_axle.registries.configuration import configuration_registry

class Configuration(models.Model):
    main = models.ForeignKey(BaseConfiguration, related_name="comments")
    enabled = models.BooleanField(default=True)
    notify_address = models.EmailField(blank=True)

class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        exclude = ['main']

configuration_registry.register("comments", "Comments", Configuration, ConfigurationForm)
