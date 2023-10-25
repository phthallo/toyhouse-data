import requests
from bs4 import BeautifulSoup
from utilities import scrape

class Session:
    """
    Establishes a new Toyhou.se session to allow access to restricted profiles.
    """
    def __init__(self,username,password):
        """
        __init__ method

        Arguments:
        username (str): Toyhou.se username
        password (str): Toyhou.se password
        """
        self.session = requests.Session()
        self.authenticated = False
        self.username = username
        self.password = password

    def auth(self):
        """
        Authenticates the user using credentials provided previously. 
        (Note that it doesn't actually check if they are correct at this stage.)
        """
        csrf = scrape(self.session, "https://toyhou.se/~account/login", "meta", {"name": "csrf-token"}, all = False)["content"]
        creds = {"username": self.username,
                "password": self.password,
                "_token": csrf}
        post = self.session.post("https://toyhou.se/~account/login", data=creds)
        if "Log In" not in post.text:
            self.authenticated = True
            return "Authenticated as " + self.username
        elif "You have failed to login too many times" in post.text:
            raise Exception("AuthError: You have been ratelimited. Please try again in a few minutes.")
        else:
            raise ValueError("Authentication unsuccessful. Please recheck login credentials.")
        
   