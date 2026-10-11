try:
    from django.urls import re_path
except ImportError:  # Django < 2.0, where re_path did not exist yet
    from django.conf.urls import url as re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^traced_with_attrs/', views.traced_func_with_attrs),
    re_path(r'^traced_with_error/', views.traced_func_with_error),
    re_path(r'^traced_with_arg/?(?P<arg>\d+)?/?', views.traced_func_with_arg),
    re_path(r'^traced/', views.traced_func),
    re_path(r'^traced_scope/', views.traced_scope_func),
    re_path(r'^untraced/', views.untraced_func)
]
