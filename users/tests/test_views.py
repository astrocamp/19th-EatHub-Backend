from django.test import TestCase
from django.db import connection

class DatabaseConnectionTest(TestCase):
    def test_connection(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
            self.assertEqual(row[0], 1)
