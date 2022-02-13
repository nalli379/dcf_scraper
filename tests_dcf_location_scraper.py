import unittest

from requests.exceptions import Timeout
from dcf_location_scraper import *
from urllib.request import urlopen
from bs4 import BeautifulSoup

class TestDCFDirectory(unittest.TestCase):
    bs_object = None
    def setUpClass():
        global bs_object
        url = "http://dcflist.valpak.co.uk/?search=7"
        bs_object = BeautifulSoup(urlopen(url), "lxml")
    
    def test_titleText(self):
        global bs_object
        pageTitle = bs_object.find("h1").get_text()
        self.assertEqual("Designated Collection Facilities", pageTitle)
    
    def test_tableExists(self):
        global bs_object
        table = bs_object.find_all('table')
        self.assertIsNotNone(table)
        

# class DCFScraperTestException(unittest.TestCase):
"""
the DCL site url accepts any type of search query which all direct to an empty page
for this test, the function was adapted to accept an input url directly.
"""
    # def test_dcf_scraper_exception(self):
    #     url="https://www.laaldsdkfdsnklfds.com/"
    #     self.assertRaises(Exception, dcf_scraper(url))
    
class DCFScraperTestMain(unittest.TestCase):
    
    def test_dcf_scraper_no_results1(self):
        expect = 0
        result = dcf_scraper("Q")
        self.assertEqual(expect, result)
    
    def test_dcf_scraper_no_results2(self):
        result = dcf_scraper("fmkdslfkdsl")
        self.assertIsNotNone(result)
    
    def test_dcf_scraper_results(self):
        expect = 1
        result = dcf_scraper("7")
        self.assertEqual(expect, result)
    
    def test_dcf_scraper_results(self):
        expect = 75
        result =dcf_scraper("B")
        self.assertEqual(expect, result)
    

class RegexTestCases(unittest.TestCase):
    def test_dcf_scraper_clean_regex(self):
        postcode1='kt3*$$7by^^'
        self.assertRegex(postcode1,r"[^a-zA-Z0-9]")
    
    def test_dcf_scraper_clean_regex2(self):
        postcode2='£^&TW11*$9PE@^^'
        self.assertRegex(postcode2,r"[^a-zA-Z0-9]")


class PostcodeAPITest(unittest.TestCase):
    
    def test_postcode_api_request1(self):
        test_dictionary1 = {"Turriff Recycling Centre": "AB534AZ"}
        result = postcode_api_request(test_dictionary1)
        self.assertIsNotNone(result)
    
    def test_postcode_api_request2(self):
        test_dictionary2 = {"WEEE MUST RECYCLE": "B775DF"}
        expect = 1
        result = postcode_api_request(test_dictionary2)
        self.assertEqual(expect, result)
    
    def test_postcode_api_request3(self):
        test_dictionary3 = {"Invalid": "T117DF"}
        expect = 0
        result = postcode_api_request(test_dictionary3)
        self.assertEqual(expect, result)
    
    def test_postcode_api_request4(self):
        test_dictionary4 = {"Invalid": "XR578F"}
        result = postcode_api_request(test_dictionary4)
        self.assertIsNotNone(result)



if __name__ == '__main__':
    unittest.main()
    