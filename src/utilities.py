import requests
from bs4 import BeautifulSoup
def scrape(session, url, tag, class_attr, all=True):
    retrieve_url = session.get(url)
    retrieve_lxml = BeautifulSoup(retrieve_url.content, features="lxml")
    if all:
        retrieve_attributes = retrieve_lxml.find_all(tag, class_attr)
    else: 
        retrieve_attributes = retrieve_lxml.find(tag, class_attr)
    return retrieve_attributes


def char_object(session, url, output):
    try:
        max_pages = scrape(session, url ,"a", {"class": "page-link"})[-2].text
    except:
        max_pages = 1
    for i in range(1, int(max_pages)+1):
        retrieve_characters = scrape(session, f"{url}?page={i}","a", {"class": "btn btn-sm btn-primary character-name-badge"})
        for character in retrieve_characters:
            output.append(
                ((character.text).strip(), 
                    int((character.get('href')[1:]).split('.',1)[0]),
                    f"https://toyhou.se/{int((character.get('href')[1:]).split('.',1)[0])}.{(character.text).strip()}"
                    ))
    return output 