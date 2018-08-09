from .middleware import OpenTracingMiddleware  # noqa
from .tracer import DjangoTracer  # noqa
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
