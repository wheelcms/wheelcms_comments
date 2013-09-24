WheelCMS comments
=================

![Build status](https://travis-ci.org/wheelcms/wheelcms_comments.png)

This package provides support for simple (local) comments on WheelCMS content.
It's similar to the
[wheelcms_disqus package](https://github.com/wheelcms/wheelcms_disqus/), but does
not require an external service.

Installation
------------

Add wheelcms_comments to your INSTALLED_APPS

wheelcms_comments uses [django-simple-captcha](https://django-simple-captcha.readthedocs.org/en/latest/usage.html), so you will need to include this
as well:

Add

    from django.conf.urls.defaults import *

    urlpatterns += patterns('',
        url(r'^captcha/', include('captcha.urls')),
    )

to your urls.py

django-simple-captcha  depends on the PIL library. You may need to install "python-imaging" or Pillow depending on your OS/Distribution. You will also need FreeType support with your PIL.

Lastly, add 'captcha' to your INSTALLED_APPS

Using comments
--------------

Now you should be able to enable commenting in your site's settings (save
the settings the first time, it may show incorrectly that comments are
already enabled).

You can also enable/disable comments on a per-content basis.

New contents will be created as WheelCMS content (content type Comment)
with an initial state 'pending'. You can use the workflow dropup in the
toolbar to moderate pending comments.

