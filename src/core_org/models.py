from django.db import models

class Asset(models.Model):
    REGION_CHOICES = [
        ('NORTH', 'North Asset'),
        ('SOUTH', 'South Asset'),
        ('EAST', 'East Asset'),
        ('WEST', 'West Asset'),
        ('NORTHEAST', 'NorhtEast Asset'),
    ]
    name = models.CharField(max_length=50, choices=REGION_CHOICES, unique=True)
    description = models.TextField(blank=True)

    # Adding this line to make the 'Status' column in Admin work!
    is_active = models.BooleanField(default=True)

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
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='units', null=True, blank=True)
    # The parent link creates the heirarchy (e.g., Division's parent is Departent)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_units')
    code = models.CharField(max_length=20, unique=True) # e.g., DRL-OFFSHORE

    def __str__(self):
        # Show which Asset it belongs to
        asset_prefix = f"[{self.asset.name}]" if self.asset else ""
        return f"{asset_prefix}{self.name} ({self.get_unit_type_display()})" 
