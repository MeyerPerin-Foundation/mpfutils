from azure.storage.blob import BlobServiceClient, ContainerClient
import logging
import os

logger = logging.getLogger("mpf-utils.azstorage")

class AzsContainerClient:
    def __init__(self, container_name: str, conn_str: str = None, sas_url: str = None):
        
        if not conn_str and not sas_url:
            conn_str = os.getenv("AZSTORAGE_CONNECTION_STRING")
        
        if not sas_url:
            logger.info("Using connection string to connect to Azure Storage")
            blob_service_client = BlobServiceClient.from_connection_string(conn_str)
            self.container_client = blob_service_client.get_container_client(container_name)
        else:
            # if there's a sas_url, it overrides the conn_str
            logger.info("Using SAS URL to connect to Azure Storage")
            self.container_client = ContainerClient.from_container_url(sas_url)
        
    def upload_blob(self, blob_name, data, overwrite=True):
        blob_client = self.container_client.get_blob_client(blob=blob_name)
        blob_client.upload_blob(data, overwrite=overwrite)
        return blob_client.url

    def download_blob(self, container_name, blob_name):
        blob_client = self.container_client.get_blob_client(blob=blob_name)
        return blob_client.download_blob().readall()
