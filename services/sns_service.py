import os
from config.aws_client import get_aws_client
from botocore.exceptions import ClientError

class SNSService:
    def __init__(self):
        self.sns_client = get_aws_client('sns')
        self.topic_arn = os.getenv("AWS_SNS_TOPIC_ARN")

    def publish_message(self, subject: str, message: str) -> dict:
        """
        Publica un mensaje en el Topic configurado.
        """
        try:
            response = self.sns_client.publish(
                TopicArn=self.topic_arn,
                Message=message,
                Subject=subject
            )
            return response
        except ClientError as e:
            print(f"Error publishing to SNS: {e}")
            raise e