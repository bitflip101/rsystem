from django.contrib import admin
from .models import Employee, Position
from django.contrib.admin import SimpleListFilter
from core_org.models import Asset


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'org_unit', 'rank_level', 'reports_to')
    list_filter = ('rank_level', 'org_unit')
    search_fields = ('title',)

class PositionInLine(admin.TabularInline):
    model = Position
    extra = 1 # Provide 1 empty row to quickly add a title/rank
    fields = ('title', 'rank_level', 'is_unit_head')

class AssetFilter(SimpleListFilter):
    title = 'Asset' # The label shown on the right
    parameter_name = 'asset' # The URL parameter

    def lookups(self, request, model_admin):
        # This creates the list of assets to click on
        return [(asset.id, asset.name) for asset in Asset.objects.all()]
    
    def queryset(self, request, queryset):
        # This tells Django how to filter the Employees
        if self.value():
            return queryset.filter(position__org_unit__asset_id=self.value())
        return queryset

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'get_asset', 'get_status')

    # list_filter = ('user__is_active', 'position__org_unit__asset')

    ## Use the custom filter class here instead of the string path
    list_filter = ('user__is_active', AssetFilter)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    # Method to show if the linked User is active
    @admin.display(boolean=True, description='Active')
    def get_status(self, obj):
        return obj.user.is_active

    # Method to show the Asset name
    @admin.display(description='Asset')
    def get_asset(self, obj):
        if obj.position and obj.position.org_unit:
            return obj.position.org_unit.asset
        return "Unassigned"