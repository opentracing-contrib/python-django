from django.conf import settings
import opentracing

class DjangoTracer(object):
    '''
    @param tracer the OpenTracing tracer to be used
    to trace requests using this DjangoTracer
    '''
    def __init__(self, tracer):
        self.tracer = tracer
        self.current_spans = {}

    def get_span(self, request): 
        '''
        @param request 
        Returns the span tracing this request
        '''
        return self.current_spans.get(request, None)

    def inject_as_headers(self, span, request):
        '''
        @param span
        @param request
        Injects the span as headers into the request so that 
        the trace can be continued across the wire.
        '''
        text_carrier = {}
        self.tracer.inject(span, opentracing.Format.TEXT_MAP, text_carrier)
        for k, v in text_carrier.iteritems():
            request.add_header(k,v)

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
            if hasattr(settings, 'OPENTRACING') and settings.OPENTRACING.get('TRACE_ALL_REQUESTS', False):
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
        span = None

        # start new span from trace info
        operation_name = view_func.__name__
        try:
            span = self.tracer.join(operation_name, opentracing.Format.TEXT_MAP, headers)
        except (opentracing.InvalidCarrierException, opentracing.TraceCorruptedException):
            span = self.tracer.start_span(operation_name)
        if span is None:
            span = self.tracer.start_span(operation_name)

        # add span to current spans 
        self.current_spans[request] = span

        # log any traced attributes
        for attr in attributes:
            if hasattr(request, attr):
                payload = str(getattr(request, attr))
                if payload:
                    span.set_tag(attr, payload)
        
        return span  

    def _finish_tracing(self, request):
        span = self.current_spans.pop(request, None)     
        if span is not None:
            span.finish()