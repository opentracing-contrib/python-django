# Django Opentracing

This is an extension for Django that provides support for OpenTracing. In order to use this package, ensure that have `opentracing` installed and are able to instantiate some implementation of an OpenTracing tracer. 

## Setting up Tracing

In order to implement tracing in your system, add the following lines of code to your site's settings.py file:

```python

import django_opentracing

# OpenTracing settings

OPENTRACING = {
    'TRACING': True, # if not included, defaults to True
    'TRACER': django_opentracing.DjangoTracer(some_opentracing_tracer), # you can use any valid opentracing tracer implementation
    'TRACE_ALL_REQUESTS': False, # if not included, defaults to False
    'TRACED_REQUEST_ATTRIBUTES': [], # only valid if tracing all requests
}
```

Note: Valid request attributes to trace are listed [here](https://docs.djangoproject.com/en/1.9/ref/request-response/#django.http.HttpRequest). When you trace an attribute, this means that created spans will have tags with the attribute name and the request's value.

## Tracing All Requests

In order to trace all requests, set `'TRACE_ALL_REQUESTS': True`. If you want to trace any attributes for all requests, then add them to `'TRACED_REQUEST_ATTRIBUTES'`. For example, if you wanted to trace the path and method, then set `'TRACED_REQUEST_ATTRIBUTES': ['path', 'method']`.

Tracing all requests uses the middleware django_opentracing.OpenTracingMiddleware, so add this to your settings.py file's `MIDDLEWARE_CLASSES` at the top of the stack.

```python
MIDDLEWARE_CLASSES = [
    'django_opentracing.OpenTracingMiddleware',
    ... # other middleware classes
    ...
    ]
```

## Tracing Individual Requests

If you don't want to trace all requests to your site, then you can use function decorators to trace individual view functions. This can be done by adding the following lines of code to views.py (or any other file that has url handler functions):

```python
from django.conf import settings

tracer = settings.OPENTRACING['TRACER']

@tracer.trace(optional_args)
def some_view_func(request):
    ... #do some stuff
```
This tracing method doesn't use middleware, so there's no need to add it to your settings.py file.

The optional arguments allow for tracing of request attributes. For example, if you want to trace metadata, you could pass in `@tracer.trace('META')` and request.META would be set as a tag on all spans for this view function.

Note: If you turn on `TRACE_ALL_REQUESTS`, this decorator will be ignored, including any traced request attributes. 

## Accessing Spans Manually

In order to access the span for a request, we've provided an method `DjangoTracer.get_span(request)` that returns the span for the request, if it is exists and is not finished. This can be used to log important events to the span, set tags, or create child spans to trace non-RPC events.

## Tracing an RPC

If you want to make an RPC and continue an existing trace, you can inject the current span into the RPC. For example, if making an http request, the following code will continue your trace across the wire:

```python
@tracer.trace()
def some_view_func(request):
    new_request = some_http_request
    current_span = tracer.get_span(request)
    tracer.inject_as_headers(current_span, new_request)
    ... # make request
```
Note: `DjangoTracer.inject_as_headers(span, request)` is a convenience method that injects the span into an http request's headers`.

