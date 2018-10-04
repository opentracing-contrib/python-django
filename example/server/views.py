from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import opentracing

tracing = settings.OPENTRACING_TRACING

# Create your views here.

def server_index(request):
    return HttpResponse("Hello, world. You're at the server index.")

@tracing.trace('method')
def server_simple(request):
    return HttpResponse("This is a simple traced request.")

@tracing.trace()
def server_log(request):
    tracing.tracer.active_span.log_event("Hello, world!")
    return HttpResponse("Something was logged")

@tracing.trace()
def server_child_span(request):
    child_span = tracing.tracer.start_active_span("child span")
    child_span.close()
    return HttpResponse("A child span was created")
