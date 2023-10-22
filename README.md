# Toyhouse Character Checker
[work in progress] A Toyhouse service to retrieve your OCs and compare them with another user's favourited OCs. 

This is very much a niche project (lol), but I'm making this to automate the process - since it's quite tedious going through 20+ (or more) pages of another user's favourite characters if I'm trying to see whether my OCs are there.

## Prerequisites
- Python
- [Requests](https://pypi.org/project/requests/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)


## Usage
Start by importing the module, then instantiating the class with your Toyhou.se username and password. 
You will then need to authenticate yourselves to log in on that session. This is required, as many profiles/characters are inaccessible to guest users. 

```
from ToyhouseSession import ToyhouseSession
session = ToyhouseSession("username", "password")
session.auth()
```

Right now, the only other thing you can do is retrieve your own characters. 

```
characters = session._retrieve_char()
print(characters)
```

Doing so should print a list containing the names of your characters and IDs in the default order that your characters are sorted in, usually alphabetical order e.g:

```
[('Ashclaw', 4717***), ('Cosmos', 7092***), ('Dakota', 565***), ('July', 7955***)] 
```


## To-Do List
[x] Retrieve own characters (and ID) 
[ ] Retrieve other users' favourite characters, ID, and folders/subfolders/page they are located on. 
[ ] Compare characters and return list of every character + location found.
[ ] Test on profiles with custom CSS
[ ] Add better ways to catch errors (e.g user has no characters, login credentials incorrect)
