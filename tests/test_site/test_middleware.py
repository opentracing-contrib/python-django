from django.test import SimpleTestCase, Client
from django.conf import settings
import mock


class TestDjangoOpenTracingMiddleware(SimpleTestCase):

    def test_middleware_untraced(self):
        client = Client()
        with mock.patch('opentracing.Span.set_tag') as set_tag:
            response = client.get('/untraced/')
            assert set_tag.call_args[0][0] == 'META'
        assert response['numspans'] == '1'
        assert len(settings.OPENTRACING_TRACER._current_spans) == 0

    def test_middleware_traced(self):
        client = Client()
        with mock.patch('opentracing.Span.set_tag') as set_tag:
            response = client.get('/traced/')
            assert set_tag.call_args[0][0] == 'META'
        assert response['numspans'] == '1'
        assert len(settings.OPENTRACING_TRACER._current_spans) == 0

    def test_middleware_traced_with_attrs(self):
        client = Client()
        with mock.patch('opentracing.Span.set_tag') as set_tag:
            response = client.get('/traced_with_attrs/')
            assert set_tag.call_args[0][0] == 'META'
        assert response['numspans'] == '1'
        assert len(settings.OPENTRACING_TRACER._current_spans) == 0
