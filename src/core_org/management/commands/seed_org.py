from django.core.management.base import BaseCommand
from core_org.models import Asset, OrgUnit
from staffing.models import Position

class Command(BaseCommand):
    help = "Seed the initial Org Structure"

    def handle(self, *args, **options):
        ## 1. Create Asset
        asset, _ = Asset.objects.get_or_create(name='NORTH', defaults={'description': 'North Sea Operations'})

        ## 2. Create high-level Org Unit
        corp, _ = OrgUnit.objects.get_or_create(
            code='CORP-01',
            defaults={'name': 'Corporate HQ','unit_type': 'CORP', 'asset': asset}
        )

        ## 3. Create a Department
        drl_dept, _ = OrgUnit.objects.get_or_create(
            code='DRL_OPS',
            defaults={'name': 'Drilling Operations', 'unit_type': 'DEPT', 'asset': asset}
        )
        
        ## 4. Create Standard Positions
        positions = [
            {'title': 'VP Operations', 'rank': 10, 'is_head':True, 'unit': corp},
            {'title': 'Drilling Manager', 'rank': 8, 'is_head':True, 'unit': drl_dept},
            {'title': 'Superintendent', 'rank': 6, 'is_head':False, 'unit': drl_dept},
            {'title': 'Driller', 'rank': 2, 'is_head':False, 'unit': drl_dept},

        ]

        for p in positions:
            Position.objects.get_or_create(
                title=p['title'],
                org_unit=p['unit'],
                defaults={'rank_level': p['rank'], 'is_unit_head':p['is_head']}
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded R-System Org Structure'))