import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent



if __name__ == '__main__':

    text = """
   Executive Vice President, Chief Accounting Officer, and Controller
Wells Fargo & Company
Muneera Carr serves as executive vice president, chief accounting officer, and controller for Wells Fargo & Company. She manages accounting and reporting, corporate tax, and controllership activities such as financial controls, as well as oversight policies and processes for the company’s business groups and enterprise functions.
Muneera joined Wells Fargo as controller in 2020 and has more than 20 years of public accounting and financial services industry experience. Prior to Wells Fargo, Muneera served as executive vice president and chief financial officer with Comerica, Inc., where she led all areas of finance including: Corporate Treasury, Controllership, Investor Relations & Sustainability, Procurement, Real Estate, Planning & Forecasting, and Business Finance. Previously, she was Comerica’s chief accounting officer, where her responsibilities included Tax, Management Information Systems, and Planning & Forecasting. Before joining Comerica, Muneera served as a professional accounting fellow in the Office of the Chief Accountant at the United States Securities and Exchange Commission. She also led the accounting policy function at major banks, such as SunTrust and Bank of America, and served as an auditor with PricewaterhouseCoopers.
Muneera attended the University of Texas, where she graduated summa cum laude with a bachelor’s degree in business administration and accounting. She is a Certified Public Accountant. 
    """

    sent = preprocess(text)
    for each in sent:
        print(each)