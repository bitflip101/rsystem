from django.contrib import admin
from .models import Asset, OrgUnit

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    # list_display = ('name', 'region', 'get_status')
    list_display = ('get_name_display', 'description')

@admin.register(OrgUnit)
class OrgUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_type', 'asset', 'parent', 'code')
    list_filter = ('unit_type', 'asset')
    search_fields = ('name', 'code')
