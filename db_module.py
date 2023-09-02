import psycopg2
from psycopg2 import sql

def insert_query(conn, user_login_dict):
    """
    Insert a user login record into the PostgreSQL database.

    Parameters:
        conn (psycopg2.extensions.connection): The PostgreSQL database connection.
        user_login_dict (dict): A dictionary containing user login information.

    Returns:
        int: A status code indicating the result of the insertion operation.
             - 0: Successfully inserted.
             - 1: Failed to insert.
    """

    try:
        insert_query = """
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            user_login_dict["user_id"],
            user_login_dict["device_type"],
            user_login_dict["masked_ip"],
            user_login_dict["masked_device_id"],
            user_login_dict["locale"],
            user_login_dict["app_version"],
            user_login_dict["create_date"]
        )
        with conn, conn.cursor() as cursor:
            cursor.execute(insert_query, data)
        return 0
    except Exception as e:
        return 1
