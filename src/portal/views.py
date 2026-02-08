from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from well_assets.models import WellProject
from django.utils import timezone

def home_view(request):
    # Default context for guests
    context = {
        'is_guest': True,
    }
    if request.user.is_authenticated:
        context['is_guest'] = False

        # Assuming that every logged-in user has an Employee profile
        # tied to a position and an asset (from staffing/core_org_apps)
        try:
            employee = request.user.employee
            user_position = employee.position
            user_asset = user_position.org_unit.asset

            # 1. Get the Work Queue count for THIS position and asset
            pending_query = WellProject.objects.filter(
                assigned_to_position=user_position,
                well__asset=user_asset,
                status='IN_PROGRESS'
            )

            context['pending_count'] = pending_query.count()

            # 2. Get Overdue items (Teaser for the table)
            context['overdue_projects'] = pending_query.filter(
                due_date__lt=timezone.now()
            ).order_by('due_date')[:5] # Just show 5 items

        except AttributeError:
            # Handle cases where a User exists but hasn't been assigned to a position/Employee profile yet.
            context['pending_count'] = 0
            context['error_message'] = "Profile incomplete. Please contact Support."
    tn = "portal/home.html"        
    return render(request,tn,context)