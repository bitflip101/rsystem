from django.db import models
from staffing.models import Position
import uuid
from django.conf import settings 
from core_org.models import Asset

class Well(models.Model):
    """The permanent physical asset record"""
    uwi = models.CharField("Unique Well Identifier", max_length=50, unique=True)
    well_name = models.CharField(max_length=100)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    field_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.well_name} ({self.uwi})"

class WellProject(models.Model):
    """The 'WORK ITEM' that moves through the SAP-like routing"""

    STAGE_CHOICES = [
        ('EXPLORE', 'Exploration'),
        ('DRILL', 'Drilling'),
        ('COMPLETE', 'Completion'),
        ('PROD', 'Production'),
        ('ABANDON', 'Abandonment'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('REVIEW', 'In Review/Approval'),
        ('APPROVED', 'Approved/Active'),
        ('ON_HOLD', 'On Hold'),
        ('CLOSED', 'Completed/Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(Well, on_delete=models.CASCADE, related_name='projects')
    project_type = models.CharField(max_length=20, choices=STAGE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    # The 'Current Owner' Logic
    # This is the Position currently responsible for teh next approval
    # name = models.CharField(max_length=200)
    current_stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='EXPLORATION')
    assigned_to_position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name='pending_projects')

    # Ownership & Timing
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(help_text="The date by which current approval step is due")
     
    # Financial (Classic O&G requirements)
    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.project_type} - {self.well.well_name}"

    