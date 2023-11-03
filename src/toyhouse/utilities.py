import requests
import string
import re

from bs4 import BeautifulSoup
def scrape(session, url, tag, class_attr, all=True):
    retrieve_url = session.get(url)
    retrieve_lxml = BeautifulSoup(retrieve_url.content, features="lxml")
    if all:
        retrieve_attributes = retrieve_lxml.find_all(tag, class_attr)
    else: 
        retrieve_attributes = retrieve_lxml.find(tag, class_attr)
    return retrieve_attributes



# Some illegal characters are present in the character's name (as in they are illegal in URLs). If they're kept in, it will break that link.
def strip_illegal(phrase):
    for character in phrase: 
        if character in """\/:*?"<>|() """:
            phrase = phrase.replace(character,"-")
        elif character not in string.ascii_letters and character not in string.digits:
            phrase = phrase.replace(character, "")
    phrase = re.sub('\-\-+', '-', phrase)
    return phrase.lower()
# FIX THIS TO REMOVE THE TRAILING DASH IF THE LAST CHARACTER IS ILLEGAL
# Note: Low priority. Links still work with the trailing dash.

# The way Toyhouse lays out characters is similar whether you're looking at someone's owned characters, their favourited ones, their designs... Even in the characters viewable in Worlds.
# Basically, anywhere characters are present, they are shown in this default 'card' style showing the character's picture, name, favourites/pictures/comments/links etc. 
# We can scrape specifically for this 'character object' and return the primary attributes (name, ID, and full link (the full URl includes the character's name, but that's not required.))
# As long as the link is something like 'https://toyhou.se/<id>.<name>' (note the presence of the full stop) it should work.
# Still, for the sake of presentation, it's best to include the name.
# Note: Make extra a compulsory parameter for including the folder that the OC is located in, since it's already included in favourites. This means we will no longer be using folder:all anymore.
def char_object(session, url, output, extra=False):
    try:
        max_pages = scrape(session, url ,"a", {"class": "page-link"})[-2].text
    except:
        max_pages = 1
    for i in range(1, int(max_pages)+1):
        retrieve_characters = scrape(session, f"{url}?page={i}","a", {"class": "btn btn-sm btn-primary character-name-badge"})
        if extra:
            for character in retrieve_characters:
                output.append(
                    ((character.text).strip(), 
                        int((character.get('href')[1:]).split('.',1)[0]),
                        f"https://toyhou.se/{int((character.get('href')[1:]).split('.',1)[0])}." + strip_illegal((character.text).strip()),
                        extra
                        ))
        else:
            for character in retrieve_characters:
                output.append(
                    ((character.text).strip(), 
                        int((character.get('href')[1:]).split('.',1)[0]),
                        f"https://toyhou.se/{int((character.get('href')[1:]).split('.',1)[0])}." + strip_illegal((character.text).strip())
                        ))


    return output 