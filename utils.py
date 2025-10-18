import mimetypes
import os
import uuid
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class S3Manager:
    """
    A manager for handling all interactions with Amazon S3.

    This class centralizes the logic for connecting to S3, uploading files,
    and retrieving file information. It's designed to be a one-stop shop
    for all S3-related operations in the application.
    """

    def __init__(self):
        """
        Initializes the S3Manager and sets up the S3 client.

        By not passing credentials directly to boto3.client(), the library
        will automatically search for credentials in your environment, such as
        IAM roles, environment variables, or the AWS credentials file.
        This makes the application more secure and flexible.
        """
        self.s3_client = boto3.client("s3", region_name=os.getenv("AWS_S3_REGION"))
        self.bucket_name = os.getenv("AWS_S3_BUCKET_NAME")

    def upload_file(self, file_path: str) -> dict:
        """
        Uploads a file from the local filesystem to S3.

        This method handles everything from validating the file to uploading
        it to S3 with the correct content type.

        Args:
            file_path (str): The absolute path to the file on the local filesystem.

        Returns:
            dict: A dictionary containing details about the uploaded file,
                  including its S3 key, status, and location.
        """
        # Ensure the file exists before proceeding.
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Guess the file's content type, or default to a generic binary type.
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = "application/octet-stream"

        # Generate a unique key for the file to avoid naming conflicts in S3.
        # Using a UUID ensures that every uploaded file has a distinct name.
        file_extension = Path(file_path).suffix
        key = f"user_uploads/{uuid.uuid4()}{file_extension}"

        # Read the file's content in binary mode.
        with open(file_path, "rb") as file:
            file_content = file.read()

        # Upload the file to S3 using the put_object method.
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=file_content,
            ContentType=content_type,
        )

        # Return a success response with details about the uploaded file.
        return {
            "file_key": key,
            "status": "success",
            "message": f"File uploaded successfully from {file_path}",
            "s3_location": f"s3://{self.bucket_name}/{key}",
        }

    def get_file_info(self, file_key: str) -> dict:
        """
        Retrieves metadata about a file stored in S3.

        This method is useful for checking if a file exists and getting
        details like its size and content type without downloading the
        entire file.

        Args:
            file_key (str): The S3 key of the file.

        Returns:
            dict: A dictionary with the file's metadata. If the file
                  doesn't exist, it returns an error message.
        """
        try:
            # Use head_object to get metadata without the file body.
            # This is much faster and more efficient than downloading the file.
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=file_key)

            # Return a dictionary with the file's information.
            return {
                "file_key": file_key,
                "exists": True,
                "size_bytes": response.get("ContentLength"),
                "content_type": response.get("ContentType"),
                "last_modified": response.get("LastModified").isoformat()
                if response.get("LastModified")
                else None,
            }
        except ClientError:
            # If head_object raises a ClientError, it usually means the file was not found.
            return {"file_key": file_key, "exists": False, "error": "File not found"}
