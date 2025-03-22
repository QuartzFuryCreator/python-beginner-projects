from abc import ABC, abstractmethod
import sqlite3

# Abstract Classes 
class AbstractDatabase():
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

# Interfaces
class I_CustomSelectQuery:
    def execute_simple_select_query(self, table_name:str, fields:list[str]) -> list:
        pass


# List of Inerfaces
INTERFACES:list = [I_CustomSelectQuery]


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
        
        def connect(self):
            """
                Connects to a SQLite3 database.
            """
            self.conn.connect()

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
                result = self.cusor.execute(query)
            except Exception as e:
                print('Impossible to fetch result data:', e)
            finally:
                self.cursor.execute(query)

            if result:
                print('Database query sucessfully executed!')
                return result
            print('Not result obtained from the database query execution, but it worked sucessfully!')
            return None 