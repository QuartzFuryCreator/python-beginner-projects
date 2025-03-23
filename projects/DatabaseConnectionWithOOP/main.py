from classes import Database, CustomCursor


""" Now with a simple cursor object we can execute the most common queries like the typical 'SELECT', or create a table with ease reducing the SQL statement we have to provide to just parameters. """
my_database = Database('MyDatabase')
my_cursor = CustomCursor(my_database)

# Creating users table
my_cursor.create_table('users', ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'username TEXT UNIQUE NOT NULL', 'email TEXT UNIQUE NOT NULL', 'password TEXT NOT NULL', 'age INTEGER'])

# Inserting data in users table
users_to_insert = [
    ['Joaquin', 'joaquin@gmail.com', '123password', 22], 
    ['Aline', 'aline@gmail.com', '123password', 21], 
    ['Henry', 'henry@gmail.com', '123password', 35], 
    ['James', 'james@gmail.com', '123password', 32], 
    ['Nicole', 'nicole@gmail.com', '123password', 28],
    ['Maria', 'maria@gmail.com', '123password', 38] 
]
users_fields = ['username', 'email', 'password', 'age']
my_cursor.insert_rows('users', users_fields, users_to_insert)

# Fetching data from database in users table
result = my_cursor.execute_simple_select_query('users', users_fields)
result2 = my_cursor.execute_simple_select_query('users', ['username', 'age'])
print('First fetch:', result)
print('Second fetch:', result2)