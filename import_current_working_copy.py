import psycopg2
import os
import csv
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', required=True)
    args = parser.parse_args()

    # Define the database name and collation
    database_name = 'ukraine_it_ceo'

    table_name = os.path.basename(args.file_path)

    # Define the SQL statement to create the table
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS current_working_copy (
        sales_navigator_profile_url TEXT PRIMARY KEY
    );
    """

    try:
        print('Connect to the PostgreSQL database')

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
        with open(args.file_path, 'r', encoding="utf-8") as csv_file:
            # Use the COPY statement to insert data from the CSV into the table
            cur.copy_expert(sql=f"COPY current_working_copy FROM stdin WITH CSV HEADER", file=csv_file)

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

