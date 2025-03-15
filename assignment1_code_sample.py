import os
import pymysql
from urllib.request import urlopen
import requests

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

def send_email(to, subject, body):
    os.system(f'echo {body} | mail -s "{subject}" {to}')

# Unvalidated External URL in get_data
# Vulnerability: The script fetches data from http://insecure-api.com/get-data without validating the source or using HTTPS.
# OWASP Category: A08:2021 – Software and Data Integrity Failures
# Mitigation: Use HTTPS and validate the SSL certificate.
def get_data():
    url = 'https://secure-api.com/get-data'  # Use HTTPS
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raise error for bad responses
    return response.text

def save_to_db(data):
    query = f"INSERT INTO mytable (column1, column2) VALUES ('{data}', 'Another Value')"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
