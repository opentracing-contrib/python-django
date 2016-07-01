from django.shortcuts import render
from django.http import HttpResponse
from django_opentracing import trace
from django.conf import settings

tracer = settings.TRACER
# Create your views here.

def server_index(request):
	return HttpResponse("Hello, world. You're at the server index.")

@trace
def server_simple(request):
	return HttpResponse("This is a simple traced request.")

@trace
def server_log(request):
	span = tracer.get_span(request)
	span.log_event("hello world")
	return HttpResponse("Something was logged")

@trace
def server_child_span(request):
	span = tracer.get_span(request)
	child_span = tracer.tracer.start_span("child span", span)
	child_span.finish()
	return HttpResponse("A child span was created")