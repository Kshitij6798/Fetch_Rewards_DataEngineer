import json
import hashlib
import datetime

def clean_message(message, bad_message_queue):
    """
    Clean and transform a message dictionary by masking sensitive data and modifying its structure.

    Parameters:
        message (str): The JSON message to be processed as a string.
        bad_message_queue (list): A list to store messages that could not be processed.

    Returns:
        dict: A dictionary representing the cleaned and transformed message, or None if the message is invalid.

    """
    try:
        # Load the JSON message into a dictionary
        message_dict = json.loads(message)

        # Define a function to mask a string using sha256
        def mask_string(value):
            return hashlib.sha256(value.encode()).hexdigest()

        # Transform and modify the dictionary
        new_message = {
            'user_id': message_dict.get('user_id'),
            'device_type': message_dict.get('device_type'),
            'masked_ip': mask_string(message_dict.get('ip')),
            'masked_device_id': mask_string(message_dict.get('device_id')),
            'locale': message_dict.get('locale'),
            'app_version': int(message_dict.get('app_version').split('.')[0]),
            'create_date': datetime.datetime.now().isoformat()
        }

        return new_message
    except Exception as ex:
        bad_message_queue.append(message)
