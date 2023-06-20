from django.contrib import admin
from .models import MainOrders, SecondOrdersModel, StatisticDataSet
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register(MainOrders, ImportExportModelAdmin)
admin.site.register(SecondOrdersModel, ImportExportModelAdmin)
admin.site.register(StatisticDataSet)
