import time
from timeit import default_timer as timer

class CustomCSVEntry:
    """
    A class used for a custom CSV entry (very close to the built methods)

    Attributes
    ----------
    self.__sort_estime : float
        The elapsed sort time

    self.__int_entry_list : list
        The list of int values

    self.__descending_order : bool
        The flag to indicate the order of the list (default: ascending)
    """

    def __init__(self):
        """
        The constructor of the class takes no input
        """
        self.__sort_estime = None
        self.__int_entry_list = None
        self.__descending_order = None


    def create_entry_from_tuple(self, entry_tuple):
        """
        Method can be used to construct the entry in a none-default way
        :param entry_tuple: (0: The list of ints, 1: The order of the list, 3: Time taken to sort)
        :return: Return the class (self) for method chains
        """
        self.__int_entry_list = self.raw_csv_input(entry_tuple[1])
        self.__descending_order = True if entry_tuple[2] == 1 else False
        self.__sort_estime = entry_tuple[3]
        return self


    def initiate_sort(self, descending=False):
        """
        This method is used to sort the list of ints
        :param descending: A flag to indicate the order (Default: ascending)
        :return: Return the sorted list, the time taken, and the current order
        """

        # We capture the start time, then sort the list with the default method, then capture the end
        s_time = timer()
        self.__int_entry_list.sort(reverse=descending)
        e_time = timer()

        # The time taken is calculated by taking the start time (s_time), substract it from the end time (e_time)
        # the time taken is then converted into milliseconds and round to five decimal places
        self.__sort_estime = self._convert_time_to_milliseconds(s_time, e_time)

        # Finally  we denote the order, and return all modified values for testing purposes
        self.__descending_order = descending
        return self.__int_entry_list, self.__sort_estime, self.__descending_order


    def _convert_time_to_milliseconds(self, s_time, e_time):
        """
        A simple helper method that calculates elapsed time, and coverts it into milliseconds
        :param s_time: The start time in nanoseconds since last epoch
        :param e_time: The end time in nanoseconds since last epoch
        :return: Returns the elapsed time in milliseconds
        """
        return round((e_time - s_time) * 1000, 5)


    def raw_csv_input(self, str_raw_csv_input):
        """
        This method accepts a CSV string, known as the raw input.
        :param str_raw_csv_input: A string of comma separated values (1, 2, ..., n)
        :return: Returns the list of converted strings
        """

        # The raw input is stripped of white space and split via the commas
        str_cleaned_csv_input_list = str_raw_csv_input.strip().split(",")

        # Common mistakes such as multi-commas and blank strings are removed.
        str_filtered_csv_input_list = list(filter(lambda entry: "," not in entry and entry != "''" and entry != "" and entry, str_cleaned_csv_input_list))

        # All of the valid inputs that remain are converted into ints (NOTE: Caller should catch ValueError expectations)
        self.__int_entry_list = list(map(int, str_filtered_csv_input_list))
        return self.__int_entry_list


    def entry_list_to_string(self):
        """
        This method is used to convert the list of ints back into strings
        :return: Returns a list of str based numbers separated by commas
        """
        return ",".join(str(item) for item in self.__int_entry_list)


    def get_data_tuple(self, str=False):
        """
        Returns the attributes of the class as a tuple
        :param str: If true, it converts the list of ints into strings
        :return: Returns a tuple of all the class attributes
        """
        return (self.entry_list_to_string(), self.__descending_order, self.__sort_estime) if str else \
            (self.__int_entry_list, self.__descending_order, self.__sort_estime)

    def get_list_size(self):
        """
        A simple method that returns the size of the list
        :return: Returns list size
        """
        return len(self.__int_entry_list)

    def get_data_dict(self, str=False):
        """
        Returns all the class attributes as a dict
        :param str: If true, it converts the list of ints into strings
        :return: Returns a dict of the class
        """
        return { "descending": self.__descending_order, "es_time": self.__sort_estime,
                 "entries": self.entry_list_to_string() if str else self.__int_entry_list }

    def set_int_list(self, int_list):
        """
        A simple setter function that allows the assignment to the int list
        :param int_list: The set of new values
        :return: None
        """
        self.__sort_estime = None
        self.__descending_order = None
        self.__int_entry_list = int_list


    def __str__(self):
        """
        A simple override for display
        :return: Returns a formatted string of all attribute values
        """
        return "Descending: {}, ESTime: {}, List: {}".\
            format(self.__descending_order, self.__sort_estime, self.entry_list_to_string())