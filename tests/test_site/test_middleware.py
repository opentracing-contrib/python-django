from django.test import SimpleTestCase, Client
from django.conf import settings
from opentracing.ext import tags


class TestDjangoOpenTracingMiddleware(SimpleTestCase):

    def setUp(self):
        settings.OPENTRACING_TRACER._tracer.reset()

    def test_middleware_untraced(self):
        client = Client()
        response = client.get('/untraced/')
        assert response['numspans'] == '1'
        assert len(settings.OPENTRACING_TRACER._current_scopes) == 0

    def test_middleware_traced(self):
        client = Client()
        response = client.get('/traced/')
        assert response['numspans'] == '1'
        assert len(settings.OPENTRACING_TRACER._current_scopes) == 0

    def test_middleware_traced_with_attrs(self):
        client = Client()
        response = client.get('/traced_with_attrs/')
        assert response['numspans'] == '1'
        assert len(settings.OPENTRACING_TRACER._current_scopes) == 0

    def test_middleware_traced_with_error(self):
        client = Client()
        with self.assertRaises(ValueError):
            client.get('/traced_with_error/')

        spans = settings.OPENTRACING_TRACER._tracer.finished_spans()
        assert len(spans) == 1
        assert spans[0].tags.get(tags.ERROR, False) is True

        assert len(spans[0].logs) == 1
        assert spans[0].logs[0].key_values.get('event', None) is 'error'
        assert isinstance(
                spans[0].logs[0].key_values.get('error.object', None),
                ValueError
        )

    def test_middleware_traced_scope(self):
        client = Client()
        response = client.get('/traced_scope/')
        assert response['active_span'] is not None
        assert response['request_span'] == response['active_span']
