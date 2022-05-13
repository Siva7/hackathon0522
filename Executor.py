import asyncio
import sys

from azurecomp.azure_blob_storage import upload_local_file_to_cloud
from webScraping.CompanyDiversityDeclaration import scan_urls_collected
from webScraping.WebPageDetection import gather_info_from_web

def execute():
    asyncio.run(gather_info_from_web(sys.argv[1],sys.argv[2]))
    asyncio.run(scan_urls_collected())
    upload_local_file_to_cloud(
        sys.argv[3],sys.argv[1], sys.argv[2])

if __name__=='__main__':
    execute()
    # upload_local_file_to_cloud("DefaultEndpointsProtocol=https;AccountName=webscraptest;AccountKey=4CAwZJ0BIJxFlkje7tAS33sqhnEPTs+RMap3YRcB6FCGhe+vHwcSxFM9So4hfYl9qrlcsv0W/r+h+AStzp8T+Q==;EndpointSuffix=core.windows.net",0,1)