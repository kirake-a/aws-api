import uuid
import time
from boto3.dynamodb.conditions import Attr
# Importamos la nueva función
from config.aws_client import get_aws_resource 

class DynamoDBService:
    def __init__(self):
        self.dynamodb = get_aws_resource('dynamodb') 
        self.table = self.dynamodb.Table('sesiones-alumnos')

    def create_session(self, student_id: int, session_string: str) -> None:
        item = {
            'id': str(uuid.uuid4()),
            'fecha': int(time.time()),
            'alumnoId': student_id,
            'active': True,
            'sessionString': session_string
        }
        self.table.put_item(Item=item)

    def get_session_by_string(self, session_string: str):
        response = self.table.scan(
            FilterExpression=Attr('sessionString').eq(session_string)
        )
        items = response.get('Items', [])
        return items[0] if items else None

    def invalidate_session(self, session_id: str) -> None:
        self.table.update_item(
            Key={'id': session_id},
            UpdateExpression="set active = :val",
            ExpressionAttributeValues={':val': False}
        )