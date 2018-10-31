from django.conf import settings
from django_opentracing.tracer import initialize_global_tracer
try:
    # Django >= 1.10
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object

class OpenTracingMiddleware(MiddlewareMixin):
    '''
    __init__() is only called once, no arguments, when the Web server responds to the first request
    '''
    def __init__(self, get_response=None):
        '''
        TODO: ANSWER Qs
        - Is it better to place all tracing info in the settings file, or to require a tracing.py file with configurations?
        - Also, better to have try/catch with empty tracer or just fail fast if there's no tracer specified
        '''
        self.get_response = get_response
        self._tracer = None

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Lazily initialize the Tracer for compatibility with Jaeger and Django>=1.10
        if self._tracer is None:
            initialize_global_tracer()
            self._tracer = settings.OPENTRACING_TRACER

        # determine whether this middleware should be applied
        # NOTE: if tracing is on but not tracing all requests, then the tracing occurs
        # through decorator functions rather than middleware
        if not self._tracer._trace_all:
            return None

        if hasattr(settings, 'OPENTRACING_TRACED_ATTRIBUTES'):
            traced_attributes = getattr(settings, 'OPENTRACING_TRACED_ATTRIBUTES')
        else:
            traced_attributes = []
        self._tracer._apply_tracing(request, view_func, traced_attributes)

    def process_response(self, request, response):
        self._tracer._finish_tracing(request)
        return response

