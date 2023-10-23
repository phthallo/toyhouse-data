import requests
from bs4 import BeautifulSoup
from utilities import scrape

class Session:
    """
    Establishes a new Toyhou.se session for information about the authenticated user.
    """
    def __init__(self,username,password):
        """
        __init__ method

        Arguments:
        username (str): Toyhou.se username
        password (str): Toyhou.se password
        """
        self.session = requests.Session()
        self.session.verify = False
        self.username = username
        self.password = password
        self.characters = []
        self.stats = []
        self.stat_values = []

    def auth(self):
        """
        Authenticates the user using credentials provided previously. 
        (Note that it doesn't actually check if they are correct at this stage.)
        """
        retrieve_url = self.session.get("https://toyhou.se/~account/login")
        retrieve_lxml = BeautifulSoup(retrieve_url.content, features="lxml")
        csrf = retrieve_lxml.find("meta", {"name":"csrf-token"})["content"]
        creds = {"username": self.username,
                "password": self.password,
                "_token": csrf}
        self.session.post("https://toyhou.se/~account/login", data=creds)
        return "Attempting to authenticate as " + self.username
        
    def retrieve_char(self):
        """
        Retrieves the logged-in user's characters and returns a list containing tuples of form `(charactername, characterID)`.
        """
        if self.session is None:
            raise Exception("AuthenticationError: You must be logged in to retrieve characters!")
        try:
            retrieve_url = self.session.get(f"https://toyhou.se/{self.username}/characters/folder:all")
            try:
                max_pages = BeautifulSoup(retrieve_url.content, features="lxml").find_all("a", {"class": "page-link"})[-2].text
            except:
                max_pages = 1
            for i in range(1, int(max_pages)+1):
                retrieve_characters = scrape(self.session, f"https://toyhou.se/{self.username}/characters/folder:all?legacy=0&page={i}","a", {"class": "btn btn-sm btn-primary character-name-badge"})
                for character in retrieve_characters:
                    self.characters.append(
                        (
                            (character.text).strip(),
                            int((character.get('href')[1:]).split('.',1)[0])
                            )
                            )
        except: 
            raise Exception("ParseError: Parsing was unsuccessful. Please verify that your login credentials are correct.")
        return self.characters
    
    def retrieve_stats(self):
        """
        Retrieves the logged-in user's statistics and username log. Even though some can be hidden, all statistics are visible (provided you are viewing your own profile.)
        """
        retrieve_stat_attributes = scrape(self.session, f"https://toyhou.se/{self.username}/stats", "span", {"class": "custom-control-description ml-1"})
        retrieve_stat_values = scrape(self.session, f"https://toyhou.se/{self.username}/stats", "dd", {"class": "field-value col-lg-9 col-md-8"})
        # Because the last-logged-in time is relative to when you're viewing the page (e.g 6 seconds ago, 2 weeks ago), we need to search specifically for the actual date (usually viewable by tooltip).
        last_logged_in = (BeautifulSoup(self.session.get(f"https://toyhou.se/{self.username}/stats").content, features="lxml")).find("abbr", {"class": "tooltipster datetime"})["title"]
        for statistic in retrieve_stat_attributes:
            self.stats.append(statistic.text)
        for statistic_value in retrieve_stat_values:
            self.stat_values.append((statistic_value.text).strip())
        self.stat_values.insert(1, last_logged_in)
        return dict(zip(self.stats, self.stat_values))
