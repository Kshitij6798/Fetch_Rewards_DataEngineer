import logging
import traceback
import psycopg2
from loguru import logger
from sqs_module import get_from_queue
from transform_module import clean_message
from db_module import insert_query

# Define constants
batch_size = 20
wait_time = 5
max_bad_message = 30

# Initialize logging
logger.add("app.log", mode = 'w')

def main():
    """Entry point of the application."""
    # Initialize queues
    message_queue = []
    bad_message_queue = []

    # Initialize the Postgres connection
    postgres_db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': '5432'
    }
    conn = psycopg2.connect(**postgres_db_params)
    cur = conn.cursor()

    try:
        # Process message
        while True:
            try:
                # Extracting messages directly using boto3
                response = get_from_queue(
                    batch_size=batch_size,
                    endpoint_url= 'http://localhost:4566',
                    queue_url = 'http://localhost:4566/000000000000/login-queue',
                    wait_time=wait_time
                )
                message_queue.extend(response)
                logger.info(f"{len(message_queue)} messages in the queue")

                # Transform and load messages
                for message in message_queue:
                    new_message = clean_message(message['Body'], bad_message_queue)
                    status_code = insert_query(conn, new_message)
                    if status_code == 1:
                        bad_message_queue.append(new_message)
                        logger.error("Failed to insert message", message=new_message)


            except Exception as ex:
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                logger.error(f"Job Terminated due to exception")
                conn.rollback()

            finally:
                logger.debug(f"Bad messages {bad_message_queue}")

            if len(bad_message_queue) > max_bad_message:
                logger.error("Bad messages over the allowed limit!")
                break

        conn.commit()

    except Exception as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        logger.error(f"Job Terminated due to exception")
        conn.rollback()

    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    main()
