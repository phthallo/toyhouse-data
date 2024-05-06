# Toyhouse Data
[work in progress] An API wrapper for the site Toyhou.se to retrieve data about user profiles, character profiles, forum posts and more.

This is very much a niche project (lol) but I'm hoping it'll serve some use to anyone curious!

## Prerequisites
- [Python3](https://www.python.org/downloads/)
- [Requests](https://pypi.org/project/requests/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

## Installation
You can now use [pip](https://pip.pypa.io/en/stable/) to install this project! Simply run:

```
py -m pip install toyhouse
```

This project can be found [here](https://pypi.org/project/toyhouse/), albeit slightly out of date.

> [!IMPORTANT]
> I cannot guarantee that this service works on profiles with extreme custom CSS, legacy layouts or profile warnings! If you want to use this, please manually visit `https://toyhou.se/~account/display` and turn off all three settings under 'Profile Browsing'. In the meantime, I will be attempting to fix that.

## Usage
Start by importing the module, then instantiating either the Session or GuestSession class to start the session. With the former, you are required to authenticate (actually log in) using `auth()`
It is highly recommended to log in with a Session in order to access logged-in user only/authorise-only profiles and content.


*`file_path` here is an optional argument - it dictates a folder in which relevant images are saved.*

*For instance, if you want to save a user's profile picture in your Documents folder, you would add `C:/Users/<yourusername>/Documents`, and the profile picture would then be downloaded in the subfolder `/<thatuser>/`. If left blank, the subfolder will be placed in the directory where this code is currently running.*

```python
import toyhouse
session = toyhouse.Session("<username>", "<password>", "file_path")
session.auth()
# alternatively
session = toyhouse.GuestSession("<file_path>")
```

## Examples
If you don't care about the docs and just want to know how you can use this, see the [Snippets page](/snippets.md).

## Functions
### Session
```python
session = toyhouse.Session("<username>", "<password>")
session.auth()
```
Starts a new logged-in Session using the credentials above, letting you access information on the Toyhouse website. 


```python
session = toyhouse.GuestSession()
```
Starts a new Guest Session. No authentication is required, but you will be limited to only publicly viewable data. 

---

### User
```python
user_info = toyhouse.User(session, "<username>")
```
Creates a new User object, letting you retrieve information about whatever user is listed there. 


#### chars
```python
user_info.chars
# Returns 
[('Althea', 12391***, 'https://toyhou.se/12391***.althea', 'https://toyhou.se/<username>/characters/<folder:folderid>?page=<page>')]
```
Outputs a **list of tuples** containing every **character from that user** accessible to the authorised session, in the form `(<char_name>, <char_id>, <char_url>, <char_loc>)`.

#### stats
```python
user_info.stats
# Returns 
{'Time Registered': '22 Mar 2019, **:**:** am', 'Last Logged In': '25 Oct 2023, **:**:** am', 'Invited By': '***', 'Character Count': '***', 'Images Count': '***', 'Literatures Count': '***', 'Words Count': '***', 'Forum Posts Count': '***', 'Subscribed To...': '*** users', 'Subscribed To By...': '*** users', 'Authorizing...': '***', 'Authorized By...': '***'}
```
Outputs the specified user's publicly viewable **statistics** (if the user is not self, else it outputs all statistics regardless of hidden status) as a **dictionary**.

#### log
```python
user_info.log
# Returns 
[{'date': '6 Nov 2020, **:**:** pm', 'name_from': 'my_old_username', 'name_to': 'my_new_username'}, {'date': '19 Apr 2020, **:**:** am', 'name_from': 'my_oldest_username', 'name_to': 'my_old_username'}]
```
Outputs the specified user's **username change history** as a **list of dictionaries**, with most recent name change first.

#### pic
```python
user_info.pic(download=True)
# Returns 
<username> profile picture has been saved at <path>

user_info.pic()
# Returns
https://f2.toyhou.se/file/f2-toyhou-se/users/<username>
```
Retrieves the specified user's **profile picture**, and if `download=True`, **downloads the image** at the file path mentioned under [Usage](#usage). If `download=False`, it returns the URL at which you can access the profile picture.

#### designs
```python
user_info.designs
```
Outputs a **list of tuples** in format `(<char_name>, <char_id>, <char_url>, <char_loc>)` for all characters that the user is credited as a designer of. This format is the same as [chars()](#chars) except with `<char_loc>` returning the URL + page number that the character is on.


#### favs
```python
user_info.favs
```
Outputs a **list of tuples** in format `(<char_name>, <char_id>, <char_url>, <char_loc>)` for all **characters that the user has favourited**. 
This format is identical to the above, with the addition of also showing what favourites folder the character has been sorted into in `<char_loc>`

---

### Character
```python
char_info = toyhouse.Character(session, characterid)
```
This creates a new Character object, letting you retrieve information about the character profile which corresponds to that ID. 

#### stats
```python
char_info.stats
# Returns 
{'Created': '31 Dec 2018, **:**:** am', 'Creator': '********', 'Favorites': '57'}
```
Outputs the publicly viewable **statistics** of the character, including its creation date, creator and favourites amount as a bare minimum (can also include trade listing and designer) as a **dictionary**.

#### log
```python
char_info.log
# Returns 
[('20 May 2022, **:**:** pm', 'current_owner'), ('20 Jan 2021, **:**:** pm', 'previous_owner'), ('22 Sep 2020, **:**:** pm', 'previous_previous_owner')]
```
Outputs the previous **ownership log** of the character as a **list of tuples** in form `(<transfer date>, <recipient of transfer>)`, starting with the most recent transfer (so the current owner) first.

#### favs
```python
char_info.favs
# Returns 
['i_favourited_this_character', 'i_did_too', 'i_did_as_well']
```
Outputs a **list** of all accounts that have the **character favourited**.

### Forum

```python
forum_info = toyhouse.Forum(session, forumboardid)
```
Creates a new Forum object, letting you retrieve information about Forum boards and their posts. 

#### threads
```python
forum_info.threads
```

Outputs a **list of tuples** in format `[(thread_title, thread_author, thread_creation_date)]` for the threads on the first page of a specific forum board. There is currently no distinguishing between pinned threads and standard threads. 

---
## To-Do List

- [ ] Retrieve character stats (~~favourites/favourite amount~~ - comments/comment amount - ~~ownership log~~)

- [X] Add Guest Session

- [ ] Find a profile which has multiple designers listed 

- [ ] Add the character's name into character statistics, since that's kind of important

- [X] Retrieve other users' favourite characters, ID, and folders/subfolders/page they are located on. 

- [ ] Test on profiles with custom CSS

- [ ] Add better ways to catch errors (e.g ~~login credentials incorrect~~)
