from azure.storage.blob import BlobServiceClient
import logging
import os

logger = logging.getLogger("mpf-utils.azstorage")

class AzsContainerClient:
    def __init__(self, container_name: str, conn_str: str = None):
        if not conn_str:
            conn_str = os.getenv("AZSTORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        self.client = blob_service_client.get_container_client(container_name)
        
        self.blob_service_client = BlobServiceClient.from_connection_string(conn_str)

    def upload_blob(self, blob_name, data, overwrite=True):
        blob_client = self.client.get_blob_client(blob=blob_name)
        blob_client.upload_blob(data, overwrite=overwrite)
        return blob_client.url

    def download_blob(self, container_name, blob_name):
        blob_client = self.client.get_blob_client(blob=blob_name)
        return blob_client.download_blob().readall()
