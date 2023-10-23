import requests
from bs4 import BeautifulSoup
def scrape(session, url, tag, class_attr):
    retrieve_url = session.get(url)
    retrieve_lxml = BeautifulSoup(retrieve_url.content, features="lxml")
    retrieve_attributes = retrieve_lxml.find_all(tag, class_attr)
    return retrieve_attributes