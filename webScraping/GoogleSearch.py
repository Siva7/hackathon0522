from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

from webScraping.utils import counter

google_search_count=0

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


def google_search_results_and_desc(query):
    counter.google_search_count+=1
    web_page = requests.get("http://www.google.com/search?q="+quote_plus(query))
    sour_parsed = BeautifulSoup(web_page.text,'html.parser')
    links = sour_parsed.findAll("a")

    search_result_links=[]
    for link in links:

        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href:
            search_result_links.append(
                (link.get('href').split("?q=")[1].split("&sa=U")[0],
                    link.find('h3').text if link.find('h3') else ""
                ))
    return search_result_links

if __name__ == "__main__":
    print(google_search_results_and_desc("wellsfargo leadership"))