from azure.storage.blob import BlobServiceClient
def upload_string_as_blob(file_name,data):
    service = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=acogstorage;AccountKey=A/AqRiqGci9qzqxFB28nW/L8Usi+BEQQyTRZOAuPlxCOdrLaqq5mTqbt/bxBQF4hhsB8kgGLZiY/+AStnKydAw==;EndpointSuffix=core.windows.net")
    container_client=service.get_container_client("datadump")
    container_client.upload_blob(name=file_name,data=data)

def upload_local_file_to_cloud(connectionString,start,stop):
    service = BlobServiceClient.from_connection_string(
        connectionString)
    container_client = service.get_container_client("datadump")
    # container_client.upload_blob(name=file_name, data=data)
    # blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    with open("Hackathon_Data_MinorityWomenOwned_2022 withcompany_urls_and_info.xlsx", "rb") as data:
        container_client.upload_blob(name="Hackathon_Data_"+str(start)+"_"+str(stop)+".xlsx", data=data)

if __name__ == '__main__':
    upload_local_file_to_cloud("DefaultEndpointsProtocol=https;AccountName=webscraptest;AccountKey=4CAwZJ0BIJxFlkje7tAS33sqhnEPTs+RMap3YRcB6FCGhe+vHwcSxFM9So4hfYl9qrlcsv0W/r+h+AStzp8T+Q==;EndpointSuffix=core.windows.net",0,1)