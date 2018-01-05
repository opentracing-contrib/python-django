from .middleware import OpenTracingMiddleware
from .tracer import DjangoTracer
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
