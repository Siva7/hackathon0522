from webScraping.GoogleSearch import google_search_results_and_desc
from webScraping.utils import get_visible_text_from_webpages
import pandas as pd
import asyncio

diversity_identifiers = {"national minority supplier development council": "women",
                         "nmsdc": "women",
                         "women’s business enterprise national council": "women",
                         "wbenc": "women",
                         "national veteran business development council": "veteran",
                         "nvdbc": "veteran",
                         "national veteran-owned business association": "veteran",
                         "navoba": "veteran",
                         "national lbgt chamber of commerce": "lgbtq+",
                         "nglcc": "lgbtq+",
                         "women led": "women",
                         "racially diverse" : "racial",
                         "women diversity": "women",
                         "lgbt": "lgbtq+",
                         "veteran diversity": "veteran",
                         "veteran employees":"veteran",
                         "veteran led": "veteran",
                         "women business owners":"women"}


def check_for_diversity_mention_in_page(url):
    print("scanning for diversity in "+str(url))
    page_text = get_visible_text_from_webpages(url).lower()
    diversity_list = [diversity_identifiers[key] if key in page_text else "" for key in diversity_identifiers]
    filtered_list = list(filter(lambda x:not x == "",diversity_list))
    return filtered_list

def get_list_of_urls_from_collected_cols(url_string):
    return url_string.replace("CompanyWebSites:","").replace(";RefWebSites:",",").split(",")

def get_urls_and_scan_pages(utl_string):
    list_of_urls=get_list_of_urls_from_collected_cols(utl_string)
    return [check_for_diversity_mention_in_page(eachUrl) for eachUrl in list_of_urls]


async def get_diversity_info_from_company_urls_series(data_excel):
    return data_excel["company_info_urls"].apply(lambda x: str(get_urls_and_scan_pages(x)))

async def get_diversity_info_from_diversity_urls_series(data_excel):
    return data_excel["company_diversity_info_urls"].apply(lambda x: str(get_urls_and_scan_pages(x)))

async def scan_urls_collected():
    data_excel = pd.read_excel('Hackathon_Data_MinorityWomenOwned_2022 withcompany_urls.xlsx')

    diversity_info_from_company_url,diversity_info_from_diversity_search=await asyncio.gather(get_diversity_info_from_company_urls_series(data_excel),
                         get_diversity_info_from_diversity_urls_series(data_excel))
    data_excel["company_info_urls_diversity_info"]=diversity_info_from_company_url
    data_excel["company_diversity_info_urls_diversity_info"] =diversity_info_from_diversity_search


    writer = pd.ExcelWriter('Hackathon_Data_MinorityWomenOwned_2022 withcompany_urls_and_info.xlsx', engine='xlsxwriter')
    data_excel.to_excel(writer,index=False)
    writer.save()


if __name__ == '__main__':
    asyncio.run(scan_urls_collected())
    # # list_of_urls=list(x[0] for x in google_search_results_and_desc("wellsfargo diversity"))
    # # for each_url in list_of_urls:
    # #     print(each_url)
    # #     print(check_for_diversity_mention_in_page(each_url))

    # print(check_for_diversity_mention_in_page("https://www.dnb.com/business-directory/company-profiles.cpy_inc.d3f8766c48e3701560244592f8a542f5.html"))
