import sqlite3


class DatabaseHandler:

    """
    A very simple database handler designed for the task

    Attributes
    ----------

    self.__path : str
        The path to the database

    self.__connection : object
        The connection to the database if one has been created

    """

    def __init__(self, path):
        """
        The constructor for the class
        :param path: The path to the database (Database will be created if it doesn't exist)
        """
        self.__path = path
        self.__connection = None


    def select_all_entries(self):
        """
        A simple method that allows us to select an entire table
        :return: Returns all the rows of a table
        """
        cursor = self.__connection.cursor()
        cursor.execute("SELECT * FROM entry_lists")
        rows = cursor.fetchall()
        return rows


    def insert_entry(self, entry):
        """
        A simple method that allows use to insert data into the table (Format: (List, Order, ESTime))
        :param entry: The entry as a tuple that's to be inserted
        :return: Returns the class for method chains
        """
        cursor = self.__connection.cursor()
        insert_list_query = "INSERT INTO entry_lists (sorted_list, asc, es_time) VALUES (?, ?, ?)"
        cursor.execute(insert_list_query, entry.get_data_tuple(True))
        return self


    def create_connection(self):
        """
        A simple method to create the database and table
        :return: Returns the class itself for method chains
        """
        self.__connection = sqlite3.connect(self.__path)
        cursor = self.__connection.cursor()

        # A simple create query that auto-increments our primary key for convenience
        create_table_query = "CREATE TABLE IF NOT EXISTS entry_lists ( id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                                    "sorted_list STRING NOT NULL, asc INTEGER NOT NULL, es_time REAL NOT NULL )"

        # We execute the query and return the class
        cursor.execute(create_table_query)
        return self


    def commit(self):
        """
        A simple method that commits all executable querys at the end of a method chain
        :return: Returns the active connection
        """
        self.__connection.commit()
        return self.__connection
