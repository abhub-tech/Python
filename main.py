# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
from src.database_handler import DatabaseHandler
from src.custom_CSV_entry import CustomCSVEntry


def main():

    instance_database_handler = DatabaseHandler("list_entries.db")
    instance_database_handler.create_connection().commit()
    main_menu(instance_database_handler)

def main_menu(instance_database_handler):
    """
    This function prints out the main menu and allows option selection
    :param instance_database_handler: The database handler needed for SqLite communication
    :return: None
    """

    print("#-------------------------------------------------#")
    print("Welcome to the simple data sorter")
    print("#-------------------------------------------------#")
    print("1) Input CSV entry")
    print("2) View CSV Records")
    print("#-------------------------------------------------#")
    cleaned_selection = clean_str(input("Select option (1 or 2): "))
    print("#-------------------------------------------------#")

    # Selection 1 moves to the input screen
    if cleaned_selection == "1":
        manual_csv_input(instance_database_handler)

    # Selection 2 moves to the view screen
    elif cleaned_selection == "2":
        view_all_records(instance_database_handler)

    # If no screens are selected we ask them if they'd like to exit
    else:
        wants_to_exit = input("Would you like to exit? (Y/N): ")
        leaned_selection = clean_str(wants_to_exit)
        if leaned_selection == "n":
            main_menu(instance_database_handler)


def view_all_records(instance_database_handler):
    """
    This method allows the viewing of all records that have been entered
    :param instance_database_handler: The database handler needed for SqLite communication
    :return None
    """

    # We run a simple query to select all the database rows
    # These rows are converted into entries and printed neatly
    database_table_rows = instance_database_handler.select_all_entries()
    for row in database_table_rows:
        instance_custom_CSV_entry = CustomCSVEntry()
        instance_custom_CSV_entry.create_entry_from_tuple(row)
        print(instance_custom_CSV_entry)


    # Once all records have been shown, there's an option to export them all to JSON
    selection = clean_str(input("Would you like to export records as JSON? (Y/N): "))
    if selection == "y":
        raw_file_name = input("Enter file name: ")
        full_file_name = clean_str((raw_file_name + ".json"))
        export_to_json(database_table_rows, full_file_name)
        print("JSON file saved (Name: " + full_file_name + ")")


    # Finally we return to the main menu
    main_menu(instance_database_handler)


def export_to_json(database_table_rows, filename):
    """
    A simple method that exports all the sorts to JSON
    :param database_table_rows: The database rows we want to export
    :param filename: The name of the file to be saved
    """

    # Simply we build a dict
    raw_json = {}
    for row in database_table_rows:
        entry_id = str(row[0])
        raw_json[entry_id] = row[1]

    # Then covert the dict into a JSON and write it to the disk
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(raw_json))


def manual_csv_input(instance_database_handler, instance_custom_CSV_entry=CustomCSVEntry()):
    """
    The method that allows data to be entered in an CSV format
    :param instance_database_handler:  The database handler, the class that allows select and insertions into the database
    :param instance_custom_CSV_entry: The current entry
    :return: None
    """
    try:
        # We prompt the user to enter in a valid CSV list
        str_raw_csv_input = input("Enter valid Integer values in an CSV format (1, 2, ..., n): ")
        instance_custom_CSV_entry.raw_csv_input(str_raw_csv_input)
        if instance_custom_CSV_entry.get_list_size() <= 1:
            raise ValueError("A list must contain at least two items")


        # We ask them which order they'd like, by default its sorted into ascending.
        # If they enter Y we sort the list into descending order, if the value isn't an N, there's been an error
        descending = False
        str_sort_order = input("(Default: Ascending) Change sort order to descending? (Y/N): ")
        str_cleaned_sort_order = clean_str(str_sort_order)
        if str_cleaned_sort_order == "y":
            descending = True
        elif str_cleaned_sort_order != "n":
            raise ValueError()


        # The entry is sorted and inserted into the database
        instance_custom_CSV_entry.initiate_sort(descending)
        instance_database_handler.insert_entry(instance_custom_CSV_entry).commit()
        print("Success! (", instance_custom_CSV_entry, ")")

    except ValueError as value_error:
        # We simply print the error
        print("Values that were inputted were not correct: ", value_error)


    finally:
        # Finally we ask them if they want to insert a new entry, if so, we start the process again
        # If any other value is selected we return to the main menu
        str_input = input("Submit new entry (Y/N)?")
        if str_input.lower() == "y":
            manual_csv_input(instance_database_handler)
        else:
            main_menu(instance_database_handler)


def clean_str(str_value):
    """
    A simple method used to clean strings
    :param str_value: The string we want to format
    :return: Returns the cleaned string
    """
    cleaned_str_value = str_value.replace(" ", "").lower()
    return cleaned_str_value


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
