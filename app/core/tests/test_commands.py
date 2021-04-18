from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is availible"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # this means whatever django.db.utils.ConnectionHandler.__getitem__
            # during tests execution just return true
            gi.return_value = True
            call_command('wait_for_db')

            self.assertEqual(gi.call_count, 1)

    # replace the behaviour of time.sleep and just returns true
    # just to speed up the test
    # by default django would wait a second to reconnect
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # Add side affect
            # Raise Operational error 5 times
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 6)
