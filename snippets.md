# Code Snippets 
Each of the following snippets assumes authentication has already occurred i.e the following, which produces a `session` object:
```python
import toyhouse
session = toyhouse.Session("username", "password")
session.auth()
```

#### Favourites Filtering 
```python
user1_favs = toyhouse.User(session, "<user1>").favs
user2_chars = toyhouse.User(session, "<user2>").chars

def usercomparison(favs, chars):
    match = [(chars[0], chars[2], favs[3]) for character in chars for favourite in favs if chars[1] == favs[1]]
    # Outputs the name (char2[0]), URL ([chars[2]) and location in favourites (favs[3]) of a character if the character is found in the other person's favourites. 
    return match

print(usercomparison(user1_favs, user2_chars))
```
This snippet can be used to produce a list of a user's characters that have been favourited by another user, and will produce a link to where the character can be found in their favourites (relevant if the user sorts their favourited characters in different folders). 

You may wish to use this to see whether another user has taken interest in your own characters. In that case, substitute `<user1>` for their username and `user2` for your own username.
