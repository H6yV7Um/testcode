from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CommonConfig, CommonConfigAdmin)
admin.site.register(LoadTestRecord, LoadTestRecordAdmin)
admin.site.register(AutoTestRecord, AutoTestRecordAdmin)

