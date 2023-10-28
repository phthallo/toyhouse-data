import requests
from bs4 import BeautifulSoup
from .session import *
from .utilities import *
import shutil
import os



class User:
    def __init__(self, session, username):
        """
        __init__ method

        Arguments: 
        session (Session): Used to access restricted user profiles.
        username (str): Username of profile to access.
        """
        self._authenticated = session.authenticated
        if self._authenticated is False:
            raise Exception("AuthError: You must be logged in to retrieve information about users")
        if isinstance(session, Session) != True: 
            raise ValueError(f"{session} is not of class Session")
        if username == session.username:
            self.username = session.username
            self._determine_self = True
        else:
            self.username = username
            self._determine_self = False
        self.session = session.session
        self.file_path = session.file_path
        self.characters = []
        self.statistics = {}
        self.username_log = []
        self.designs = []

    def _create_path(self):
        if self.username in self.file_path:
            return self.file_path 
        if self.file_path == "":
            self.file_path = os.getcwd() + f"/{self.username}"
        else:
            self.file_path = self.file_path + f"/{self.username}"
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        return self.file_path

    def user_chars(self):
        """
        Retrieves the specified user's characters and returns a list containing tuples of format (<char_name>, <char_id>, <char_url>).
        """
        return char_object(self.session, f"https://toyhou.se/{self.username}/characters/folder:all", self.characters)
    

    def user_stats(self):
        """
        Retrieves the specified user's statistics as a dictionary. It will return all statistics (regardless of public view status) recorded provided you are viewing your own profile.
        Else, it will only return the ones marked visible.
        """
        # Toyhou.se lets people hide specific statistcs, such as the time they last logged in. Furthermore, the /stats page for your own profile versus another person's profile is different.
        # This is primarily due to stuff like the statistics on your own page being clickable, as well as 'greying out' stats hidden to the public.
        # Unfortunately, this means that we can't exactly use the same code, so we have to quickly check whether the profile we're checking has the same username as the current session.
        # Of course, we could just skip this. However, it's still helpful to obtain all the statistics available.
        
         # Because the last-logged-in time is relative to when you're viewing the page (e.g 6 seconds ago, 2 weeks ago), we need to search specifically for the actual date (usually viewable by tooltip).
        if self._determine_self == True:
            retrieve_stat_attributes = scrape(self.session, f"https://toyhou.se/{self.username}/stats", "span", {"class": "custom-control-description ml-1"})
        else:
            retrieve_stat_attributes = scrape(self.session, f"https://toyhou.se/{self.username}/stats", "dt", {"class": "field-title col-lg-3 col-md-4"})
        retrieve_stat_values = scrape(self.session, f"https://toyhou.se/{self.username}/stats", "dd", {"class": ["field-value col-lg-9 col-md-8", "field-value col-lg-9 col-md-8 faded"]})
        try:
            last_logged_in = scrape(self.session, f"https://toyhou.se/{self.username}/stats", "abbr", {"class": "tooltipster datetime"}, all = False)["title"]
            listform = [(stat.text).strip() for stat in retrieve_stat_attributes]
            retrieve_stat_values[(list(listform).index('Last Logged In'))] = last_logged_in
        except:
            pass
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

    def user_log(self):
        """
        Retrieves the specified user's previous username log, as a list of dictionaries containing the date of change, previous username and updated name (sorted by most recent change first). 
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
    
    def user_pic(self, download=False):
        """
        Retrieves a link to the specified user's profile picture, and optionally, saves the image. 
        """
        user_image = (f"https://f2.toyhou.se/file/f2-toyhou-se/users/{self.username}?15")
        if download:
            response = requests.get(user_image, stream=True)
            with open(User._create_path(self) + f'/{self.username}.png', 'wb') as fout:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, fout)
            return f"{self.username} profile picture has been saved at {User._create_path(self)}."
        return user_image          

    def user_designs(self):
        """
        Returns links and information about all characters that the user is credited as a designer of, in the format (<char_name>, <char_id>, <char_url>)
        """
        return char_object(self.session, f"https://toyhou.se/{self.username}/created", self.designs)
