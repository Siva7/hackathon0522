import pandas as pd
import pathlib
import os
from azure.storage.blob import BlobServiceClient
from itertools import chain
temp_cache_dir="temp_dir_to_combine_results"

def rmdir(directory):
    directory = pathlib.Path(directory)
    if directory.exists():
        for item in directory.iterdir():
            if item.is_dir():
                rmdir(item)
            else:
                item.unlink()
        directory.rmdir()

def take_output_decision(x):
    web_scrap_company_url=""
    web_scrape_company_diversity_url=""
    nlp_gender=""
    nlp_race=""
    try:
        web_scrap_company_url=x["diversity_info_from_company_core_urls"]
    except:
        web_scrap_company_url=""
    try:
        web_scrape_company_diversity_url=x["diversity_info_from_company_diversity_urls"]
    except:
        web_scrape_company_diversity_url=""
    try:
        nlp_gender=x["gender"]
    except:
        nlp_gender=""
    try:
        nlp_race=x["race"]
    except:
        nlp_race=""
    iswomanowned=0
    minorityowneddesc=""
    web_scrap_company_url=str(web_scrap_company_url)
    web_scrape_company_diversity_url=str(web_scrape_company_diversity_url)
    if web_scrap_company_url.lower()=="nan":
        web_scrap_company_url=""
    if web_scrape_company_diversity_url.lower()=="nan":
        web_scrape_company_diversity_url=""


    webScrappingDetails = ','.join(set(chain(set(web_scrap_company_url.strip().split(",")),set(web_scrape_company_diversity_url.split(",")))))
    webScrappingDetails=webScrappingDetails.lower()
    if "women" in webScrappingDetails or nlp_gender == 1:
        iswomanowned=1
    webScrappingDetails=webScrappingDetails.replace("women","")
    if (not webScrappingDetails == ""):
        minorityowneddesc=webScrappingDetails
    else:
        minorityowneddesc=nlp_race
    return f"{iswomanowned}#{minorityowneddesc}"


def getFinalResult():
    conn_string="DefaultEndpointsProtocol=https;AccountName=codesanddoc;AccountKey=ydz3XndrMKSX4aYFOc/TQfr8C6gj2/jQddc75+7FNshlqIGf5bieFfJvDg0M6YFCvGHYwOcU/CKm+AStywykNA==;EndpointSuffix=core.windows.net"
    print("Process Started...")
    rmdir(temp_cache_dir)
    os.mkdir(temp_cache_dir)

    blob_service_client = BlobServiceClient.from_connection_string(conn_string)

    print("Extracting WebScrapping Info")
    webscrapping_blob_client = blob_service_client.get_blob_client("webscrappingconsolidatedoutput","WebScrappingResults2022.xlsx",snapshot=None)
    with open(f"{temp_cache_dir}/WebScrappingResults2022.xlsx", "wb") as my_blob:
        blob_data = webscrapping_blob_client.download_blob()
        blob_data.readinto(my_blob)

    nlp_blob_client = blob_service_client.get_blob_client("output",
                                                                   "Hackathon_Data_MinorityWomenOwned_2022_0_59776.xlsx",
                                                                   snapshot=None)
    print("Extracting NLP Info")
    with open(f"{temp_cache_dir}/Hackathon_Data_MinorityWomenOwned_2022_0_59776.xlsx", "wb") as my_blob:
        blob_data = nlp_blob_client.download_blob()
        blob_data.readinto(my_blob)

    print("Merging both DataSets..")
    web_scrapping_excel = pd.read_excel(f"{temp_cache_dir}/WebScrappingResults2022.xlsx").loc[:,["dunsNum",'company_info_urls',
       'company_diversity_info_urls', 'company_leadership_likedin_urls',
       'diversity_info_from_company_core_urls',
       'diversity_info_from_company_diversity_urls',
       'diversity_info_from_leaders_linkedin_urls']]
    nlp_excel = pd.read_excel(f"{temp_cache_dir}/Hackathon_Data_MinorityWomenOwned_2022_0_59776.xlsx").loc[:,['dunsnum', 'dunsname', 'county', 'streetaddress', 'city', 'state',
       'zip', 'phone', 'executivecontact1', 'executivecontact2',
       'iswomanowned', 'minorityowneddesc', 'executivecontact1_name',
       'executivecontact1_job', 'executivecontact2_name',
       'executivecontact2_job', 'executivecontact1_fname',
       'executivecontact1_lname', 'executivecontact2_fname',
       'executivecontact2_lname', 'executive1_gender_x', 'probability_x',
       'executive2_gender_x', 'rowindex', 'gender', 'executive1_race',
       'executive2_race', 'race']]

    print(web_scrapping_excel.columns)
    print(nlp_excel.columns)

    joined_df = nlp_excel.merge(web_scrapping_excel,how="left",left_on='dunsnum', right_on='dunsNum')
    print(joined_df.columns)
    merged_df = joined_df.loc[:,['dunsnum', 'dunsname', 'county', 'streetaddress', 'city', 'state',
           'zip', 'phone', 'executivecontact1', 'executivecontact2',
           'iswomanowned', 'minorityowneddesc', 'company_info_urls',
           'company_diversity_info_urls', 'company_leadership_likedin_urls',
           'diversity_info_from_company_core_urls',
           'diversity_info_from_company_diversity_urls',
           'diversity_info_from_leaders_linkedin_urls', 'executivecontact1_name',
           'executivecontact1_job', 'executivecontact2_name',
           'executivecontact2_job', 'executivecontact1_fname',
           'executivecontact1_lname', 'executivecontact2_fname',
           'executivecontact2_lname', 'executive1_gender_x', 'probability_x',
           'executive2_gender_x', 'rowindex', 'gender', 'executive1_race',
           'executive2_race', 'race']]

    print("-----------------------")
    print(merged_df.columns)


    merged_df[['iswomanowned', 'minorityowneddesc']]=merged_df.apply(lambda x:take_output_decision(x),axis=1).str.split("#",expand=True)

    print("Persisting Detailed report to Local...")
    writer = pd.ExcelWriter(f"{temp_cache_dir}/Final_Result_With_Details_hack2022.xlsx",
                            engine='xlsxwriter')
    merged_df.to_excel(writer, index=False)
    writer.save()

    print("Persisting Final  report to Local...")
    select_result_df = merged_df.loc[:,['dunsnum', 'dunsname', 'county', 'streetaddress', 'city', 'state',
           'zip', 'phone', 'executivecontact1', 'executivecontact2',
           'iswomanowned', 'minorityowneddesc']]

    writer = pd.ExcelWriter(f"{temp_cache_dir}/Final_Result_hack2022.xlsx",
                            engine='xlsxwriter')
    select_result_df.to_excel(writer, index=False)
    writer.save()

    output_container_client = blob_service_client.get_container_client("finalresult")

    print("Persisting Final  report to Storage Account...")
    with open(f"{temp_cache_dir}/Final_Result_hack2022.xlsx", "rb") as data:
        output_container_client.upload_blob(name="Final_Result_hack2022.xlsx", data=data, overwrite=True)

    print("Persisting Detail report to Storage Account...")
    with open(f"{temp_cache_dir}/Final_Result_With_Details_hack2022.xlsx", "rb") as data:
        output_container_client.upload_blob(name="Final_Result_With_Details_hack2022.xlsx", data=data, overwrite=True)



if __name__=='__main__':
    getFinalResult()