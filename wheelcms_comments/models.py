from django.db import models
from django import forms

from wheelcms_axle.models import Configuration as BaseConfiguration
from wheelcms_axle.registries.configuration import configuration_registry

from wheelcms_axle.content import type_registry, Content
from wheelcms_axle.templates import template_registry
from wheelcms_axle.spoke import Spoke
from wheelcms_axle.forms import formfactory

class CommentBase(Content):
    class Meta:
        abstract = True

    ## gravatar oid?
    body = models.TextField(blank=False)

class Comment(CommentBase):
    pass

class CommentForm(formfactory(Comment)):
    pass
    ## captcha

    ## body doesn't have to be rich


class CommentType(Spoke):
    implicit_add = False   # can't create through frontend directly
    add_to_index = False   # do not index in search
    discussable = False    # well...

    model = Comment
    form = CommentForm

    title = "A comment"
    # type_icon = icon = ..

template_registry.register(CommentType, "wheelcms_comments/comment_view", "Comment View", default=True)

type_registry.register(CommentType)

class Configuration(models.Model):
    main = models.ForeignKey(BaseConfiguration, related_name="comments")
    enabled = models.BooleanField(default=True)
    notify_address = models.EmailField(blank=True)

class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        exclude = ['main']

configuration_registry.register("comments", "Comments", Configuration, ConfigurationForm)
