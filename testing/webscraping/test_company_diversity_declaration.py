from unittest import TestCase

from webScraping.CompanyDiversityDeclaration import check_for_diversity_mention_in_page, \
    individual_diversity_identifiers, diversity_identifiers_for_companies, check_for_diversity_mention_for_ind_in_page, \
    get_list_of_urls_from_collected_cols, get_urls_and_scan_pages, get_urls_and_scan_pages_for_ind


class TestCompanyDiversityDeclaration(TestCase):
    def test_check_for_diversity_mention_in_page(self):
       list_returned= check_for_diversity_mention_in_page("https://www.wellsfargo.com/about/diversity/diversity-and-inclusion/")
       self.assertEquals("racial,veteran",','.join(sorted(list_returned)))


    def test_individual_diversity_identifiers(self):
        print(individual_diversity_identifiers)
        print(str(len(individual_diversity_identifiers)))
        self.assertEquals(19,len(individual_diversity_identifiers))

    def test_diversity_identifiers_for_companies(self):
        print(diversity_identifiers_for_companies)
        print(str(len(diversity_identifiers_for_companies)))
        self.assertEquals(134,len(diversity_identifiers_for_companies))


    def test_check_for_diversity_mention_for_ind_in_page(self):
        list_returned = check_for_diversity_mention_for_ind_in_page(
            "https://www.wellsfargo.com/about/diversity/diversity-and-inclusion/")
        self.assertEquals("African American,asian,hispanic", ','.join(sorted(list_returned)))

    def test_get_list_of_urls_from_collected_cols(self):
        self.assertEquals("a,b,c",
                          ','.join(get_list_of_urls_from_collected_cols("a,b,c").split(",")))


    def test_get_urls_and_scan_pages(self):
        self.assertEquals("racial,veteran",get_urls_and_scan_pages("https://www.wellsfargo.com/about/diversity/diversity-and-inclusion/"))


    def test_get_urls_and_scan_pages_for_ind(self):
        self.assertEquals("African American,asian,hispanic", str(get_urls_and_scan_pages_for_ind(
            "https://www.wellsfargo.com/about/diversity/diversity-and-inclusion/")))
