import sqlite3

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
    return conn

# Function to execute a SELECT query
def execute_select_query(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
        rows = c.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return None

# Function to print query results
def print_query_results(query, rows):
    print(f"\nQuery: {query}")
    print("Results:")
    if rows:
        for row in rows:
            print(row)
    else:
        print("No results found.")

# Main function
def main():
    database = "imdb.db"  # Replace with your .db file

    # Create a database connection
    conn = create_connection(database)

    if conn is not None:
        # Example SELECT queries

        # 1. Select distinct names from People table
        query = "SELECT DISTINCT name FROM people LIMIT 10;"    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)

        # 2. Select names from People
        query = "SELECT * FROM people LIMIT 10;"    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)

        # 3. Select ratings, crew and titles for display
        query = "SELECT * FROM ratings LIMIT 10;"    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)

        query = "SELECT * FROM crew LIMIT 10;"    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)

        query = "SELECT * FROM titles LIMIT 10;"    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows) 

        # 4. Select titles according to types
        query = "SELECT type, COUNT(DISTINCT title_id) FROM titles GROUP BY type ORDER BY type;"    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)

        # 5. Select best rated movies  
        query = """SELECT T.primary_title, R.rating, R.votes as numVotes
                FROM titles AS T
                JOIN ratings AS R ON T.title_id = R.title_id
                WHERE numVotes > 10
                ORDER BY R.rating DESC, numVotes DESC
                LIMIT 10;"""    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)

        #6. select most popular 10 genre
        query = """SELECT T.genres,  AVG(R.rating) as avgRating
            FROM titles AS T
            JOIN ratings AS R ON T.title_id = R.title_id
            GROUP BY T.genres
            ORDER BY T.genres
            LIMIT 10;"""    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)

        #7. select most popular directors
        query = """SELECT C.job,  AVG(R.rating) as avgRating
            FROM crew AS C
            JOIN ratings AS R ON C.title_id = R.title_id
            WHERE C.job LIKE '%director%'
            GROUP BY C.job
            ORDER BY avgRating DESC
            LIMIT 10;"""    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)

        #8. select Tarantino movies
        query = """SELECT *
            FROM people 
            WHERE name LIKE '%Taran%'
            LIMIT 10;"""    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)

        #9. select most popular Tarantino movies
        query = """SELECT P.name, T.original_title,  R.rating
            FROM titles AS T
            JOIN ratings AS R ON T.title_id = R.title_id
            JOIN crew AS C ON T.title_id = C.title_id
            JOIN people AS P ON C.person_id = P.person_id
            WHERE P.name LIKE '%Tarantino%'
            ORDER BY R.rating DESC
            LIMIT 10;"""    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)
  

        #10. select most popular actor and actress
        query = """SELECT P.name,  R.rating
            FROM people AS P
            JOIN crew AS C ON C.person_id = P.person_id
            JOIN ratings AS R ON C.title_id = R.title_id
            WHERE (C.category='actor' OR C.category='actress') AND R.votes > 5000
            ORDER BY R.rating DESC, P.name
            LIMIT 10;"""    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)

        #11. Calculate average ratings for actors and actresses 
        query = """SELECT C.category,  AVG(R.rating) as avgRating
            FROM crew AS C
            JOIN ratings AS R ON C.title_id = R.title_id
            WHERE (C.category='actor' OR C.category='actress') 
            GROUP BY C.category
            LIMIT 2;"""    
        rows = execute_select_query(conn, query)
        print_query_results(query, rows)


        # Close the connection
        conn.close()
        print("\nConnection closed.")
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()