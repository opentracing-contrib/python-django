from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

tracer = settings.OPENTRACING['TRACER']

# Create your views here.

def server_index(request):
    return HttpResponse("Hello, world. You're at the server index.")

@tracer.trace()
def server_simple(request):
    return HttpResponse("This is a simple traced request.")

@tracer.trace()
def server_log(request):
    span = tracer.get_span(request)
    if span is not None:
        span.log_event("Hello, world!")
    return HttpResponse("Something was logged")

@tracer.trace()
def server_child_span(request):
    span = tracer.get_span(request)
    if span is not None:
        child_span = tracer.tracer.start_span("child span", span)
        child_span.finish()
    return HttpResponse("A child span was created")