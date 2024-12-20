import os

from users.tasks import setup_schedule

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panda_records_api.settings")

from django_q.management.commands.qcluster import Command as QClusterCommand


class Command(QClusterCommand):

    def handle(self, *args, **kwargs):
        setup_schedule()
        super().handle(*args, **kwargs)
