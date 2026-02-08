from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from well_assets.models import WellProject
from staffing.models import Employee

@shared_task
def process_project_reminders():
    now = timezone.now()

    # 1. Find the Projects in the "WARNING ZONE" (Due in the next 24hrs)
    warning_window = now + timedelta(hours=24)
    upcoming_projects = WellProject.objects.filter(
        status='IN_PROGRESS',
        due_date__lte=warning_window,
        due_date__gt=now
    )

    for project in upcoming_projects:
        send_reminder(project, "GENTLE_REMINDER")

    # 2. Find Projects in the "ESCALATION ZONE" (Past due)
    overdue_projects = WellProject.objects.filter(
        status='IN_PROGRESS',
        due_date__lt=now
    )

    for project in overdue_projects:
        send_reminder(project, "URGENT_ESCALATION")

def send_reminder(project, alert_type):
    # Get the people currently in the assigned position
    recipients = Employee.objects.filter(
        position=project.assigned_to_position,
        is_active=True
    )

    recipient_emails = [emp.user.email for emp in recipients]

    if alert_type == "GENTLE_REMINDER":
        subject = f"Reminder: Approval Due for {project.well.well_name}"
        message = f"The {project.project_type} project is due for review in 24 hours."
        # Logic to trigger email/push notification
        print(f"Sending reminder to {recipient_emails}")

    elif alert_type == "URGENT_ESCALATION":
        # Get the Boss (The hierarchical escalation)
        boss_position = project.assigned_to_position.reports_to
        bosses = Employee.objects.filter(position=boss_position, is_active=True)
        boss_emails = [b.user.email for b in bosses]

        subject = f"!!! ESCALATION !!!: {project.well.well_name} is Overdue"
        message = f"Action required by {project.assigned_to_position.title}.Deadline was {project.due_date}."

        # Notify BOTH the asignee and their supervisor
        all_recipients = recipient_emails + boss_emails
        print(f"Escalating to: {all_recipients}")