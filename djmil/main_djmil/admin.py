from django.contrib import admin
from .models import MainOrders
from import_export.admin import ImportExportModelAdmin


class ExportOrders(ImportExportModelAdmin):
    resource_classes = [MainOrders]


# Register your models here.
admin.site.register(MainOrders, ImportExportModelAdmin)
