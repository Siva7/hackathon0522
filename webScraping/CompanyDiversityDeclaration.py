from webScraping.GoogleSearch import google_search_results_and_desc
from webScraping.utils import get_visible_text_from_webpages

diversity_identifiers = {"national minority supplier development council": "women",
                         "nmsdc": "women",
                         "women’s business enterprise national council": "women",
                         "wbenc": "women",
                         "national veteran business development council": "veteran",
                         "nvdbc": "veteran",
                         "national veteran-owned business association": "veteran",
                         "navoba": "veteran",
                         "national lbgt chamber of commerce": "lgbtq+",
                         "nglcc": "lgbtq+",
                         "women led": "women",
                         "racially diverse" : "racial",
                         "women diversity": "women",
                         "lgbt": "lgbtq+",
                         "veteran diversity": "veteran",
                         "veteran employees":"veteran",
                         "veteran led": "veteran",
                         "women business owners":"women"}


def check_for_diversity_mention_in_page(url):
    page_text = get_visible_text_from_webpages(url).lower()
    diversity_recog=[]
    for key in diversity_identifiers:
        if key in page_text:
            diversity_recog.append(diversity_identifiers[key])
    return diversity_recog

if __name__ == '__main__':
    list_of_urls=list(x[0] for x in google_search_results_and_desc("wellsfargo diversity"))
    for each_url in list_of_urls:
        print(each_url)
        print(check_for_diversity_mention_in_page(each_url))
