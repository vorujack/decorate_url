__author__ = 'Vorujack'

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import RegexURLResolver, Resolver404, ResolverMatch, RegexURLPattern, get_callable
from django.utils.encoding import force_text
from django.utils import six


def decorated_url(regex, view, kwargs=None, name=None, prefix='', wrap=None):
    if isinstance(view, (list, tuple)):
        urlconf_module, app_name, namespace = view
        return DecorateRegexURLResolver(regex, urlconf_module, kwargs, app_name=app_name, namespace=namespace, wrap=wrap)
    else:
        if isinstance(view, six.string_types):
            if not view:
                raise ImproperlyConfigured('Empty URL pattern view name not permitted (for pattern %r)' % regex)
            if prefix:
                view = prefix + '.' + view
        return DecorateRegexURLPattern(regex, view, kwargs, name, wrap)


class DecorateRegexURLResolver(RegexURLResolver):
    def __init__(self, regex, urlconf_name, default_kwargs=None, app_name=None, namespace=None, wrap=None):
        super(DecorateRegexURLResolver, self).__init__(regex, urlconf_name, default_kwargs, app_name, namespace)
        if isinstance(wrap, (tuple, list)):
            self.wrap = wrap
        elif wrap:
            self.wrap = [wrap]
        else:
            self.wrap = []

    def resolve(self, path):
        path = force_text(path)
        tried = []
        match = self.regex.search(path)
        if match:
            new_path = path[match.end():]
            for pattern in self.url_patterns:
                try:
                    sub_match = pattern.resolve(new_path)
                except Resolver404 as e:
                    sub_tried = e.args[0].get('tried')
                    if sub_tried is not None:
                        tried.extend([pattern] + t for t in sub_tried)
                    else:
                        tried.append([pattern])
                else:
                    if sub_match:
                        sub_match_dict = dict(match.groupdict(), **self.default_kwargs)
                        sub_match_dict.update(sub_match.kwargs)
                        return ResolverMatch(self._decorate(sub_match.func), sub_match.args, sub_match_dict,
                                             sub_match.url_name, self.app_name or sub_match.app_name,
                                             [self.namespace] + sub_match.namespaces)
                    tried.append([pattern])
            raise Resolver404({'tried': tried, 'path': new_path})
        raise Resolver404({'path': path})

    def _decorate(self, callback):
        for decorator in reversed(self.wrap):
            callback = decorator(callback)
        return callback


class DecorateRegexURLPattern(RegexURLPattern):
    def __init__(self, regex, callback, default_args=None, name=None, wrap=None):
        super(DecorateRegexURLPattern, self).__init__(regex, callback, default_args, name)
        if isinstance(wrap, (tuple, list)):
            self.wrap = wrap
        elif wrap:
            self.wrap = [wrap]
        else:
            self.wrap = []

    @property
    def callback(self):
        if self._callback is not None:
            return self._decorate(self._callback)

        self._callback = get_callable(self._callback_str)
        return self._decorate(self._callback)

    def _decorate(self, callback):
        for decorator in reversed(self.wrap):
            callback = decorator(callback)
        return callback
