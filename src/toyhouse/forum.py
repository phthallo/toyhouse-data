import requests
from bs4 import BeautifulSoup
from toyhouse.utilities import *
from toyhouse.session import *

class Forum:
    """Pulls information about a forum board."""
    def __init__(self, session,id): 
        """
        __init__ method

        Arguments: 
        session (Session): Used to access restricted forum posts.
        id (int): Forum ID 
        """
        if isinstance(session, Session) != True and isinstance(session, GuestSession) != True: 
            raise ValueError(f"{session} is not of class Session or GuestSession")
        self.id = id
        self.session = session.session
        self.threads = []

    @property
    def threads(self):
        retrieve_thread_titles = scrape(self.session, f"https://toyhou.se/~forums/{self.id}.x/", "h3", {"class": "forum-thread-title"})
        retrieve_thread_authors = scrape(self.session, f"https://toyhou.se/~forums/{self.id}.x/", "div", {"class": "forum-thread-info small"})
        retrieve_thread_time = scrape(self.session, f"https://toyhou.se/~forums/{self.id}.x/", "abbr", {"class": "tooltipster datetime"})
        retrieve_thread_url = scrape(self.session, f"https://toyhou.se/~forums/{self.id}.x/", "h3", {"class": "tooltipster datetime"})
        del retrieve_thread_time[1::2]
        for title, author, time in zip(retrieve_thread_titles, retrieve_thread_authors, retrieve_thread_time):
            self._posts.append(((title.text), (author.text).strip().split()[2], (str(time).split('"'))[3]))
        return self._posts
    
    # remove newline chars from output
        
