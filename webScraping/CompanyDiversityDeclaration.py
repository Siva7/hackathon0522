from webScraping.GoogleSearch import google_search_results_and_desc
from webScraping.utils import get_visible_text_from_webpages
import pandas as pd
import asyncio
import itertools

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
                         "women own": "women",
                         "women diversity": "women",
                         "women business own": "women",
                         "racially diverse" : "racial",
                         "lgbt": "lgbtq+",
                         "veteran diversity": "veteran",
                         "veteran employees":"veteran",
                         "veteran led": "veteran",
                         "veteran own": "veteran",
                         "Asian owned":"Asian",
                         "Asian led":"Asian",
                         "Asian diversity":"Asian",
                         "Indian led":"Asian,Indian",
                         "Indian owned":"Asian,Indian",
                         "Indian diversity":"Asian,Indian",
                         "Chinese led": "Asian,Chinese",
                         "Chinese owned": "Asian,Chinese",
                         "Chinese diversity": "Asian,Chinese",
                         "African American led":"African American",
                        "African American owned":"African American",
                         "African American diversity": "African American",
                        "African led":"African American",
                        "African owned":"African American",
                         "African diversity": "African American",
                         "hispanic owned":"hispanic",
                        "hispanic led":"hispanic",
                        "hispanic diversity":"hispanic"
                         }

diversity_identifiers_for_companies = {}

for key in diversity_identifiers:
    new_key=key.lower()
    diversity_identifiers_for_companies[new_key]=diversity_identifiers[key]
    diversity_identifiers_for_companies[new_key.replace(" ","_")]=diversity_identifiers[key]
    diversity_identifiers_for_companies[new_key.replace(" ", "-")]=diversity_identifiers[key]
    diversity_identifiers_for_companies[new_key.replace(" ", "")] = diversity_identifiers[key]

individual_diversity_keys= {
    "Asian":"asian",
    "hispanic":"hispanic",
    "spanish":"hispanic",
    "latino":"hispanic",
    "mexico":"hispanic",
    "mexican":"hispanic",
    "south american":"hispanic",
    "lgbt":"lgbtq+",
    "african":"African American",
    "Native america": "Native American",
    "China":"Chinese",
    "Chinese":"Chinese",
    "India":"Indian"
}

individual_diversity_identifiers={}

for key in individual_diversity_keys:
    new_key=key.lower()
    individual_diversity_identifiers[new_key]=individual_diversity_keys[key]
    individual_diversity_identifiers[new_key.replace(" ", "_")]=individual_diversity_keys[key]
    individual_diversity_identifiers[new_key.replace(" ", "-")]=individual_diversity_keys[key]
    individual_diversity_identifiers[new_key.replace(" ", "")] = individual_diversity_keys[key]


def check_for_diversity_mention_in_page(url):
    print("scanning for diversity in "+str(url))
    page_text = get_visible_text_from_webpages(url).lower()
    diversity_list = [diversity_identifiers_for_companies[key] if key in page_text else "" for key in diversity_identifiers_for_companies]
    filtered_list = set(filter(lambda x:not x == "",diversity_list))
    return filtered_list

def check_for_diversity_mention_for_ind_in_page(url):
    print("scanning for leader diversity in "+str(url))
    page_text = get_visible_text_from_webpages(url).lower()
    diversity_list = [individual_diversity_identifiers[key] if key in page_text else "" for key in individual_diversity_identifiers]
    filtered_list = set(filter(lambda x:not x == "",diversity_list))
    return filtered_list

def get_list_of_urls_from_collected_cols(url_string):
    return url_string.replace("CompanyWebSites:","").replace(";RefWebSites:",",").split(",")

def get_urls_and_scan_pages(utl_string):
    list_of_urls=get_list_of_urls_from_collected_cols(utl_string)
    lst_of_lsts_of_diversity_per_page = [check_for_diversity_mention_in_page(eachUrl) for eachUrl in list_of_urls]
    identified_diversity=','.join(set(itertools.chain(*lst_of_lsts_of_diversity_per_page)))
    return identified_diversity

def get_urls_and_scan_pages_for_ind(url_string):
    if url_string == "":
        return ""
    list_of_urls=url_string.split(",")
    lst_of_lsts_of_diversity_per_page = [check_for_diversity_mention_for_ind_in_page(eachUrl) for eachUrl in list_of_urls]
    identified_diversity=','.join(set(itertools.chain(*lst_of_lsts_of_diversity_per_page)))
    return identified_diversity

async def get_diversity_info_from_company_urls_series(data_excel):
    return data_excel["company_info_urls"].apply(lambda x: str(get_urls_and_scan_pages(x)))

async def get_diversity_info_from_diversity_urls_series(data_excel):
    return data_excel["company_diversity_info_urls"].apply(lambda x: str(get_urls_and_scan_pages(x)))

async def get_urls_and_scan_pages_for_ind_info_series(data_excel):
    return data_excel["company_leadership_likedin_urls"].apply(lambda x: str(get_urls_and_scan_pages_for_ind(x)))


async def scan_urls_collected():
    data_excel = pd.read_excel('Hackathon_Data_MinorityWomenOwned_2022 withcompany_urls.xlsx')

    diversity_info_from_company_url,diversity_info_from_diversity_search,diversity_info_from_leader_linked_in_page=await asyncio.gather(get_diversity_info_from_company_urls_series(data_excel),
                         get_diversity_info_from_diversity_urls_series(data_excel),
                         get_urls_and_scan_pages_for_ind_info_series(data_excel))
    data_excel["diversity_info_from_company_core_urls"]=diversity_info_from_company_url
    data_excel["diversity_info_from_company_diversity_urls"]=diversity_info_from_diversity_search
    data_excel["diversity_info_from_leaders_linkedin_urls"]=diversity_info_from_leader_linked_in_page


    writer = pd.ExcelWriter('Hackathon_Data_MinorityWomenOwned_2022 withcompany_urls_and_info.xlsx', engine='xlsxwriter')
    data_excel.to_excel(writer,index=False)
    writer.save()


if __name__ == '__main__':
    # asyncio.run(scan_urls_collected())
    # list_of_urls=list(x[0] for x in google_search_results_and_desc("Grosvenor Building Services, Inc. diversity"))
    # for each_url in list_of_urls:
    #     print(each_url)
    #     print(check_for_diversity_mention_in_page(each_url))

    # print(check_for_diversity_mention_in_page("https://www.dnb.com/business-directory/company-profiles.cpy_inc.d3f8766c48e3701560244592f8a542f5.html"))
    print(individual_diversity_identifiers)
    print(diversity_identifiers_for_companies)