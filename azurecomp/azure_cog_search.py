from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import json

def search():
    service_name = "azurecogsearch1234"
    admin_key = "193B56F435C271DD7C9C79F071CE99B7"
    index_name = "azureblob-index"
    # Create an SDK client
    endpoint = "https://{}.search.windows.net/".format(service_name)
    # admin_client = SearchIndexClient(endpoint=endpoint,
    #                        index_name=index_name,
    #                        credential=AzureKeyCredential(admin_key))
    search_client = SearchClient(endpoint=endpoint,
                                 index_name=index_name,
                                 credential=AzureKeyCredential(admin_key))

    results = search_client.search(search_text="*",select="pii_entities,locations,people,metadata_storage_name",  include_total_count=True)
    print('Total Documents Matching Query:', results.get_count())
    for result in results:
        # print(str(result))
        json_results=json.loads(str(result).replace('\'','\"').replace('None','\"None\"'))
        # print(json_results)
        for eachValue in json_results['pii_entities']:
            print(eachValue)
        for eachValue in json_results['locations']:
            print(eachValue)
        for eachValue in json_results['people']:
                print(eachValue)
        print(json_results['metadata_storage_name'])



if __name__ == '__main__':
    search()