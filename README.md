django decorate url
====================

Django decorate URL allows you to apply a decorator to a URL pattern.

Install
-------

You can install with pip:


    pip install decorate-url


Usage
-----


In Django/Python you can wrap a function like this:

```python
@wrapper
def function(..):
    ...
```
This is great but only works on a single view.  This module instead allows
you to decorate an entire url pattern. Have a look at the examples below:



Example 1 in `urls.py`
----------------------
```
from decorate_url import decorated_url
from django.conf.urls import include, url
from django.contrib.auth.decorators import user_passes_test

def email_check(user):
    return user.email.endswith('@example.com')

urlpatterns = [
    url(r'^accounts/', include('apps.home.urls')),
    # Admin
    decorated_url(r'^example/', include('apps.example.urls'),
                  wrap=user_passes_test(email_check),
]
```
In the above example, the `user_passes_test` is applied to the 
pattern `r'^example/'`. It ensures that only users with emails that end in `@example.com` can
access urls with the `r'^example/'` patten.



Example 2 in `urls.py`
----------------------
```
from decorate_url import decorated_url
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^accounts/', include('apps.home.urls')),
    # Admin
    decorated_url(r'^admin/', include(admin.site.urls),
                  wrap=staff_member_required(login_url=settings.LOGIN_URL)),
]
```
In the above example, the `staff_member_required` is applied to the 
pattern `r'^admin/'`. By setting the `login_url` to `settings.LOGIN_URL`, access to the 
standard admin login page is blocked and forces staff users through the login screen
defined by settings.LOGIN_URL.
