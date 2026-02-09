from django.contrib import admin
from .models import ApprovalLog, ApprovalMatrix

@admin.register(ApprovalMatrix)
class ApprovalMatrixAdmin(admin.ModelAdmin):
    list_display = ('stage', 'step_number', 'required_position')
    list_filter = ('stage', 'required_position')

@admin.register(ApprovalLog)
class ApprovalLogAdmin(admin.ModelAdmin):
    list_display  = ('project', 'approver', 'action', 'timestamp')
    list_filter = ('action', 'timestamp',)
    readonly_fields = ('timestamp',)
