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
        self.char_stats = []
        self.favs = []
        self.comments = []

    def retrieve_char_stats(self):
        """
        Obtains information such as character designer, date of creation and ownership log.
        """

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

    
    