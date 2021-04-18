"""
Applications can register their own actions with manage.py.
For example, you might want to add a manage.py
action for a Django app that you’re distributing.
"""
import time

from django.core.management import BaseCommand
from django.db.utils import OperationalError
from django.db import connections


class Command(BaseCommand):
    """Django command to pause execution until database is availible"""

    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write("Waiting for DB ...")  # write to user
        db_con = None
        while not db_con:
            try:
                db_con = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second ...')
                time.sleep(1)
                # we mocked it test that it would NOT be sleeping
        #         But it practise it would wait a second

        self.stdout.write(self.style.SUCCESS('Database available'))
