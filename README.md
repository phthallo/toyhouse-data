# Toyhouse Character Checker
[work in progress] A Toyhouse service to retrieve data about your (and other people's) OCs.

This is very much a niche project (lol), but I'm making this to automate the process - since it's quite tedious going through 20+ (or more) pages of another user's favourite characters if I'm trying to see whether my OCs are there.

## Prerequisites
- [Python3](https://www.python.org/downloads/)
- [Requests](https://pypi.org/project/requests/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)


## Usage
Start by importing the module, then instantiating the class with your Toyhou.se username and password. 
You will then need to authenticate yourselves to log in on that session. This is required, as many profiles/characters are inaccessible to guest users. 

```python
from Session import Session
session = Session("username", "password")
session.auth()
```

You can retrieve a list of your characters and their corresponding IDs by calling `retrieve_char()`. 

```python
characters = session.retrieve_char()
print(characters)
```

Doing so should print a list containing the names of your characters and IDs in the default order that your characters are sorted in (which is alphabetical order, given that we're only looking in `folder:all`) e.g:

```python
[('Ashclaw', 4717***), ('Cosmos', 7092***), ('Dakota', 565***), ('July', 7955***)] 
```

With these IDs, you can retrieve a list of the people who favourited that specific character, sorted in default order (which is descending via data favourited)
```python
character_favourites = Character(4717***, session) # We log in with our pre-existing session to retrieve information about the character Ashclaw.
# returns
['username', 'another username', 'a third username']

```

Another thing we can do with `Session()` is obtain the logged-in user's statistics, as visible from the `toyhou.se/<username>/stats` page (even if they are hidden from the public) 
```python
statistics = session.retrieve_stats()
print(statistics)
```

This outputs a dictionary, letting you access the value using the statistic attribute name as a key.
```python
{ #dict containing arbitrary values
    'Time Registered': '22 Mar 2019, *:**:** am', 
    'Last Logged In': '22 Oct 2023, *:**:** pm', 
    'Invited By': '*****', 
    'Character Count': '25', 
    'Images Count': '323', 
    'Literatures Count': '1', 
    'Words Count': '233', 
    'Forum Posts Count': '157', 
    'Subscribed To...': '2 users', 
    'Subscribed To By...': '46 users', 
    'Authorizing...': '1', 
    'Authorized By...': '3'
    }
```

## To-Do List
- [x] Retrieve own characters (and ID) 

- [x] Retrieve list of users who have favourited individual characters (by ID)

- [ ] Retrieve stats? (~~favourites/favourite amount~~ - comments/comment amount - ownership log)

- [ ] Retrieve other users' favourite characters, ID, and folders/subfolders/page they are located on. 

- [ ] Compare characters and return list of every character + location found.

- [ ] Test on profiles with custom CSS

- [ ] Add better ways to catch errors (e.g user has no characters, login credentials incorrect)
