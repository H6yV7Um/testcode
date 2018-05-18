# -*- coding: utf-8 -*-
import logging

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden

from dataprocess import response_msg
from .models import TestGroupServers, TestServerFrom

logger = logging.getLogger('svc_web')

def server_list(req):
    '''func doc'''
    if req.method == 'GET':
        data_list = list(TestGroupServers.objects.values())
        return response_msg(data_list)
    else:
        return HttpResponseForbidden()

def add_server(req):
    '''func doc'''
    if req.method == 'POST' and req.POST:
        new_server = TestServerFrom(req.POST)
        if new_server.is_valid():
            new_server.save()
            msg = 1
        else:
            msg = new_server.error_message
        return response_msg(msg)
    else:
        return HttpResponseForbidden

def update_server(req):
    '''func doc'''
    if req.method == 'POST' and req.POST:
        pk_id = req.POST.get('id', None)
        server = TestGroupServers.objects.get(pk=pk_id)
        update_server = TestServerFrom(req.POST, instance=server)
        num = update_server.save()
        if not num:
            return response_msg('update fail')
        return response_msg(1)
    else:
        return HttpResponseForbidden()

def del_server(req):
    '''func doc'''
    if req.method == 'POST' and req.POST:
        pk_id = req.POST.get('id', None)
        num = TestGroupServers.objects.filter(pk=pk_id).delete()
        if not num:
            return response_msg('delete fail')
        return response_msg(1)
    else:
        return HttpResponseForbidden()
