WheelCMS comments
=================

This package provides support for simple (local) comments on WheelCMS content.
It's similar to the wheelcms_disqus package, but does not require an external
service.

Installation
------------

Add wheelcms_comments to your INSTALLED_APPS

wheelcms_comments uses django-simple-captcha, so you will need to include this
as well:

Add 

    urlpatterns += patterns('',
        url(r'^captcha/', include('captcha.urls')),
    )

to your urls.py

Add 'captcha' to your INSTALLED_APPS

