import psycopg2
import os
import csv
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', required=True)
    args = parser.parse_args()

    # Define the database name and collation
    database_name = 'Ukraine_IT_CEO'
    collation = 'en_US.utf8'

    # Define the SQL statement to create the database if it doesn't exist
    create_database_sql = f"""
    CREATE DATABASE {database_name} WITH ENCODING 'UTF8' LC_COLLATE = '{collation}' LC_CTYPE = '{collation}' TABLESPACE = pg_default CONNECTION LIMIT = -1 IS_TEMPLATE = False TEMPLATE 'template0';
    """

    table_name = os.path.basename(args.file_path)

    # Define the SQL statement to create the table
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        profile_url TEXT PRIMARY KEY,
        full_name TEXT
    );
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

        # Reconnect to the 'CEO' database
        conn = psycopg2.connect(
            host='159.89.13.130',
            port=5432,
            database=database_name,
            user='Administrator',
            password='lUwm8vS21jLW'
        )
        cur = conn.cursor()

        # Create the table
        cur.execute(create_table_sql)

        # Open and read the CSV file
        with open(args.file_path, 'r') as csv_file:
            # Use the COPY statement to insert data from the CSV into the table
            cur.copy_expert(sql=f"COPY linkedin_profiles FROM stdin WITH CSV HEADER", file=csv_file)

        # Commit the transaction
        conn.commit()

        print("Data inserted successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

    finally:
        # Close the cursor and database connection
        if cur:
            cur.close()
        if conn:
            conn.close()

