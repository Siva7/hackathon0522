from urllib.parse import urljoin
from webScraping.GoogleSearch import google_search_results
from bs4 import BeautifulSoup
import requests

from webScraping.utils import  get_visible_text_and_images_from_webpages


def getLeaderPageLinksFor(company):
    wells_fargo_first_results=google_search_results(f"${company} leadership")[0]
    print(wells_fargo_first_results)
    leadership_page_requesr = requests.get(wells_fargo_first_results)
    soup_parser = BeautifulSoup(leadership_page_requesr.text,'html.parser')
    page_links = soup_parser.select('.button.primary.btn-link.chaseanalytics-track-link')
    leader_page_links = []
    for each_link in page_links:
        url = urljoin(wells_fargo_first_results,each_link.get('href'))
        leader_page_links.append(url)
    return leader_page_links


def getTextAboutExec(company):
    leader_page_links=getLeaderPageLinksFor(company)
    text_and_img_list=list(map(lambda x: get_visible_text_and_images_from_webpages(x), leader_page_links))
    return text_and_img_list

if __name__ ==  '__main__':

    print(getTextAboutExec("JpMorgan Chase"))
    # print(get_data_from_eah_leader_page("https://www.wellsfargo.com/about/corporate/governance/carr/"))