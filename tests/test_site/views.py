from django.http import HttpResponse
from django.conf import settings

tracer = settings.OPENTRACING_TRACER


def index(_request):
    return HttpResponse("index")


@tracer.trace('path', 'scheme', 'fake_setting')
def traced_func_with_attrs(_request):
    current_span_count = len(settings.OPENTRACING_TRACER._current_spans)
    response = HttpResponse()
    response['numspans'] = current_span_count
    return response


@tracer.trace()
def traced_func(_request):
    current_span_count = len(settings.OPENTRACING_TRACER._current_spans)
    response = HttpResponse()
    response['numspans'] = current_span_count
    return response


def untraced_func(_request):
    current_span_count = len(settings.OPENTRACING_TRACER._current_spans)
    response = HttpResponse()
    response['numspans'] = current_span_count
    return response
