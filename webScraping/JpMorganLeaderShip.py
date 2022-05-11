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
    leaderInfoList=list(map(lambda x: get_visible_text_and_images_from_webpages(x), leader_page_links))
    return leaderInfoList

if __name__ ==  '__main__':

    # print(getTextAboutExec("JpMorgan Chase"))
    company="JpMorgan Chase"
    list_of_leader_info_objects=getTextAboutExec(company)
    for index, leader_info_object in enumerate(list_of_leader_info_objects):
        file_name = company+"_eid_"+str(index)+".txt"
        print(file_name)
        for image_index,eachImage_content in enumerate(leader_info_object.image_content):
            img_file_name = company + "_img_"+str(image_index)+"_eid_" + str(index) + "."+leader_info_object.image_extn[image_index]
            print(img_file_name)
    # print(get_data_from_eah_leader_page("https://www.wellsfargo.com/about/corporate/governance/carr/"))