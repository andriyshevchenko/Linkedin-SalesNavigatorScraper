import psycopg2
from datetime import datetime
import csv

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host='159.89.13.130',
    port=5432,
    database='ukraine_it_ceo',
    user='Administrator',
    password='lUwm8vS21jLW'
)
cursor = conn.cursor()

# Fetch data from the connected_profiles table
cursor.execute("SELECT * FROM connected_profiles")
data = cursor.fetchall()

today = datetime.utcnow().strftime('%Y-%m-%d')

# Define the CSV file path
csv_file_path = f'export_{today}.csv'

# Write the data to a CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write the header
    csv_writer.writerow(['profile_url', 'full_name'])
    # Write the data rows
    csv_writer.writerows(data)

# Close the cursor and connection
cursor.close()
conn.close()

print(f"Data from 'connected_profiles' table exported to '{csv_file_path}' successfully.")
