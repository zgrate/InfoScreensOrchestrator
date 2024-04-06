from pydoc import Helper

from django.contrib import admin

from helpermonitor.models import HelperModel, HelperDutyTimeModel, HelperDutyCategoryModel

# Register your models here.
admin.site.register(HelperModel)
admin.site.register(HelperDutyTimeModel)
admin.site.register(HelperDutyCategoryModel)