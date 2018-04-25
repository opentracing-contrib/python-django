from django.conf import settings
from django.utils.module_loading import import_string
import opentracing
import threading
from opentracing.ext import tags as ot_tags


SERVER_SPAN_TAGS = {
    ot_tags.SPAN_KIND: ot_tags.SPAN_KIND_RPC_SERVER
}


class DjangoTracer(object):
    '''
    @param tracer the OpenTracing tracer to be used
    to trace requests using this DjangoTracer
    '''
    def __init__(self, tracer=None):
        self._tracer_implementation = None
        if tracer:
            self._tracer_implementation = tracer
        self._current_spans = {}
        if not hasattr(settings, 'OPENTRACING_TRACE_ALL'):
            self._trace_all = False
        elif not getattr(settings, 'OPENTRACING_TRACE_ALL'):
            self._trace_all = False
        else:
            self._trace_all = True

        self.hooks = getattr(settings, 'OPENTRACING_HOOKS', {})

    @property
    def _tracer(self):
        if self._tracer_implementation:
            return self._tracer_implementation
        else:
            return opentracing.tracer

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
            # TODO: do we want to provide option of overriding
            # trace_all_requests so that they can trace certain attributes of
            # the request for just this request (this would require to
            # reinstate the name-mangling with a trace identifier, and another
            # settings key)
            if self._trace_all:
                return view_func

            # otherwise, execute decorator
            def wrapper(request):
                self._apply_tracing(request, view_func, list(attributes))
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
        for k, v in request.META.iteritems():
            k = k.lower().replace('_', '-')
            if k.startswith('http-'):
                k = k[5:]
            headers[k] = v

        # start new span from trace info
        span = None
        operation_name = view_func.__name__
        tags = SERVER_SPAN_TAGS.copy()
        tags[ot_tags.HTTP_METHOD] = request.method
        tags[ot_tags.HTTP_URL] = request.build_absolute_uri()
        try:
            span_ctx = self._tracer.extract(opentracing.Format.HTTP_HEADERS, headers)
            span = self._tracer.start_span(operation_name=operation_name,
                                           child_of=span_ctx, tags=tags)
        except (opentracing.InvalidCarrierException,
                opentracing.SpanContextCorruptedException):
            span = self._tracer.start_span(operation_name=operation_name,
                                           tags=tags)
        if span is None:
            span = self._tracer.start_span(operation_name=operation_name,
                                           tags=tags)

        # log any traced attributes
        for attr in attributes:
            if hasattr(request, attr):
                payload = str(getattr(request, attr))
                if payload:
                    span.set_tag(attr, payload)

        start_hook = self.hooks.get('start')
        if start_hook and callable(start_hook) and start_hook(span):
            return span

        # add span to current spans
        self._current_spans[request] = span

        return span

    def _finish_tracing(self, request):
        span = self._current_spans.pop(request, None)
        finish_hook = self.hooks.get('finish')
        if finish_hook and callable(finish_hook) and finish_hook(span=span):
            return
        if span:
            span.finish()


def initialize_global_tracer():
    '''
    Initialisation as per https://github.com/opentracing/opentracing-python/blob/9f9ef02d4ef7863fb26d3534a38ccdccf245494c/opentracing/__init__.py#L36

    Here the global tracer object gets initialised once from Django settings.
    '''
    # Short circuit without taking a lock
    if initialize_global_tracer.complete:
        return
    with initialize_global_tracer.lock:
        if initialize_global_tracer.complete:
            return
        if hasattr(settings, 'OPENTRACING_TRACER'):
            # Backwards compatibility with the old way of defining the tracer
            opentracing.tracer = settings.OPENTRACING_TRACER._tracer
        else:
            tracer_callable = getattr(settings, 'OPENTRACING_TRACER_CALLABLE', 'opentracing.Tracer')
            tracer_parameters = getattr(settings, 'OPENTRACING_TRACER_PARAMETERS', {})
            opentracing.tracer = import_string(tracer_callable)(**tracer_parameters)
            settings.OPENTRACING_TRACER = DjangoTracer()
        initialize_global_tracer.complete = True


initialize_global_tracer.lock = threading.Lock()
initialize_global_tracer.complete = False
