from django.conf import settings 
import opentracing

class OpenTracingMiddleware(object):
    '''
    __init__() is only called once, no arguments, when the Web server responds to the first request
    '''
    def __init__(self):
        '''
        TODO: ANSWER Qs
        - Is it better to place all tracing info in the settings file, or to require a tracing.py file with configurations?
        - Also, better to have try/catch with empty tracer or just fail fast if there's no tracer specified
        '''
        if hasattr(settings, 'OPENTRACING_TRACER'):
            self._tracer = settings.OPENTRACING_TRACER 
        else:
            self._tracer = opentracing.Tracer()

    def process_view(self, request, view_func, view_args, view_kwargs):
        # determine whether this middleware should be applied
        # NOTE: if tracing is on but not tracing all requests, then the tracing occurs
        # through decorator functions rather than middleware
        if not hasattr(settings, 'OPENTRACING_TRACED_ALL') or not getattr(settings, 'OPENTRACING_TRACED_ALL'):
            return None

        if hasattr(settings, 'OPENTRACING_TRACED_ATTRIBUTES'):
            traced_attributes = getattr(settings, 'OPENTRACING_TRACED_ATTRIBUTES')
        else: 
            traced_attributes = []
        self._tracer._apply_tracing(request, view_func, traced_attributes)

    def process_response(self, request, response):
        self._tracer._finish_tracing(request)
        return response