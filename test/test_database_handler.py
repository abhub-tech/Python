import unittest
import os
from src.database_handler import DatabaseHandler
from src.custom_CSV_entry import CustomCSVEntry


class TestDatabaseHandler(unittest.TestCase):

    def setUp(self):
        if os.path.exists("test_list_entries.db"):
            os.remove("test_list_entries.db")


    def test_create_connection(self):
        instance_database_handler = DatabaseHandler("test_list_entries.db")
        connection = instance_database_handler.create_connection().commit()

        cursor = connection.cursor()
        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='entry_lists'")

        expected_output = 1
        actual_outcome = cursor.fetchone()[0]
        self.assertEqual(actual_outcome, expected_output)


    def test_insert_entry(self):

        instance_database_handler = DatabaseHandler("test_list_entries.db")
        connection = instance_database_handler.create_connection().commit()

        instance_custom_csv_entry = CustomCSVEntry()
        instance_custom_csv_entry.create_entry_from_tuple((0, "1, 2, 3, 4", False, 100))
        instance_database_handler.insert_entry(instance_custom_csv_entry).commit()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM entry_lists")

        expected_outcome = [(1, '1,2,3,4', 0, 100.0)]
        actual_outcome = cursor.fetchall()
        self.assertEqual(actual_outcome, expected_outcome)


    def test_select_all(self):

        instance_database_handler = DatabaseHandler("test_list_entries.db")
        connection = instance_database_handler.create_connection().commit()

        instance_custom_csv_entry = CustomCSVEntry()
        instance_custom_csv_entry.create_entry_from_tuple((0, "1, 2, 3, 4", False, 100))
        instance_database_handler.insert_entry(instance_custom_csv_entry).commit()
        instance_database_handler.insert_entry(instance_custom_csv_entry).commit()
        instance_database_handler.insert_entry(instance_custom_csv_entry).commit()

        cursor = connection.cursor()
        cursor.execute("SELECT count(id) FROM entry_lists")

        expected_outcome = 3
        actual_outcome = cursor.fetchone()[0]
        self.assertEqual(actual_outcome, expected_outcome)