from django.db import models

class Asset(models.Model):
    REGION_CHOICES = [
        ('NORTH', 'North Asset'),
        ('SOUTH', 'South Asset'),
        ('EAST', 'East Asset'),
    ]
    name = models.CharField(max_length=50, choices=REGION_CHOICES, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()
    
# Update OrgUnit to be Asset-aware
class OrgUnit(models.Model):
    UNIT_TYPES = [
        ('CORP', 'Corporate/Executive'),
        ('DEPT', 'Department'),
        ('DIV', 'Division'),
        ('GROUP', 'Group/Unit'),
    ]

    name = models.CharField(max_length=255)
    unit_type = models.CharField(max_length=10, choices=UNIT_TYPES)
    # The parent link creates the heirarchy (e.g., Division's parent is Departent)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_units')
    code = models.CharField(max_length=20, unique=True) # e.g., DRL-OFFSHORE

    def __str__(self):
        return f"{self.name} ({self.get_unit_type_display()})" 
