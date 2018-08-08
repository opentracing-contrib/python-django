## Example

This is an example of a Django site with tracing implemented using the django_opentracing package. To run the example, make sure you've installed package `opentracing` and the `Tracer` of your choice (Jaeger, LightStep, etc).

Navigate to this directory and then run:

```
> python manage.py runserver 8000
```

Open in your browser `localhost:8000/client`.

### Trace a Request and Response

Navigate to `/client/simple` to send a request to the server. There will be a span created for both the client request and the server response from the tracing decorators, `@tracer.trace()`.

![simple](https://raw.githubusercontent.com/kcamenzind/django_opentracing/master/example/img/simple.png)

### Log a Span

Navigate to `/client/log` to send a request to the server and log something to the server span. There will be a span created for both the client request and server response from the tracing decorators. The server views.py handler will manually log the server span with the message 'Hello, world!'.

![log](https://raw.githubusercontent.com/kcamenzind/django_opentracing/master/example/img/log.png)

### Create a Child Span manually

Navigate to `/client/childspan` to send a request to the server and create a child span for the server. There will be span created for both the client request and server response from the tracing decorators. The server views.py handler will manually create and finish a child span for the server span. 

![child span](https://raw.githubusercontent.com/kcamenzind/django_opentracing/master/example/img/childspan.png)

### Don't Trace a Request

Navigating to `/client` will not produce any traces because there is no `@trace.trace()` decorator. However, if `settings.OPENTRACING['TRACE_ALL_REQUESTS'] == True`, then every request (including this one) will be traced, regardless of whether or not it has a tracing decorator.
