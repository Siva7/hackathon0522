from webScraping.GoogleSearch import google_search_results, google_search_results_and_desc
from  cleanco import basename
import pandas as pd
import tldextract
import asyncio
def if_url_belongs_to_company(company_name,url_and_desc):
    url,desc=url_and_desc
    tld_extract = tldextract.extract(url.lower())
    clean_url = tld_extract.subdomain + tld_extract.domain
    clean_url = clean_url.replace("www","").replace("http","")
    clean_url = ''.join(char for char in clean_url if char.isalnum())
    company_basename = basename(company_name).lower()
    company_basename = ''.join(char for char in company_basename if char.isalnum())
    short_form = "".join([word[0] for word in company_basename])
    full_name = company_basename.replace(" ","")
    if company_name.lower() in clean_url:
        return True
    if short_form in clean_url:
        return True
    if full_name in clean_url:
        return True
    for word in company_basename.split(" "):
        if word in clean_url:
            return True
    return False

def if_url_has_company_reference(company_name,url_and_desc):
    url,desc=url_and_desc
    desc=''.join(char for char in desc if char.isalnum()).lower().replace(" ","")
    company_basename = basename(company_name).lower()
    company_basename = ''.join(char for char in company_basename if char.isalnum())
    full_name = company_basename.replace(" ", "")
    if full_name in desc:
        return True
    else:
        return False
def get_company_and_ref_websites_urls_for_tag(company,tag):
    print("Analyzing Google Search results for " + company +" "+tag)
    search_results_with_desc = google_search_results_and_desc(company)
    # print(company+" "+tag+" google search results")
    # print(search_results_with_desc)
    company_website_urls_descs = list(filter(lambda x:if_url_belongs_to_company(company,x),search_results_with_desc))
    company_url_string = "CompanyWebSites:"+",".join([company_url_desc[0] for company_url_desc in company_website_urls_descs])
    ref_website_urls_descs = list(filter(lambda x:if_url_has_company_reference(company,x),search_results_with_desc))

    all_possible_ref_urls = [ref_url_desc[0] for ref_url_desc in ref_website_urls_descs]
    ref_urls_not_in_web_urls = list(filter(lambda x:x not in company_url_string,all_possible_ref_urls))
    ref_url_string=";RefWebSites:"+",".join(ref_urls_not_in_web_urls)

    # print(company+" "+tag+" google search results - identified as company url")
    # print(company_url_string+ref_url_string)
    return company_url_string+ref_url_string

def get_company_website_urls(company):
    print("Analyzing Google Search results for "+company)
    search_results_with_desc = google_search_results_and_desc(company)
    # print(company+" google search results")
    # print(search_results_with_desc)
    company_website_urls_descs = list(filter(lambda x:if_url_belongs_to_company(company,x),search_results_with_desc))
    company_url_string = "CompanyWebSites:"+",".join([company_url_desc[0] for company_url_desc in company_website_urls_descs])
    ref_website_urls_descs = list(filter(lambda x:if_url_has_company_reference(company,x),search_results_with_desc))

    all_possible_ref_urls = [ref_url_desc[0] for ref_url_desc in ref_website_urls_descs]
    ref_urls_not_in_web_urls = list(filter(lambda x:x not in company_url_string,all_possible_ref_urls))
    ref_url_string=";RefWebSites:"+",".join(ref_urls_not_in_web_urls)
    #  print(company+" google search results - identified as company url")
    # print(company_url_string+ref_url_string)
    return company_url_string+ref_url_string


async def get_company_info_url_series(data_excel):
    series = data_excel["dunsName"].apply(lambda x:str(get_company_website_urls(x)))
    return series

async def get_company_diversity_info_url_series(data_excel):
    series = data_excel["dunsName"].apply(lambda x: str(get_company_and_ref_websites_urls_for_tag(x," diversity")))
    return series

async def get_company_leadership_info_url_series(data_excel):
    series = data_excel["dunsName"].apply(lambda x: str(get_company_and_ref_websites_urls_for_tag(x, " leadership")))
    return series
async def gather_info_from_web():
    data_excel = pd.read_excel('D:\IT\Apps\IntelProjects\Hackathon_2022\hackathonMay22\Hackathon_Data_MinorityWomenOwned_2022 v1.xlsx')
    data_excel = data_excel.loc[:10,:]

    info_series,divesity_series,leadership_series=await asyncio.gather(get_company_info_url_series(data_excel),
                         get_company_diversity_info_url_series(data_excel),
                         get_company_leadership_info_url_series(data_excel))
    data_excel["company_info_urls"]=info_series
    data_excel["company_diversity_info_urls"] =divesity_series
    data_excel["company_leadership_info_urls"] = leadership_series


    writer = pd.ExcelWriter('D:\IT\Apps\IntelProjects\Hackathon_2022\hackathonMay22\Hackathon_Data_MinorityWomenOwned_2022 withcompany_urls.xlsx', engine='xlsxwriter')
    data_excel.to_excel(writer,index=False)
    writer.save()

if __name__ == '__main__':

    # print(read_excel)
    # data_excel["company_info_urls"]=data_excel["dunsName"].apply(lambda x:str(get_company_website_urls(x)))
    # data_excel["company_diversity_info_urls"] = data_excel["dunsName"].apply(lambda x: str(get_company_and_ref_websites_urls_for_tag(x," diversity")))
    # data_excel["company_leadership_info_urls"] = data_excel["dunsName"].apply(lambda x: str(get_company_and_ref_websites_urls_for_tag(x, " leadership")))
    asyncio.run(gather_info_from_web())
