from django.http import HttpResponse
from django.conf import settings

tracer = settings.OPENTRACING_TRACER

def index(request):
    return HttpResponse("index")

@tracer.trace('path', 'scheme', 'fake_setting')
def traced_func_with_attrs(request):
    currentSpanCount = len(settings.OPENTRACING_TRACER._current_spans) 
    response = HttpResponse()
    response['numspans'] = currentSpanCount 
    return response

@tracer.trace()
def traced_func(request):
    currentSpanCount = len(settings.OPENTRACING_TRACER._current_spans) 
    response = HttpResponse()
    response['numspans'] = currentSpanCount 
    return response

def untraced_func(request):
    currentSpanCount = len(settings.OPENTRACING_TRACER._current_spans) 
    response = HttpResponse()
    response['numspans'] = currentSpanCount 
    return response


