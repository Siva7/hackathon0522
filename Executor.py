import asyncio

from webScraping.CompanyDiversityDeclaration import scan_urls_collected
from webScraping.WebPageDetection import gather_info_from_web

def execute():
    asyncio.run(gather_info_from_web(0,1))
    asyncio.run(scan_urls_collected())

if __name__=='__main__':
    execute()