import psycopg2
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', required=True)
    args = parser.parse_args()

    # Define the database name and collation
    database_name = 'ukraine_it_ceo'
    collation = 'en_US.utf8'

    # Define the SQL statement to create the database if it doesn't exist
    create_database_sql = f"""
    CREATE DATABASE {database_name} WITH ENCODING 'UTF8' LC_COLLATE = '{collation}' LC_CTYPE = '{collation}' TABLESPACE = pg_default CONNECTION LIMIT = -1 IS_TEMPLATE = False TEMPLATE 'template0';
    """

    try:
        print('Connect to the PostgreSQL database')

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host='159.89.13.130',
            port=5432,
            database='master',
            user='Administrator',
            password='lUwm8vS21jLW'
        )
        conn.autocommit = True
        print('Create a cursor object')

        # Create a cursor object
        cur = conn.cursor()

        print('Create the database if it doesn\'t exist')

        # Create the database if it doesn't exist

        cur.execute(create_database_sql)

        print('Commit the transaction to create the database')
        # Commit the transaction to create the database

        conn.commit()
        
        print('Close the connection to the default database')
        # Close the connection to the default database
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

    finally:
        # Close the cursor and database connection
        if cur:
            cur.close()
        if conn:
            conn.close()

