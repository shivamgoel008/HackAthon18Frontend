from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
import os

load_dotenv()

class BlobStorageService:
    def __init__(self):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def list_blobs(self, path=""):
        blob_list = self.container_client.list_blobs(name_starts_with=path)
        return [blob.name for blob in blob_list]

    def upload_blob(self, blob_name, data, path="."):
        blob_client = self.container_client.get_blob_client(blob_name)
        with open(os.path.join(path, data), "rb") as data:
            blob_client.upload_blob(data)
        return f"Blob '{blob_name}' uploaded successfully."
    
    def upload_folder(self, folder_path, blob_path=""):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                blob_name = os.path.join(blob_path, os.path.relpath(file_path, folder_path))
                with open(file_path, "rb") as data:
                    self.container_client.get_blob_client(blob_name).upload_blob(data)
        return f"Folder '{folder_path}' uploaded successfully."

    def download_blob(self, blob_name, path="."):
        blob_client = self.container_client.get_blob_client(blob_name)
        download_path = os.path.join(path, blob_name)
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        return f"Blob '{blob_name}' downloaded successfully to {download_path}."

    def download_folder(self, blob_folder_name, local_folder_path=""):
        blobs = self.list_blobs(blob_folder_name)
        for blob in blobs:
            self.download_blob(blob, local_folder_path)
        return f"Folder '{blob_folder_name}' downloaded successfully to '{local_folder_path}'."

    def delete_blob(self, blob_name, path=""):
        blob_client = self.container_client.get_blob_client(os.path.join(path, blob_name))
        blob_client.delete_blob()
        return f"Blob '{blob_name}' deleted successfully from path '{path}'."
    
    def delete_blob_folder(self, folder_path):
        for blob in self.list_blobs(folder_path):
            self.delete_blob(blob)
        return f"Folder '{folder_path}' deleted successfully."

