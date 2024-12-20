from django_q.models import Schedule
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


def blacklist_cleanup() -> None:
    BlacklistedToken.objects.all().delete()

def setup_schedule() -> None:
    if not Schedule.objects.filter(func="users.tasks.blacklist_cleanup").exists():
        Schedule.objects.create(
            func="users.tasks.blacklist_cleanup",
            schedule_type=Schedule.MINUTES,
            repeats=-1,
            name="Weekly Blacklist Cleanup",
        )
