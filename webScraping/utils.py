from urllib.parse import urljoin

import requests
from bs4 import Comment, BeautifulSoup

from dto.transferObjects import LeaderInfo


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


def get_visible_text_and_images_from_webpages(leaderpage):
    leaderPage = requests.get(leaderpage)
    leader_text=text_from_html(leaderPage.text)
    soup = BeautifulSoup(leaderPage.text, 'html.parser')
    img_tags = soup.find_all('img')

    img_urls = [urljoin(leaderpage,img['src']) for img in img_tags]
    print(img_urls)
    imgs_content = [requests.get(eachURL).content for eachURL in img_urls]
    imgs_extns = [str(img_url).split(".")[-1] for img_url in img_urls]
    leaderInfo = LeaderInfo(leader_text,imgs_content,imgs_extns)
    return leaderInfo

def get_visible_text_from_webpages(leaderpage):
    leaderPage = requests.get(leaderpage)
    leader_text=text_from_html(leaderPage.text)
    return leader_text