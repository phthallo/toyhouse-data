import requests
from bs4 import BeautifulSoup
from Session import Session
from utilities import scrape



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
        
        self.characters = []
        self.statistics = {}
        self.username_log = []


    def user_chars(self):
        """
        Retrieves the specified user's characters and returns a list containing tuples of format (<char_name>, <char_id>).
        """
        try:
            retrieve_url = self.session.get(f"https://toyhou.se/{self.username}/characters/folder:all")
            try:
                max_pages = scrape(self.session, f"https://toyhou.se/{self.username}/characters/folder:all","a", {"class": "page-link"})[-2].text
            except:
                max_pages = 1
            for i in range(1, int(max_pages)+1):
                retrieve_characters = scrape(self.session, f"https://toyhou.se/{self.username}/characters/folder:all?legacy=0&page={i}","a", {"class": "btn btn-sm btn-primary character-name-badge"})
                for character in retrieve_characters:
                    self.characters.append(
                        ((character.text).strip(), int((character.get('href')[1:]).split('.',1)[0])))
        except: 
            raise Exception("ParseError: Parsing was unsuccessful.")
        return self.characters 
    

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