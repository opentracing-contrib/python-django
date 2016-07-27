##################
Django Opentracing
##################

This package enables distributed tracing in Django projects via `The OpenTracing Project`_. Once a production system contends with real concurrency or splits into many services, crucial (and formerly easy) tasks become difficult: user-facing latency optimization, root-cause analysis of backend errors, communication about distinct pieces of a now-distributed system, etc. Distributed tracing follows a request on its journey from inception to completion from mobile/browser all the way to the microservices. 

As core services and libraries adopt OpenTracing, the application builder is no longer burdened with the task of adding basic tracing instrumentation to their own code. In this way, developers can build their applications with the tools they prefer and benefit from built-in tracing instrumentation. OpenTracing implementations exist for major distributed tracing systems and can be bound or swapped with a one-line configuration change.

If you want to learn more about the underlying python API, visit the python `source code`_.

.. _The OpenTracing Project: http://opentracing.io/
.. _source code: https://github.com/opentracing/opentracing-python

Installation
============

Run the following command::

    $ pip install django_opentracing

Setting up Tracing
==================

In order to implement tracing in your system, add the following lines of code to your site's settings.py file:

.. code-block:: python

    import django_opentracing

    # OpenTracing settings

    # if not included, defaults to False
    # has to come before OPENTRACING_TRACER setting because python...
    OPENTRACING_TRACE_ALL = False, 

    # defaults to []
    # only valid if OPENTRACING_TRACE_ALL == True
    OPENTRACING_TRACED_ATTRIBUTES = ['arg1', 'arg2'],

    # some_opentracing_tracer can be any valid OpenTracing tracer implementation
    OPENTRACING_TRACER = django_opentracing.DjangoTracer(some_opentracing_tracer), 

**Note:** Valid request attributes to trace are listed [here](https://docs.djangoproject.com/en/1.9/ref/request-response/#django.http.HttpRequest). When you trace an attribute, this means that created spans will have tags with the attribute name and the request's value.

Tracing All Requests
====================

In order to trace all requests, set `OPENTRACING_TRACE_ALL = True`. If you want to trace any attributes for all requests, then add them to `OPENTRACING_TRACED_ATTRIBUTES`. For example, if you wanted to trace the path and method, then set `OPENTRACING_TRACED_ATTRIBUTES = ['path', 'method']`.

Tracing all requests uses the middleware django_opentracing.OpenTracingMiddleware, so add this to your settings.py file's `MIDDLEWARE_CLASSES` at the top of the stack.

.. code-block:: python

    MIDDLEWARE_CLASSES = [
        'django_opentracing.OpenTracingMiddleware',
        ... # other middleware classes
        ...
        ]

Tracing Individual Requests
===========================

If you don't want to trace all requests to your site, then you can use function decorators to trace individual view functions. This can be done by adding the following lines of code to views.py (or any other file that has url handler functions):

.. code-block:: python

    from django.conf import settings

    tracer = settings.OPENTRACING_TRACER

    @tracer.trace(optional_args)
    def some_view_func(request):
        ... #do some stuff

This tracing method doesn't use middleware, so there's no need to add it to your settings.py file.

The optional arguments allow for tracing of request attributes. For example, if you want to trace metadata, you could pass in `@tracer.trace('META')` and request.META would be set as a tag on all spans for this view function.

**Note:** If you turn on `OPENTRACING_TRACE_ALL`, this decorator will be ignored, including any traced request attributes. 

Accessing Spans Manually
========================

In order to access the span for a request, we've provided an method `DjangoTracer.get_span(request)` that returns the span for the request, if it is exists and is not finished. This can be used to log important events to the span, set tags, or create child spans to trace non-RPC events.

Tracing an RPC
==============

If you want to make an RPC and continue an existing trace, you can inject the current span into the RPC. For example, if making an http request, the following code will continue your trace across the wire:

.. code-block:: python

    @tracer.trace()
    def some_view_func(request):
        new_request = some_http_request
        current_span = tracer.get_span(request)
        text_carrier = {}
        opentracing_tracer.inject(span, opentracing.Format.TEXT_MAP, text_carrier)
        for k, v in text_carrier.iteritems():
            request.add_header(k,v)
        ... # make request

Example
=======

Here is an `example`_ of a Django application that acts as both a client and server,
with integrated OpenTracing tracers.

.. _example: https://github.com/opentracing-contrib/python-django/tree/master/example

Further Information
===================

If you’re interested in learning more about the OpenTracing standard, please visit `opentracing.io`_ or `join the mailing list`_. If you would like to implement OpenTracing in your project and need help, feel free to send us a note at `community@opentracing.io`_.

.. _opentracing.io: http://opentracing.io/
.. _join the mailing list: http://opentracing.us13.list-manage.com/subscribe?u=180afe03860541dae59e84153&id=19117aa6cd
.. _community@opentracing.io: community@opentracing.io

