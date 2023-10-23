import requests
from bs4 import BeautifulSoup
from utilities import scrape
from Session import Session

class Character:
    """
    Pulls information about an existing character from its profile ID. 
    Requires an existing authenticated session to access characters who may be authorise/logged-in users only.
    """
    def __init__(self,id,session):
        """
        __init__ method

        Arguments: 
        id (int): Character ID 
        session (Session): Used to access restricted character profiles.
        """
        self.id = id
        self.session = session.session
        self.char_stats = {}
        self.ownership_log = []
        self.favs = []
        self.comments = []

    def retrieve_char_stats(self):
        """
        Obtains information such as:
        - designer and creator of the character (if applicable, considering designer is an optinal field)
        - the date of creation
        - the number of Gallery, Library, World and Link items (left sidebar) [wip]
        - the number of comments and favourites (left sidebar underneath) [wip]
        """
        retrieve_char_stat_attributes = scrape(self.session, f"https://toyhou.se/{self.id}./", "dt", {"class": "field-title col-sm-4"})
        retrieve_char_stat_values = scrape(self.session, f"https://toyhou.se/{self.id}./", "dd", {"class": "field-value col-sm-8"})
        created_date = scrape(self.session, f"https://toyhou.se/{self.id}./", "abbr", {"class": "tooltipster datetime"}, all=False)["title"]
        retrieve_char_stat_values[0] = created_date
        for attribute, value in zip(retrieve_char_stat_attributes, retrieve_char_stat_values):
            try:
                self.char_stats[(attribute.text).strip()] = (value.text).strip()
            except:
                self.char_stats[(attribute.text).strip()] = (value).strip()        
        return self.char_stats
    
    def retrieve_char_log(self):
        """
        Obtains the ownership log of the character.
        """
        retrieve_char_transfer_date = scrape(self.session, f"https://toyhou.se/{self.id}./ownership/log", "td", {"class": "col-4 col-md-3"})
        retrieve_char_recipient = scrape(self.session, f"https://toyhou.se/{self.id}./ownership/log", "span", {"class": "display-user"})
        for date, recipient in zip(retrieve_char_transfer_date, retrieve_char_recipient[1:]):
            self.ownership_log.append({
                "transfer_date": (date.text).strip(),
                "transfer_recipient": (recipient.text).strip()
            })
        return self.ownership_log

    def retrieve_favs(self):
        """
        Obtains a list of who favourited the character.
        """
        retrieve_favourites_list = scrape(self.session, f"https://toyhou.se/{self.id}./favorites", "a", {"class": "btn btn-sm btn-default user-name-badge"})
        for favourite in retrieve_favourites_list:
            self.favs.append(favourite.text)
        return self.favs

    def retrieve_comments(self):
        """
        Obtains a list of comments, timestamps and their authors.
        """

    
    