from django.test import SimpleTestCase, Client
from django.conf import settings

class TestDjangoOpenTracingMiddleware(SimpleTestCase):

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

    def test_middleware_traced_scope(self):
        client = Client()
        response = client.get('/traced_scope/')
        assert response['active_span'] is not None
        assert response['request_span'] == response['active_span']
