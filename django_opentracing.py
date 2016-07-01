from django.conf import settings 
import opentracing
import sys

# an identifier for traced functions
trace_identififier = "opentracing_traced_view"

def trace(view_func):
	'''
	Decorator function used to trace a specific view function.
	
	Ex:

	@trace
	def some_view_func(request):
		// do some stuff
		return HttpResponse(args)

	The response of some_view_func will be traced, including
	continuing the trace if there are injected OT headers in 
	the request

	'''
	if hasattr(settings, 'TRACER'):
		def wrapper(request):
			return view_func(request)
		wrapper.__name__ = trace_identififier + view_func.__name__
		return wrapper
	else:
		return view_func

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

class OpenTracingMiddleware(object):
	'''
	__init__() is only called once, no arguments, when the Web server responds to the first request
	'''
	def __init__(self):
		'''
		I'm still unclear as to where the tracer should be placed; either in settings or maybe the
		package __init__ file? Or could also require a tracer file.
		'''
		try:
			self.tracer = settings.TRACER 
		except:
			self.tracer = opentracing.Tracer()

	def process_view(self, request, view_func, view_args, view_kwargs):
		if hasattr(settings, 'TRACING'):
			is_tracing = settings.TRACING
		else:
			is_tracing = True
		if not view_func.__name__.startswith(trace_identififier) or not is_tracing:
			return None

		headers = {}
		for k, v in request.META.iteritems():
			k = k.lower().replace('_','-')
			if k.startswith('http-'):
				k = k[5:]
			headers[k] = v
		span = None
		
		operation_name = view_func.__name__[len(trace_identififier):]
		try:
			span = self.tracer.tracer.join(operation_name, opentracing.Format.TEXT_MAP, headers)
		except:
			span = self.tracer.tracer.start_span(operation_name)
		
		self.tracer.current_spans[request] = span

	def process_response(self, request, response):
		try:
			span = self.tracer.get_span(request)
			span.finish()
		except:
			pass
		return response