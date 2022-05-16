from azure.storage.blob import BlobServiceClient
import pandas as pd
import os
import pathlib
import sys

def rmdir(directory):
    directory = pathlib.Path(directory)
    if directory.exists():
        for item in directory.iterdir():
            if item.is_dir():
                rmdir(item)
            else:
                item.unlink()
        directory.rmdir()

def combine_web_scrapping_output_files():
    conn_string=sys.argv[1]
    temp_cache = "temp_cache_for_data_extract_from_azure"
    blob_service_client = BlobServiceClient.from_connection_string(conn_string)
    container_client = blob_service_client.get_container_client("datadump")
    list_blobs = container_client.list_blobs()
    rmdir(temp_cache)
    os.mkdir(temp_cache)

    stat_files = []
    excel_files = []
    for blob in list_blobs:
        each_file = blob.name
        blob_client_instance = blob_service_client.get_blob_client("datadump",each_file,snapshot=None)

        if r".txt" in each_file and r"0_1." not in each_file:
            stat_files.append(each_file)
            with open(f"{temp_cache}/{each_file}", "wb") as my_blob:
                blob_data = blob_client_instance.download_blob()
                blob_data.readinto(my_blob)

        if r".xlsx" in each_file and r"0_1." not in each_file:
            excel_files.append(each_file)
            with open(f"{temp_cache}/{each_file}", "wb") as my_blob:
                blob_data = blob_client_instance.download_blob()
                blob_data.readinto(my_blob)

        result_df = pd.DataFrame()
        for each_excel in excel_files:
            result_df=result_df.append(pd.read_excel(f"{temp_cache}/{each_excel}"),ignore_index=True)

        writer = pd.ExcelWriter(f"{temp_cache}/Combined_WebScraping_Info_hack2022.xlsx",
                                engine='xlsxwriter')
        result_df.to_excel(writer, index=False)
        writer.save()

        google_api_call=0
        uris_analyzed=0
        web_pages_analyzed=0
        for each_stats_file in stat_files:
            text_file = open(f"{temp_cache}/{each_stats_file}", "r")
            data = text_file.read()
            text_file.close()
            lines=list(filter(lambda x:not x.strip() == "",data.split("\n")))
            google_api_call+=int(lines[0].strip().split("=$")[1])
            uris_analyzed += int(lines[1].strip().split("=$")[1])
            web_pages_analyzed += int(lines[2].strip().split("=$")[1])


        outout_container_client = blob_service_client.get_container_client("webscrappingconsolidatedoutput")
        # container_client.upload_blob(name=file_name, data=data)
        # blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

        with open(f"{temp_cache}/Combined_WebScraping_Info_hack2022.xlsx", "rb") as data:
            outout_container_client.upload_blob(name="WebScrappingResults2022.xlsx", data=data,overwrite=True)


        stats_data= f"""
            Total number of calls to google search [APi]={google_api_call}
            Total number of urls Analyzed={uris_analyzed}
            Total number of Web Pages Analyzed={web_pages_analyzed}
            """

        outout_container_client.upload_blob(name="WebScrapping_stats.txt", data=stats_data,overwrite=True)


if __name__ == '__main__':
    combine_web_scrapping_output_files()

    # combine_web_scrapping_output_files("DefaultEndpointsProtocol=https;AccountName=codesanddoc;AccountKey=ydz3XndrMKSX4aYFOc/TQfr8C6gj2/jQddc75+7FNshlqIGf5bieFfJvDg0M6YFCvGHYwOcU/CKm+AStywykNA==;EndpointSuffix=core.windows.net")