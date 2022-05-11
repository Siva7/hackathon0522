from azure.storage.blob import BlobServiceClient
def upload_string_as_blob(file_name,data):
    service = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=acogstorage;AccountKey=A/AqRiqGci9qzqxFB28nW/L8Usi+BEQQyTRZOAuPlxCOdrLaqq5mTqbt/bxBQF4hhsB8kgGLZiY/+AStnKydAw==;EndpointSuffix=core.windows.net")
    container_client=service.get_container_client("datadump")
    container_client.upload_blob(name=file_name,data=data)


if __name__ == '__main__':
    upload_string_as_blob()