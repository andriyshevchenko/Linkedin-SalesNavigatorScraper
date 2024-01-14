import psycopg2
from datetime import datetime
import csv
from TelegramLog import TelegramLog
from telegram import Bot
import asyncio

async def main():
    log = TelegramLog(Bot(token='6464053578:AAGbooTDuVCdiYqMhN2akhMMEJI0wVZSr7k'), '-1002098033156', 'export_connected_profiles')  
    await log.write('Function started')
    
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
    cursor.execute("""
        SELECT pp.profile_url, pp.full_name
        FROM connected_profiles pp
        LEFT JOIN already_connected_profiles acp
            ON pp.profile_url = acp.profile_url
        WHERE acp.profile_url IS NULL;""")

    data = cursor.fetchall()

    # Define the CSV file path
    csv_file_path = 'connect.csv'

    # Write the data to a CSV file
    with open(csv_file_path, 'w', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header
        csv_writer.writerow(['ProfileUrl', 'FullName'])
        # Write the data rows
        csv_writer.writerows(data)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    await log.write(f"Data from 'connected_profiles' table exported to '{csv_file_path}' successfully.\n\n{len(data)} profiles impacted.")

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())

