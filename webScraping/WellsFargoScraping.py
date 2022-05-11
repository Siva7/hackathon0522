from urllib.parse import urljoin
from webScraping.GoogleSearch import google_search_results
from bs4 import BeautifulSoup
import requests
from bs4.element import Comment

def getLeaderPageLinksFor(company):
    wells_fargo_first_results=google_search_results("wellsfargo leadership")[0]
    print(wells_fargo_first_results)
    leadership_page_requesr = requests.get(wells_fargo_first_results)
    soup_parser = BeautifulSoup(leadership_page_requesr.text,'html.parser')
    page_links = soup_parser.find_all('a',attrs={'type':'componentlink'})
    leader_page_links = []
    for each_link in page_links:
        url = urljoin(wells_fargo_first_results,each_link.get('href'))
        print(url)
        if 'governance' in url:
            leader_page_links.append(url)
    return leader_page_links

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def get_data_from_eah_leader_page(leaderpage):
    lederPage = requests.get(leaderpage)
    leader_text=text_from_html(lederPage.text)
    return leader_text






if __name__ ==  '__main__':
    print(getLeaderPageLinksFor('wellsfargo'))
    # print(get_data_from_eah_leader_page("https://www.wellsfargo.com/about/corporate/governance/carr/"))