import asyncio
import sys

from azurecomp.azure_blob_storage import upload_local_file_to_cloud, upload_counter_string_as_blob
from webScraping.CompanyDiversityDeclaration import scan_urls_collected
from webScraping.WebPageDetection import gather_info_from_web
from webScraping.utils import counter
def execute():
    asyncio.run(gather_info_from_web(sys.argv[1],sys.argv[2]))
    asyncio.run(scan_urls_collected())
    upload_local_file_to_cloud(
        sys.argv[3],sys.argv[1], sys.argv[2])
    upload_counter_string_as_blob(sys.argv[3],sys.argv[1], sys.argv[2],f"""
    Total number of calls to google search [APi]=${counter.google_search_count}
    Total number of urls Analyzed=${counter.number_of_urls_scanned}
    Total number of Web Pages Analyzed=${counter.number_of_web_pages_scanned}
    """)

if __name__=='__main__':
    execute()
    # asyncio.run(gather_info_from_web(311, 315))
    # asyncio.run(scan_urls_collected())
    # print(f"""
    # Total number of calls to google search [API]={counter.google_search_count}
    # Total number of urls Analyzed={counter.number_of_urls_scanned}
    # Total number of Web Pages Analyzed={counter.number_of_web_pages_scanned}
    # """)
    # upload_local_file_to_cloud("DefaultEndpointsProtocol=https;AccountName=webscraptest;AccountKey=4CAwZJ0BIJxFlkje7tAS33sqhnEPTs+RMap3YRcB6FCGhe+vHwcSxFM9So4hfYl9qrlcsv0W/r+h+AStzp8T+Q==;EndpointSuffix=core.windows.net"
    #                            ,300,400)