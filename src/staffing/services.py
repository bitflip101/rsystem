# staffing/services.py
from .models import Position, Employee

def get_superior_by_rank(current_position, target_rank):
    """
    Docstring for get_superior_by_rank
    
    :param current_position: Description
    :param target_rank: Description
    """
    cursor  = current_position

    # Going to climb the 'reports_to' tree
    while cursor is not None:
        if cursor.rank_level >= target_rank:
            return cursor
        cursor = cursor.reports_to

    return None # Hit the top of the company without finding the rank

def get_employees_for_position(position, asset=None):
    """
    Docstring for get_employees_for_position
    
    :param position: Description
    :param asset: Description
    """
    queryset = Employee.objects.filter(position=position, is_active=True)
    if asset: 
        queryset = queryset.filter(position__org_unit__asset=asset)
    return queryset