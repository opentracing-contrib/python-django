from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^traced_with_attrs/', views.traced_func_with_attrs),
    url(r'^traced/', views.traced_func),
    url(r'^traced_scope/', views.traced_scope_func),
    url(r'^untraced/', views.untraced_func)
]
