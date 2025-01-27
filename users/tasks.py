from datetime import timedelta

from django.utils import timezone
from django_q.models import Schedule
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


def blacklist_cleanup() -> None:
    expiration_time = timezone.now() - timedelta(days=10)
    BlacklistedToken.objects.filter(blacklisted_at__lt=expiration_time).delete()

def setup_schedule() -> None:
    if not Schedule.objects.filter(func="users.tasks.blacklist_cleanup").exists():
        Schedule.objects.create(
            func="users.tasks.blacklist_cleanup",
            schedule_type=Schedule.MONTHLY,
            repeats=-1,
            name="Monthly Blacklist Cleanup",
        )
