# Toyhouse Data
[work in progress] A Toyhouse service to retrieve data about your (and other people's) OCs, as well as your (and other people's) profiles. 

This is very much a niche project (lol), but I'm making this to automate the process - since it's quite tedious going through 20+ (or more) pages of another user's favourite characters if I'm trying to see whether my OCs are there.

## Prerequisites
- [Python3](https://www.python.org/downloads/)
- [Requests](https://pypi.org/project/requests/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)


## Usage
Start by importing the module, then instantiating the class to 'log in' with your Toyhou.se username and password. This is required for basically all usage, as many profiles/characters are inaccessible to guest users. 

```python
from Session import Session
session = Session("username", "password")
session.auth()
```

## Functions
### Session
With the Session class, you can pull a list of all the authorised user's characters and their respective character IDs.  
```python
character_list = session.chars()
print(character_list)
```
```
[{'name': 'Hotaru', 'id': 3326***}, {'name': 'Kaya', 'id': 16191***}, {'name': 'Kaz', 'id': 16540***}, {'name': 'Kip', 'id': 8036***},  {'name': 'Migi', 'id': 5869***}, {'name': 'Moses', 'id': 14381***}, {'name': 'Otto', 'id': 17262***}]
```
Even if you just want the character name, the list-of-dictionaries format lets you easily retrieve those, with something like the below.
```python
for character in character_list:
    print(character.get("name"))
```

#### Statistics
Another thing you can do is get your own statistics, such as the time your Toyhou.se account was registered or the number of characters you have. 
```python
statistics = session.stats()
print(statistics)
print(statistics["Time Registered"])
```
```
{'Time Registered': '22 Mar 2019, *:**:** am', 'Last Logged In': '24 Oct 2023, *:**:** am', 'Invited By': '******', 'Character Count': '**', 'Images Count': '**', 'Literatures Count': '**', 'Words Count': '**', 'Forum Posts Count': '**', 'Subscribed To...': '** users', 'Subscribed To By...': '** users', 'Authorizing...': '**', 'Authorized By...': '**'}

22 Mar 2019 *:**:** am
```
Also included in statistics is your username log, called using `session.log()`. It contains information about the time and date of your username change as well as what the actual username change was. 
```
[{'date': '1 Jan 2020, **:**:** pm', 'name_from': 'an_old_username', 'name_to': 'a_new_username'}]
```

### Characters
Passing a valid character ID and session (as above) to the Character class lets you retrieve details about the character's creation (`char_stats()`) [and whoops, I just realised it doesn't actually output the character name, which, yknow, may be slightly important], previous ownership log (`char_log()`), and a list of people who've favourited the character (`char_favs()`). We can find out all this information about our own OCs by reusing that basic loop code from above. 
```python
for character in character_list:
    id = (character.get("id")) # We only want the ID, so we 'get' the ID from our character dictionary.
    print((Character(id, session)).char_stats()) # We instantiate the Character class with the ID and session from above. Then, we print the statistics for that character.
```
This information is capable of expanding to account for other 'optional' attributes (e.g the trade listing and designer) thanks to the way that it's presented on a standard character profile.
```
{'Created': '3 Jun 2022, 10:50:55 pm', 'Creator': '********', 'Favorites': '7', 'Trade Listing': 'Free'}
{'Created': '11 Jun 2022, 12:54:34 pm', 'Creator': '********', 'Designers': '******', 'Favorites': '54'}
{'Created': '18 Aug 2021, 3:20:01 am', 'Creator': '******', 'Favorites': '21'}
```


## To-Do List

- [ ] Retrieve character stats (~~favourites/favourite amount~~ - comments/comment amount - ~~ownership log~~)

- [ ] Find a profile which has multiple designers listed 

- [ ] Add the character's name into character statistics, since that's kind of important

- [ ] Retrieve other users' favourite characters, ID, and folders/subfolders/page they are located on. 

- [ ] Test on profiles with custom CSS

- [ ] Add better ways to catch errors (e.g user has no characters, login credentials incorrect)
