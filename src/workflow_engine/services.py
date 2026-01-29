# workflow_engine/services.py
from staffing.services import get_superior_by_rank, get_employees_for_position
from .models import ApprovalMatrix

def move_project_to_next_step(project):
    """
    Docstring for move_project_to_next_step
    
    :param project: Description
    """
    # 1. Get the rule for the next step
    next_rule = ApprovalMatrix.objects.filter(
        stage=project.current_stage,
        step_number=project.current_step + 1
    ).first()

    if not next_rule:
        # No more steps? The project is fully approved!
        project.is_finalized = True
        project.save()
        return None
    
    # 2. Find the boss in the heirarchy who matches the requred rank
    target_position = get_superior_by_rank(
        current_position=project.submitted_by.position,
        target_rank=next_rule.requred_rank_level
    )

    # 3. Update the project with the new "Owner"
    project.assigned_to_position = target_position
    project.current_step += 1
    project.save()

    # 4. Return the employees so the Notificaion App can ping them
    return get_employees_for_position(target_position, asset=project.asset)