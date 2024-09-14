import psycopg2

if __name__ == '__main__':
    # Define the database name and collation
    database_name = 'ukraine_it_ceo'

    # Define the SQL statement to create the table
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS broken_links (
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

