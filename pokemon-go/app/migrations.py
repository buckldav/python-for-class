import sqlite3
from .utils import list_to_string

# https://www.sqlitetutorial.net/sqlite-python/create-tables/
# Students can modify this to meet their needs
sql_create_pokedex_table = """ \
CREATE TABLE IF NOT EXISTS pokedex (
	id integer PRIMARY KEY,
	name text NOT NULL UNIQUE,
	types text NOT NULL,
	flavor_text text NOT NULL
); \
"""

database = "./pokedex.sqlite3"

def create_table_migration():
	# Connect to our flat file database
	conn = sqlite3.connect(database)
	c = conn.cursor()
	# Execute SQL
	c.execute(sql_create_pokedex_table)
	# Save (commit) the changes
	conn.commit()
	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()