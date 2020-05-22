import psycopg2

# Function to access the database locally, and execute a query
# Make sure to change the username, databse and password
def execQuery(query):
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "dataScience20",
                                      host = "localhost",
                                      port = "5432",
                                      database = "fakenews")
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except (Exception, psycopg2.Error) as error :
        connection = False
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("Executed query and closed connection.")

