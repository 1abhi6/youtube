from fastmcp import FastMCP
from utils import S3Manager

# Initialize the MCP application
mcp = FastMCP()

# Create an instance of our S3Manager to interact with AWS S3
s3_manager = S3Manager()


@mcp.tool(name="upload_file")
def upload_file(file_path: str):
    """
    A tool to upload a file to S3.

    This tool takes a file path, uploads the file to S3 using our S3Manager,
    and returns the result.
    """
    # Use the S3Manager to upload the file and return the response
    return s3_manager.upload_file(file_path)


@mcp.tool(name="get_file_info")
def get_file_info(file_key: str):
    """
    A tool to get information about a file in S3.

    This tool takes a file key, retrieves the file's metadata from S3,
    and returns it.
    """
    # Use the S3Manager to get file information and return the response
    return s3_manager.get_file_info(file_key)


@mcp.tool(name="download_file")
def download_file(file_key: str, destination_path: str):
    """
    A tool to download a file from S3.

    This tool takes a file key and a destination path, and it downloads the
    file from S3 to the specified local path.
    """
    # Use the S3Manager to download the file and return the response
    return s3_manager.download_file(file_key, destination_path)


if __name__ == "__main__":
    mcp.run()
