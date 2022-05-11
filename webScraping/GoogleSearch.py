from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

def google_search_results(query):
    web_page = requests.get("http://www.google.com/search?q="+quote_plus(query))
    sour_parsed = BeautifulSoup(web_page.text,'html.parser')
    links = sour_parsed.findAll("a")

    search_result_links=[]
    for link in links:
        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href:
             search_result_links.append(link.get('href').split("?q=")[1].split("&sa=U")[0])
    return search_result_links


if __name__ == "__main__":
    print(google_search_results("wellsfargo leadership"))