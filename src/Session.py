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
        self.username = username
        self.password = password
        self.characters = []
        self.statistics = {}
        self.username_log = []

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
        
    def chars(self):
        """
        Retrieves the logged-in user's characters and returns a list containing dictionaries of format {"name": <char_name>, "id": <char_id>}.
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
                        {
                            "name":(character.text).strip(),
                            "id": int((character.get('href')[1:]).split('.',1)[0])
                        }
                            )
        except: 
            raise Exception("ParseError: Parsing was unsuccessful. Please verify that your login credentials are correct.")
        return self.characters
    
    def stats(self):
        """
        Retrieves the logged-in user's statistics. Even though some can be hidden, all statistics are visible (provided you are viewing your own profile.)
        """
        retrieve_stat_attributes = scrape(self.session, f"https://toyhou.se/{self.username}/stats", "span", {"class": "custom-control-description ml-1"})
        retrieve_stat_values = scrape(self.session, f"https://toyhou.se/{self.username}/stats", "dd", {"class": "field-value col-lg-9 col-md-8"})
        # Because the last-logged-in time is relative to when you're viewing the page (e.g 6 seconds ago, 2 weeks ago), we need to search specifically for the actual date (usually viewable by tooltip).
        last_logged_in = (BeautifulSoup(self.session.get(f"https://toyhou.se/{self.username}/stats").content, features="lxml")).find("abbr", {"class": "tooltipster datetime"})["title"]
        retrieve_stat_values.insert(1, last_logged_in)
        # The value scraped is instead inserted into the ResultSet object returned by retrieve_stat_values, which thankfully, is an iterator (woah Rain World reference?? /j)
        # As the last_logged_in time was a value (as in <abbr class = "tooltipster datetime" "title" = last_logged_in>), calling .text on it doesn't work to isolate what we want.
        # So there's one exception to attempting to append it to a dictionary, in which case, we simply bypass the text method.
        # This same issue is replicated under Character().char_stats. 
        for statistic, value in zip(retrieve_stat_attributes, retrieve_stat_values):
            try:
                self.statistics[(statistic.text).strip()] = (value.text).strip()
            except: 
                self.statistics[(statistic.text).strip()] = (value).strip()
        return self.statistics

    def log(self):
        """
        Retrieves the logged-in user's previous username log, as a list of dictionaries containing the date of change, previous username and updated name (sorted by most recent change first). 
        """
        username_date = scrape(self.session, f"https://toyhou.se/{self.username}/stats/usernames", "abbr", {"class":"tooltipster datetime"})
        username_name = scrape(self.session, f"https://toyhou.se/{self.username}/stats/usernames", "td", {"class": "col-9"})
        for date, name in zip(username_date, username_name):
            self.username_log.append(
                {
                    "date": username_date[username_date.index(date)]["title"],
                    "name_from": (name.text.strip()).split(" to ")[0],
                    "name_to": (name.text.strip()).split(" to ")[1]
                } 
            )
        return self.username_log