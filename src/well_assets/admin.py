from django.contrib import admin
from .models import Well, WellProject

@admin.register(Well)
class WellAdmin(admin.ModelAdmin):
    list_display = ('well_name', 'uwi', 'asset', 'field_name')
    search_fields = ('well_name', 'uwi')

@admin.register(WellProject)
class WellProjectAdmin(admin.ModelAdmin):
    list_display = ('well', 'project_type', 'status', 'assigned_to_position', 'due_date')
    list_filter = ('status', 'project_type', 'well__asset')
    # This will make the  well selection much faster if there are 10,000 wells
    raw_id_fields = ('well',)
