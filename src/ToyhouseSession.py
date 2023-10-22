import requests
from bs4 import BeautifulSoup

class ToyhouseSession:
    """
    Establishes a new Toyhou.se session.
    """
    def __init__(self,username,password):
        """
        __init__ method

        Arguments:
        username (str): Toyhou.se username
        password (str): Toyhou.se password
        """
        self.session = requests.session()
        self.username = username
        self.password = password
        self.characters = []

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
        
    def _retrieve_char(self):
        """
        Retrieves the logged-in user's characters and returns a list containing tuples of form `(charactername, characterID)`.
        """
        try:
            retrieve_url = self.session.get(f"https://toyhou.se/{self.username}/characters/folder:all")
            try:
                max_pages = BeautifulSoup(retrieve_url.content, features="lxml").find_all("a", {"class": "page-link"})[-2].text
            except:
                max_pages = 1
            for i in range(1, int(max_pages)+1):
                retrieve_url = self.session.get(f"https://toyhou.se/{self.username}/characters/folder:all?legacy=0&page={i}")
                retrieve_lxml = BeautifulSoup(retrieve_url.content, features="lxml")
                retrieve_characters = retrieve_lxml.find_all("a", {"class": "btn btn-sm btn-primary character-name-badge"})
                for character in retrieve_characters:
                    self.characters.append(
                        (
                            (character.text).strip(),
                            int((character.get('href')[1:]).split('.',1)[0])
                            )
                            )
        except: 
            raise Exception("Parsing was unsuccessful. Please verify that your login credentials are correct.")
        return self.characters
    
    