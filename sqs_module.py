import boto3

def get_from_queue(batch_size,endpoint_url,queue_url, wait_time):
    """
    Retrieve messages from an Amazon SQS queue.
    Parameters:
        batch_size (int): Max number of messages we try to fetch from the queue.
        queue_url (str): The URL of the SQS queue to retrieve messages from.
        batch_size (int): The maximum number of messages to retrieve in a single batch.
        wait_time (int): The time, in seconds, to wait for messages if the queue is empty.

    Returns:
        list: A list of received messages as dictionaries, or an empty list if no messages are available.

    """
    sqs_client = boto3.client(
        'sqs',
        endpoint_url=endpoint_url,
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=batch_size,
        WaitTimeSeconds=wait_time
    )
    messages = response.get('Messages', [])
    return messages
