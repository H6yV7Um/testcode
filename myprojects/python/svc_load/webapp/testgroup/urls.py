#encoding:utf-8

from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'serverlist', views.server_list),
    url(r'update', views.update_server),
    url(r'delete', views.del_server),
    url(r'add', views.add_server),

]
