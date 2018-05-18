#coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.contrib import admin


class CommonConfig(models.Model):
    name = models.CharField('名称', max_length=255)
    value = models.CharField('值', max_length=255)
    comment = models.CharField('说明', max_length=255)
    create_time = models.DateTimeField('创建时间', blank=True, null=True)
    modify_time = models.DateTimeField('修改时间', blank=True, null=True)
    operate_ip = models.CharField('操作人IP', max_length=255, blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'common_config'
        verbose_name = '通用配置'
        verbose_name_plural = '通用配置'


class LoadTestRecord(models.Model):
    status_choices = (
        (0, '未运行'),
        (1, '运行中'),
        (2, '已结束')
    )
    user_count = models.IntegerField('数据总量')
    hatch_rate = models.IntegerField('登陆并发', blank=True, null=True)
    data_struct = models.CharField('数据构成', max_length=255)
    scene_struct = models.CharField('测试场景', max_length=255)
    total_rps = models.FloatField('ToalRps')
    fail_ratio = models.FloatField('失败率', blank=True, null=True)
    status = models.IntegerField('状态', choices=status_choices)
    start_time = models.DateTimeField('开始时间', blank=True, null=True)
    end_time = models.DateTimeField('结束时间', blank=True, null=True)
    stats = models.TextField("压测详细记录", blank=True, null=True)
    exceptions = models.TextField("压测异常", blank=True, null=True)

    def __str__(self):
        s = "{0} - {1}|total:{2}|concurrency:{3}"
        return s.format(self.start_time, self.end_time, self.user_count, self.hatch_rate)

    class Meta:
        db_table = 'load_test_record'
        verbose_name = '压测记录管理'
        verbose_name_plural = '压测记录管理'
        ordering = ['-start_time']

class CommonConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'comment']
    exclude = ('operate_ip',)

class LoadTestRecordAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'status', 'user_count', 'hatch_rate', 'total_rps']
    list_filter = ['status', 'start_time']
    list_per_page = 20
    empty_value_display = '-None-'


class SvcLoadClient(models.Model):
    client_ip = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    slave_count = models.IntegerField()
    create_time = models.DateTimeField(blank=True, null=True)
    modify_time = models.DateTimeField(blank=True, null=True)
    operate_ip = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'svc_load_client'

class SvcLoadClientForm(ModelForm):
    class Meta:
        model = SvcLoadClient
        fields = ['client_ip', 'role', 'status', 'slave_count']


class AutoTestRecord(models.Model):
    status_choices = (
        (0, '失败'),
        (1, '运行中'),
        (2, '已结束'),
        (3, '已终止')
    )
    job_name = models.CharField('Job名称', max_length=255)
    build_no = models.IntegerField('Build.No')
    total_executed = models.IntegerField('已执行')
    success_count = models.IntegerField('成功数', blank=True, null=True)
    error_count = models.IntegerField('错误数', blank=True, null=True)
    failure_count = models.IntegerField('失败数', blank=True, null=True)
    status = models.IntegerField('状态', choices=status_choices)
    start_time = models.DateTimeField('开始时间', blank=True, null=True)
    end_time = models.DateTimeField('结束时间', blank=True, null=True)
    report_url = models.CharField('测试报告路径', max_length=255, blank=True, null=True)
    fail_info = models.TextField('case失败详细信息', blank=True, null=True)
    error_info = models.TextField('case错误详细信息', blank=True, null=True)

    def __str__(self):
        return "{}-{}-{}".format(self.job_name, self.start_time, self.end_time)

    class Meta:
        db_table = 'auto_test_record'
        verbose_name = 'CI测试记录管理'
        verbose_name_plural = 'CI测试记录管理'
        ordering = ['-start_time']

class AutoTestRecordForm(ModelForm):
    class Meta:
        model = AutoTestRecord
        fields = '__all__'

class AutoTestRecordAdmin(admin.ModelAdmin):
    list_display = ['job_name', 'start_time', 'end_time', 'status', 'success_count', 'failure_count', 'error_count']
    list_filter = ['status', 'start_time']
    list_per_page = 20
    empty_value_display = '-None-'