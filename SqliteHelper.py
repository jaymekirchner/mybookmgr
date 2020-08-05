import sqlite3

class SqliteHelper:
    """Creates connection to database and facilitates sqlite queries to create and modify the user's data.

    METHODS:
        __init__(self, name = None)
            Accepts a database name to initialize the database connection and cursor, and call the open() method

        open(self, name)
            Attempts to connect to the database with the passed-in name and if it does not exist, the database will be created
            
        create_table(self)
            Creates the books table if it does not already exist
        
        create_calendar_table(self)
            Creates the calendar table if it does not already exist

        create_filter_table(self)
            Creates the filter table if it does not already exist
  
        insert(self, query, inserts) 
            Executes the insert query with parameterized statements

        select(self, query): 
            Executes the select query without parameterized statements
        
        sort_items(self, query, comparisons): 
            Executes the select query with parameterized statements
        
        update(self, query, updates): 
            Executes the update query with parameterized statements

        delete(self, query)
            Executes the delete query without parameterized statements

        filter_items(self, category, data)
            SQLite query to insert data into results table based on user's filter
    """

    def __init__(self, name = None):
        """Accepts a database name to initialize the database connection and cursor, and call the open() method.

        Parameters: 
            name (string) - default is None or user can pass in a database name
        """
        
        self.conn = None
        self.cursor = None 

        if name: 
            self.open(name) 

    def open(self, name): 
        """Attempts to connect to the database with the passed-in name and if it does not exist, the database will be created.

        Raises sqlite3.Error
            Failed to connect to database
        """
        
        try: 
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()
            print(sqlite3.version)
        except sqlite3.Error as e:
            print("Failed to connect to database")

    def create_table(self): 
        """Creates the books table if it does not already exist."""
       
        c = self.cursor
        c.execute("""CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            rating INTEGER NOT NULL,
            genre TEXT NOT NULL,
            series TEXT NOT NULL,
            notes TEXT NOT NULL            
            )""") 

    def create_calendar_table(self):
        """Creates the calendar table if it does not already exist."""
        
        c = self.cursor
        c.execute("""CREATE TABLE IF NOT EXISTS calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL            
            )""") 

    def create_filter_table(self): 
        """Creates the filter table if it does not already exist."""

        c = self.cursor
        c.execute("""CREATE TABLE IF NOT EXISTS results (
            id INTEGER NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            rating INTEGER NOT NULL,
            genre TEXT NOT NULL,
            series TEXT NOT NULL,
            notes TEXT NOT NULL            
            )""") 

    def insert(self, query, inserts): 
        """Executes the insert query.

        Parameters:
            query (string) - sqlite query passed in by user with parameterized statements
            inserts (tuple) - items to be inserted into parameterized sqlite statement
        """

        c = self.cursor
        c.execute(query, inserts)
        self.conn.commit()

    def select(self, query): 
        """Executes the select query without parameterized statements.

        Parameters:
            query (string) - sqlite query without parameterized statements
        """

        c = self.cursor
        c.execute(query)
        return c.fetchall() #returns a list ([] if no matches)

    def sort_items(self, query, comparisons): 
        """Executes the select query with parameterized statements.

        Parameters:
            query (string) - sqlite query with parameterized statements
            comparisons (tuple) - items to be inserted into parameterized sqlite statement
        """

        c = self.cursor
        c.execute(query, comparisons)
        return c.fetchall() #returns a list ([] if no matches)

    def update(self, query, updates): 
        """Executes the update query with parameterized statements.

        Parameters:
            query (string) - sqlite query with parameterized statements
            updates (tuple) - items to be inserted into parameterized sqlite statement
        """

        c = self.cursor
        c.execute(query, updates)
        self.conn.commit() 

    def delete(self, query): 
        """Executes the delete query without parameterized statements.

        Parameters:
            query (string) - sqlite query without parameterized statements
        """

        c = self.cursor
        c.execute(query)
        self.conn.commit()

    def filter_items(self, category, data):
        """SQLite query to insert data into results table based on user's filter.

        Parameters:
            category (string) - category chosen from radio button in filter wizard (author, genre, rating, or notes)
            data (string) - value selected from drop-down menu in filter wizard
        """

        c = self.cursor
        query = "INSERT INTO results SELECT * FROM books WHERE "+ category + "= \"" + data +"\"" 
        c.execute(query)