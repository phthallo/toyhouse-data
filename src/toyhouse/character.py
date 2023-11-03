import requests
from bs4 import BeautifulSoup
from toyhouse.utilities import *
from toyhouse.session import *

class Character:
    """
    Pulls information about an existing character from its profile ID. 
    Requires an existing authenticated session to access characters who may be authorise/logged-in users only.
    """
    def __init__(self,session, id):
        """
        __init__ method

        Arguments: 
        session (Session): Used to access restricted character profiles.
        id (int): Character ID 
        """
        self._authenticated = session.authenticated
        if self._authenticated is False:
            raise Exception("AuthError: You must be logged in to retrieve information about users")
        if isinstance(session, Session) != True: 
            raise ValueError(f"{session} is not of class Session")
        self.id = id
        self.session = session.session
        self._char_statistics = {}
        self._ownership_log = []
        self._favs = []
        self._comments = []

    @property
    def char_stats(self):
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
                self._char_statistics[(attribute.text).strip()] = (value.text).strip()
            except:
                self._char_statistics[(attribute.text).strip()] = (value).strip()        
        return self._char_statistics
    
    @property
    def char_log(self):
        """
        Obtains the ownership log of the character.
        """
        retrieve_char_transfer_date = scrape(self.session, f"https://toyhou.se/{self.id}./ownership/log", "td", {"class": "col-4 col-md-3"})
        retrieve_char_recipient = scrape(self.session, f"https://toyhou.se/{self.id}./ownership/log", "span", {"class": "display-user"})
        for date, recipient in zip(retrieve_char_transfer_date, retrieve_char_recipient[1:]):
            self._ownership_log.append(
                ((date.text).strip(),
                (recipient.text).strip())
            )
        return self._ownership_log

    @property
    def char_favs(self):
        """
        Obtains a list of who favourited the character.
        """
        retrieve_favourites_list = scrape(self.session, f"https://toyhou.se/{self.id}./favorites", "a", {"class": "btn btn-sm btn-default user-name-badge"})
        for favourite in retrieve_favourites_list:
            self._favs.append(favourite.text)
        return self._favs

    @property
    def char_content(self):
        """
        Obtains the raw content of the character's profile. 
        """
        # grab basic info + its parameters, store as dict w/ zip
        # then grab HTML content

    #def char_comments(self):
    #    """
    #    Obtains a list of comments, timestamps and their authors.
    #    """

    
    