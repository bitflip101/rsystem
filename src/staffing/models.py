from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100) # e.g., "Exploration, Reservoir"
    code = models.CharField(max_length=10, unique=True) # e.g., "EXPL", "RESR", "DRLG"
    def __strt__(self):
        return self.name

class Position(models.Model):
    RANK_CHOICES = [
        (10,'Executive (Sr.VP / VP)'),
        (8, 'Director'),
        (6, 'Manager'),
        (4, 'Supervisor/Lead'),
        (2, 'Technical/Staff'),
    ]
    title = models.CharField(max_length=100) # e.g., "Offshore Drilling Manager"
    org_unit = models.ForeignKey(OrgUnit, on_delete=models.CASCADE, related_name='positions')
    reports_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    rank_level = models.IntegerFiel(choices=RANK_CHOICES)

    # THishelps find the "HEAD" fo a unit automatically
    is_unit_head = models.BooleanField(default=False)
    # department = models.ForeignKey(Department, on_delete=models.CASCADE)
    # reports_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    # level = models.IntegerField(default=1) # 1=Foreman, 5=VP, so-on..

    def __str__(self):
        return f"{self.title} ({self.org_unit.code})"
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    # Delegation: if John is away, Sarah can approve on this behalf.
    delegate = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    @property
    def current_approver(self):
        return self.delegate if self.delegate else self
