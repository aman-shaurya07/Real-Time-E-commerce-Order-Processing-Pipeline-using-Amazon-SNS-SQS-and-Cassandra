import boto3
import json

# Initialize SQS client
sqs = boto3.client('sqs', region_name='your-region')
queue_url = 'https://sqs.your-region.amazonaws.com/your-account-id/analytics_queue'

def process_analytics_message(message_body):
    order = json.loads(message_body)
    print(f"Order data sent to analytics pipeline: {order}")

def poll_messages():
    while True:
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=5)
        if 'Messages' in response:
            for message in response['Messages']:
                process_analytics_message(message['Body'])
                sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

if __name__ == "__main__":
    poll_messages()
