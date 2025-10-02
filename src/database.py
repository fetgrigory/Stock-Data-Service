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


# Creates the users table
def create_users_table():
    """AI is creating summary for create_users_table
    """
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
        conn.commit()


# Adding a new user
def insert_user(username: str, password: str):
    """AI is creating summary for insert_user

    Args:
        username (str): [description]
        password (str): [description]

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id",
                (username, password)
            )
            user_id = cursor.fetchone()[0]
        conn.commit()
    return user_id


# Getting the user's by username
def get_user_by_username(username: str):
    """AI is creating summary for get_user_by_username

    Args:
        username (str): [description]

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, password FROM users WHERE username=%s", (username,))
            return cursor.fetchone()


# Creates the recipients table if it does not exist
def create_recipients_table():
    """AI is creating summary for create_recipients_table
    """
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
    """AI is creating summary for insert_recipient_data

    Args:
        name (str): [description]
        email (str): [description]

    Returns:
        [type]: [description]
    """
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
    """AI is creating summary for update_recipient_data

    Args:
        recipient_id (int): [description]
        name (str): [description]
        email (str): [description]

    Returns:
        [type]: [description]
    """
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
    """AI is creating summary for delete_recipient_data

    Args:
        recipient_id (int): [description]

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM recipients WHERE id = %s", (recipient_id,))
        conn.commit()
        return recipient_id


# Create the smtp_settings table
def create_smtp_settings_table():
    """AI is creating summary for create_smtp_settings_table
    """
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS smtp_settings (
                    id SERIAL PRIMARY KEY,
                    server TEXT NOT NULL,
                    port INT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    sender TEXT NOT NULL
                )
            """)
        conn.commit()


# Add a new configuration
def insert_smtp_setting(server, port, username, password, sender):
    """AI is creating summary for insert_smtp_setting

    Args:
        server ([type]): [description]
        port ([type]): [description]
        username ([type]): [description]
        password ([type]): [description]
        sender ([type]): [description]

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO smtp_settings (server, port, username, password, sender)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (server, port, username, password, sender))
            smtp_id = cursor.fetchone()[0]
        conn.commit()
    return smtp_id


# Get the first configuration
def get_smtp_setting():
    """AI is creating summary for get_smtp_setting

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, server, port, username, password, sender
                FROM smtp_settings
                LIMIT 1
            """)
            result = cursor.fetchone()
    return result


# Returns a list of all email addresses of recipients
def get_all_recipients():
    """AI is creating summary for get_all_recipients

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM recipients")
            results = cursor.fetchall()
    return [row[0] for row in results]


# Updating a configuration
def update_smtp_data(smtp_id: int, server: str | None, port: int | None, username: str | None, password: str | None, sender: str | None):
    """AI is creating summary for update_smtp_data

    Args:
        smtp_id (int): [description]
        server (str): [description]
        port (int): [description]
        username (str): [description]
        password (str): [description]
        sender (str): [description]

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        with conn.cursor() as cursor:
            # Getting the current SMTP data
            cursor.execute(
                "SELECT server, port, username, password, sender FROM smtp_settings WHERE id = %s", (smtp_id,))
            result = cursor.fetchone()
            if not result:
                return None

            current_server, current_port, current_username, current_password, current_sender = result

        # If the field is None, leave the old value
            new_server = server if server is not None else current_server
            new_port = port if port is not None else current_port
            new_username = username if username is not None else current_username
            new_password = password if password is not None else current_password
            new_sender = sender if sender is not None else current_sender

            cursor.execute(
                """
                UPDATE smtp_settings
                SET server = %s, port = %s, username = %s, password = %s, sender = %s
                WHERE id = %s
                RETURNING server, port, username, password, sender
                """,
                (new_server, new_port, new_username, new_password, new_sender, smtp_id)
            )
            updated = cursor.fetchone()
        conn.commit()

    return {"server": updated[0], "port": updated[1], "username": updated[2], "password": updated[3], "sender": updated[4]}


# Deleting a configuration
def delete_smtp_data(smtp_id: int):
    """AI is creating summary for delete_smtp_data

    Args:
        smtp_id (int): [description]

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM smtp_settings WHERE id = %s", (smtp_id,))
        conn.commit()
        return smtp_id


# Getting the recipient's name by email
def get_recipient_name(email: str):
    """AI is creating summary for get_recipient_name

    Args:
        email (str): [description]

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM recipients WHERE email = %s", (email,))
            result = cursor.fetchone()
    return result[0] if result else None
