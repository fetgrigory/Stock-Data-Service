'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 25/09/2025
Ending //

'''
# Installing the necessary libraries
import os
import psycopg2


def db_connect():
    """AI is creating summary for db_connect

    Returns:
        [type]: [description]
    """
    # Establish a connection to the PostgreSQL database using environment variables
    return psycopg2.connect(
        # Database host
        host=os.getenv('HOST'),
        # Name of the database
        dbname=os.getenv('DBNAME'),
        # Username for authentication
        user=os.getenv('USER'),
        # Password for authentication
        password=os.getenv('PASSWORD'),
        # Port number for database connection
        port=os.getenv('PORT')
    )


# Creates the recipients table if it does not exist
def create_recipients_table():
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recipients (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            """)
        conn.commit()


# Adding a new recipient
def insert_recipient_data(name: str, email: str):
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO recipients (name, email) VALUES (%s, %s) RETURNING id",
                (name, email)
            )
            recipient_id = cursor.fetchone()[0]
        conn.commit()
    return recipient_id


# Updating a recipient
def update_recipient_data(recipient_id: int, name: str | None, email: str | None):
    with db_connect() as conn:
        with conn.cursor() as cursor:
            # Getting the current recipient data
            cursor.execute("SELECT name, email FROM recipients WHERE id = %s", (recipient_id,))
            result = cursor.fetchone()
            if not result:
                return None
            current_name, current_email = result

            # If the field is None, leave the old value
            new_name = name if name is not None else current_name
            new_email = email if email is not None else current_email

            cursor.execute(
                "UPDATE recipients SET name = %s, email = %s WHERE id = %s RETURNING name, email",
                (new_name, new_email, recipient_id)
            )
            updated = cursor.fetchone()
        conn.commit()
    return {"name": updated[0], "email": updated[1]}


# Deleting a recipient
def delete_recipient_data(recipient_id: int):
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM recipients WHERE id = %s", (recipient_id,))
        conn.commit()
        return recipient_id
