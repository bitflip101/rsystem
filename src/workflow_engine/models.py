from django.db import models
from well_assets.models import WellProject
from staffing.models import Position, User

class ApprovalMatrix(models.Model):
    """
    Docstring for ApprovalMatrix
    """
    stage = models.CharField(max_length=20, choices=WellProject.STAGE_CHOICES)
    step_number = models.IntegerField()
    required_position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        ordering = [
        'stage', 'step_number'
        ]
        unique_together = ('stage', 'step_number')

class ApprovalLog(models.Model):
    project = models.ForeignKey(WellProject, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.PROTECT)
    action = models.CharField(max_length=20) # Approved, Rejected, Modified
    comments = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
