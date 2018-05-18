# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm


class TestGroupServers(models.Model):
    server_ip = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    usage = models.CharField(max_length=255)
    server_type = models.IntegerField()
    cpu = models.CharField(max_length=32, blank=True, null=True)
    memory = models.CharField(max_length=32, blank=True, null=True)
    disk = models.CharField(max_length=32, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    modify_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.server_ip

    class Meta:
        db_table = 'test_group_servers'


class TestServerFrom(ModelForm):
    class Meta:
        model = TestGroupServers
        exclude = ['create_time', 'modify_time']