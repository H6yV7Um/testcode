#encoding:utf-8

from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.test, name='test'),
    url(r'list', views.client_list),
    url(r'update', views.update_client),
    url(r'delete', views.del_client),
    url(r'add', views.add_client),
    url(r'deploy', views.deploy),
    url(r'data/start_hatch', views.start_hatch_data),
    url(r'data/stats', views.req_stats),
    url(r'data/reset', views.reset),
    url(r'data/getuids', views.get_push_uid),
    url(r'getlocust', views.get_locust_master),
    url(r'getrecords', views.get_load_test_record),
    url(r'loadtest/stats', views.get_load_test_stats),
    url(r'loadtest/exceptions', views.get_load_test_exceptions),
    url(r'startpush', views.start_push),
    url(r'profile', views.get_user_profile),
    url(r'logout', views.user_logout),
    url(r'change_password', views.change_password),
    url(r'functest/records', views.get_func_test_record),
    url(r'functest/detail_info', views.get_func_test_error_msg),
    url(r'functest/console', views.get_build_console),
    url(r'functest/start_build', views.start_build),
    url(r'functest/stop_build', views.stop_build),
]
