from django.conf import settings
import opentracing

class DjangoTracer(object):
    '''
    @param tracer the OpenTracing tracer to be used
    to trace requests using this DjangoTracer
    '''
    def __init__(self, tracer):
        self._tracer = tracer
        self._current_spans = {}

    def get_span(self, request): 
        '''
        @param request 
        Returns the span tracing this request
        '''
        return self._current_spans.get(request, None)

    def trace(self, *attributes):
        '''
        Function decorator that traces functions
        NOTE: Must be placed after the @app.route decorator
        @param attributes any number of flask.Request attributes
        (strings) to be set as tags on the created span
        '''
        def decorator(view_func):
            # if tracing all requests, then we ignore these decorators
            # TODO: do we want to provide option of overriding trace_all_requests so that they 
            # can trace certain attributes of the request for just this request (this would require
            # to reinstate the name-mangling with a trace identifier, and another settings key)
            if settings.OPENTRACING_TRACE_ALL:
                return view_func
            # otherwise, execute decorator
            def wrapper(request):
                span = self._apply_tracing(request, view_func, list(attributes))
                r = view_func(request)
                self._finish_tracing(request)
                return r
            return wrapper
        return decorator

    def _apply_tracing(self, request, view_func, attributes):
        '''
        Helper function to avoid rewriting for middleware and decorator.
        Returns a new span from the request with logged attributes and 
        correct operation name from the view_func.
        '''

        # strip headers for trace info
        headers = {}
        for k,v in request.META.iteritems():
            k = k.lower().replace('_','-')
            if k.startswith('http-'):
                k = k[5:]
            headers[k] = v              

        # start new span from trace info
        span = None
        operation_name = view_func.__name__
        try:
            span_ctx = self._tracer.extract(opentracing.Format.TEXT_MAP, headers)
            span = self._tracer.start_span(operation_name=operation_name, references=opentracing.ChildOf(span_ctx))
        except (opentracing.InvalidCarrierException, opentracing.SpanContextCorruptedException) as e:
            span = self._tracer.start_span(operation_name=operation_name, tags={"Extract failed": str(e)})
        if span is None:
            span = self._tracer.start_span(operation_name)

        # add span to current spans 
        self._current_spans[request] = span

        # log any traced attributes
        for attr in attributes:
            if hasattr(request, attr):
                payload = str(getattr(request, attr))
                if payload:
                    span.set_tag(attr, payload)
        
        return span  

    def _finish_tracing(self, request):
        span = self._current_spans.pop(request, None)     
        if span is not None:
            span.finish()