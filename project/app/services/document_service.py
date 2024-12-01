import boto3
from botocore.exceptions import ClientError
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.document import Document
from app.schemas.document import DocumentOut
from app.config import settings

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

def upload_document_to_s3(file, chatbot_id: int):
    unique_filename = f"{chatbot_id}/{uuid4()}_{file.filename}"
    try:
        s3_client.upload_fileobj(file.file, settings.AWS_S3_BUCKET_NAME, unique_filename, ExtraArgs={"ACL": "public-read"})
    except ClientError as e:
        print(e)
        return None
    return unique_filename

def create_document_record(db: Session, chatbot_id: int, filename: str, s3_key: str):
    db_document = Document(
        chatbot_id=chatbot_id,
        filename=filename,
        s3_key=s3_key
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_documents_by_chatbot(db: Session, chatbot_id: int):
    return db.query(Document).filter(Document.chatbot_id == chatbot_id).all()