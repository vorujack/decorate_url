django decorate url
====================

Django decorate URL

in python you can wrap function to other like this

```python
@wrapper
def function(..):
    ...
```
by this syntax any time call function wrapped to wrapper function
 
in django you can use this syntax for views required login
 
by this module you can wrap whole url into a method like this

Example Usage:
```python
from decorate_url import decorated_url as url

urlpatterns = patterns('',
    url(r'^', include('Main.urls'), wrap=never_cache),
)
```
