import unittest
import random
from src.custom_CSV_entry import CustomCSVEntry


class TestCustomCSVEntry(unittest.TestCase):

    def test_raw_csv_input_positive_numbers(self):

        test_input = "1, 2, 3, 4, 5"
        expected_output = [1, 2, 3, 4, 5]

        instance_custom_csv_entry = CustomCSVEntry()
        self.assertEqual(instance_custom_csv_entry.raw_csv_input(test_input), expected_output)

    def test_raw_csv_input_negative_numbers(self):

        test_input = "-3, -4, -5"
        expected_output = [-3, -4, -5]

        instance_custom_csv_entry = CustomCSVEntry()
        self.assertEqual(instance_custom_csv_entry.raw_csv_input(test_input), expected_output)

    def test_raw_csv_input_mixed_numbers(self):

        test_input = "1, 2, 3, -3, -4, -5, 0"
        expected_output = [1, 2, 3, -3, -4, -5, 0]

        instance_custom_csv_entry = CustomCSVEntry()
        self.assertEqual(instance_custom_csv_entry.raw_csv_input(test_input), expected_output)


    def test_raw_csv_input_common_errors(self):

        test_input = ",1,, 2, 3, -3,,, -4, -5, 0,'',1,2"
        expected_output = [1, 2, 3, -3, -4, -5, 0, 1, 2]

        instance_custom_csv_entry = CustomCSVEntry()
        self.assertEqual(instance_custom_csv_entry.raw_csv_input(test_input), expected_output)

    def test_initiate_sort_asc(self):

        test_input = "9, 8, 7, 6, 5, 4, 4, 3, 2, 1"
        expected_output = [1, 2, 3, 4, 4, 5, 6, 7, 8, 9]
        expected_order = False
        expected_estime = 0


        instance_custom_csv_entry = CustomCSVEntry()
        instance_custom_csv_entry.create_entry_from_tuple((0, test_input, None, None))


        actual_list, actual_estime, actual_order = instance_custom_csv_entry.initiate_sort(False)
        self.assertEqual(expected_output, actual_list)
        self.assertGreaterEqual(actual_estime, expected_estime)
        self.assertEqual(expected_order, actual_order)


    def test_initiate_sort_des(self):

        test_input = "1, 2, 3, 4, 4, 5, 6, 7, 8, 9"
        expected_list_output = [9, 8, 7, 6, 5, 4, 4, 3, 2, 1]
        expected_order = True
        expected_estime = 0


        instance_custom_csv_entry = CustomCSVEntry()
        instance_custom_csv_entry.create_entry_from_tuple((0, test_input, None, None))


        actual_list, actual_estime, actual_order = instance_custom_csv_entry.initiate_sort(True)
        self.assertEqual(expected_list_output, actual_list)
        self.assertGreaterEqual(actual_estime, expected_estime)
        self.assertEqual(expected_order, actual_order)

    def test_convert_time_to_milliseconds(self):

        start_time = 1643062274.1299589
        end_time = 1643062274.4850101
        expected_estime = 355

        instance_custom_csv_entry = CustomCSVEntry()
        actual_estime = instance_custom_csv_entry._convert_time_to_milliseconds(start_time, end_time)
        self.assertGreaterEqual(actual_estime, expected_estime)

    def test_large_sort(self):

        random.seed(1)
        test_input = random.choices(range(-9999999, 9999999), k=9999998)
        expected_estime = 0


        instance_custom_csv_entry = CustomCSVEntry()
        instance_custom_csv_entry.set_int_list(test_input)

        actual_list, actual_estime, actual_order = instance_custom_csv_entry.initiate_sort(True)
        self.assertGreaterEqual(actual_estime, expected_estime)
