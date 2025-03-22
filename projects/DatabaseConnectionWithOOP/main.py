from . classes import Cursor, Database
from . classes import INTERFACES

# Custom cursor for most common queries execution.
class CustomCursor(Cursor, INTERFACES.I_CustomSelectQuery):
    def __init__(self, database_object:Database):
        super().__init__(database_object)

    def execute_query(self, query:str):
        """
            Executes a simple query of any type wether SELECT, INSERT, CREATE TABLE, DELETE, etc.
            This method leverages its class's parent class method with the same name, behavior and attributes.

            Attributes:
                query (str): The query that will be executed.
        """
        super().execute_query(query)
    
    def execute_simple_select_query(self, table_name:str, fields:list[str]) -> list:
        table_name = table_name
        fields = fields
        query = f"""SELECT {[field for field in fields]} FROM {table_name};"""
        data = self.execute_query(query)
        return data
    
    def create_table(self, table_name:str, fields:list[str]) -> None:
        self.execute_query("")
        pass 
        """Uncompleted yet"""



""" Now with a simple cursor object we can execute the most common queries like the typical 'SELECT', or create a table with ease reducing the SQL statement we have to provide to just parameters. """
my_database = Database('MyDatabase')
my_cursor = CustomCursor(my_database)

# Creating users table
my_cursor.create_table('users')

# Fetching data from database in users table
result = my_cursor.execute_simple_select_query('users', ['username', 'email', 'password', 'age'])
print(result)