# Toyhouse Data
[work in progress] A Toyhouse service to retrieve data about your (and other people's) OCs, as well as your (and other people's) profiles. 

This is very much a niche project (lol) but I'm hoping it'll serve some use to anyone curious!

## Prerequisites
- [Python3](https://www.python.org/downloads/)
- [Requests](https://pypi.org/project/requests/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)


## Usage
Start by importing the module, then instantiating the class to 'log in' with your Toyhou.se username and password. This is required for basically all usage, as many profiles/characters are inaccessible to guest users. 

```python
from Session import Session
session = Session("<username>", "<password>")
session.auth()
```

## Functions
### Session
```python
session = Session("<username>", "<password>")
session.auth()
```
Logs you in to the session using your username and password. This session object is required to access basically everything else! 

---

### User
```python
user_info = User(session, "<username>")
```
This creates a new User object, letting you retrieve information about whatever user is listed there. 


#### user_chars()
```python
user_info.user_chars()
# Returns 
[('Althea', 12391***), ('Aster', 21438***), ('Aspen', 4106***)]
```
Outputs a **list of tuples** containing every **character from that user** accessible to the authorised session, in the form `(<character>, <id>)`.

#### user_stats()
```python
user_info.user_stats()
# Returns 
{'Time Registered': '22 Mar 2019, **:**:** am', 'Last Logged In': '25 Oct 2023, **:**:** am', 'Invited By': '***', 'Character Count': '***', 'Images Count': '***', 'Literatures Count': '***', 'Words Count': '***', 'Forum Posts Count': '***', 'Subscribed To...': '*** users', 'Subscribed To By...': '*** users', 'Authorizing...': '***', 'Authorized By...': '***'}
```
Outputs the specified user's publicly viewable **statistics** (if the user is not self, else it outputs all statistics regardless of hidden status) as a **dictionary**.

#### user_log()
```python
user_info.user_log()
# Returns 
[{'date': '6 Nov 2020, **:**:** pm', 'name_from': 'my_old_username', 'name_to': 'my_new_username'}, {'date': '19 Apr 2020, **:**:** am', 'name_from': 'my_oldest_username', 'name_to': 'my_old_username'}]
```
Outputs the specified user's **username change history** as a **list of dictionaries**, with most recent name change first.

---

### Character
```python
char_info = Character(session, characterid)
```
This creates a new Character object, letting you retrieve information about the character profile which corresponds to that ID. 

#### char_stats()
```python
char_info.char_stats()
# Returns 
{'Created': '31 Dec 2018, **:**:** am', 'Creator': '********', 'Favorites': '57'}
```
Outputs the publicly viewable **statistics** of the character, including its creation date, creator and favourites amount as a bare minimum (can also include trade listing and designer) as a **dictionary**.

#### char_log()
```python
char_info.char_log()
# Returns 
[('20 May 2022, **:**:** pm', 'current_owner'), ('20 Jan 2021, **:**:** pm', 'previous_owner'), ('22 Sep 2020, **:**:** pm', 'previous_previous_owner')]
```
Outputs the previous **ownership log** of the character as a **list of tuples** in form `(<transfer date>, <recipient of transfer>)`, starting with the most recent transfer (so the current owner) first.

#### char_favs()
```python
char_info.char_favs()
# Returns 
['i_favourited_this_character', 'i_did_too', 'i_did_as_well']
```
Outputs a **list** of all accounts that have the **character favourited**.


---
## To-Do List

- [ ] Retrieve character stats (~~favourites/favourite amount~~ - comments/comment amount - ~~ownership log~~)

- [ ] Add Guest Session

- [ ] Find a profile which has multiple designers listed 

- [ ] Add the character's name into character statistics, since that's kind of important

- [ ] Retrieve other users' favourite characters, ID, and folders/subfolders/page they are located on. 

- [ ] Test on profiles with custom CSS

- [ ] Add better ways to catch errors (e.g user has no characters, login credentials incorrect)
