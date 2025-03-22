from abc import ABC, abstractmethod
import sqlite3

# Abstract Classes 
class AbstractDatabase(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

# Interfaces
class I_CommonSelectQueries(ABC):
    @abstractmethod
    def execute_simple_select_query(self, table_name:str, fields:list[str]) -> list:
        pass

class I_CommonTableQueries(ABC):
    @abstractmethod
    def create_table(self, table_name:str, fields:list[str]) -> None:
        pass


# Classes
class Database(AbstractDatabase):
    def __init__(self, database_name:str) -> None:
        """
            Creates an object of Database type, connecting to a simple SQLite3 database.

            Attributes:
                - database_name (str): Name of the database.
        """
        self.__database_name = database_name
        self.__conn = sqlite3.connect(f'{self.__database_name}.db')

    @property
    def database_name(self) -> str:
        return self.__database_name
    
    @property
    def conn(self) -> object | None:
        return self.__conn

    def close(self):
        """
            Closes database connection.
        """ 
        self.conn.close()

class Cursor():
    def __init__(self, database_object:Database) -> None:
        """
            Creates a cursor object in base of the received database_object as parameter.

            Attributes:
                - database_object (Database): Database connection object to create the cursor.
        """
        self.database = database_object
        self.__cursor = self.database.__conn.cursor()

    @property
    def cursor(self) -> object:
        return self.__cursor
    
    def execute_query(self, query:str) -> list | None:
        """
            The Cursor object executes an SQL query that the user will pass as str, for example 'SELECT * FROM Users WHERE age > 21'.

            Attributes:
                - query (str): The query that will be executed, it can be of any type (SELECT, UPDATE, DELETE, INSERT, etc.).
        """
        try:
            result = self.cursor.execute(query)
            print('Query was executed.')
            return result.fetchall() if result else []
        except Exception as e:
            print('Impossible to execute the query:', e)
            return None 
    
# Custom cursor for most common queries execution.
class CustomCursor(Cursor, I_CommonTableQueries, I_CommonSelectQueries):
    def __init__(self, database_object:Database):
        super().__init__(database_object)

    def execute_query(self, query:str):
        """
            Executes a simple query of any type wether SELECT, INSERT, CREATE TABLE, DELETE, etc.
            This method leverages its class's parent class method with the same name, behavior and attributes.

            Attributes:
                - query (str): The query that will be executed.
        """
        return super().execute_query(query)
    
    def execute_simple_select_query(self, table_name:str, fields:list[str]) -> list:
        """
            Executes a simple query of SELECT type with the fields to show provided as parameters and the name of the table.
        
            Attributes:
                - table_name (str): Name of the table from where data is going to be obtained.
                - fields (list[str]): List of fields to fetch from the database's table.

            Return:
                - data (list): List of rows obtained from the SELECT query in str format.
        """
        query = f"""SELECT {', '.join(fields)} FROM {table_name};"""
        data = self.execute_query(query)
        return data
    
    def create_table(self, table_name:str, fields:list[str]) -> None:
        """
            Creates a table on the database based on the provided fields and table name.

            Attributes:
                - table_name (): Name of the table that is going to be created.
                -fields (list): List of the table fields in string format. 
            
            Return:
                - None
        """
        
        # Format the fields from fields list in a single string
        formated_fields = ', '.join(fields)
        
        query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({formated_fields})"""
        self.execute_query(query)

    def insert_rows(self, table_name:str, fields:list[str], values:list[list[str]]) -> bool:
        """
            Executes a classic INSERT query receiving the name of the fields matching the values to insert and the name of the table
            This method iterates over every row on the provided list of values to make an insertion on the database in the table..

            Attributes:
                - table_name (str): Name of the table where the data will be inserted as a new row.
                - fields (list[str]): List of fields to determine which type of data should be inserted.
                - values (list[list[str]]): List of rows to insert, every row is a list of every value in the desired format.  

            Return:
                - succes (str): True if rows were inserted. False if it was not possible to insert rows.
        """
        formated_fields = ', '.join(fields)
        rows_list = values
        for row in rows_list:
            try:
                formated_values = ', '.join(f"'{value}'" for value in row)
                query = f"""INSERT INTO {table_name} ({formated_fields}) VALUES({formated_values});"""
                self.execute_query(query)
            except Exception as e:
                print(f'Error during inserting data into database on table {table_name}:', e)
                succes = False
        succes = True
        return succes