""" CSC108 Assignment 3: Club Recommendations - Starter code."""
from typing import List, Tuple, Dict, TextIO


# Sample Data (Used by Doctring examples)

P2F = {'Jesse Katsopolis': ['Danny R Tanner', 'Joey Gladstone',
                            'Rebecca Donaldson-Katsopolis'],
       'Rebecca Donaldson-Katsopolis': ['Kimmy Gibbler'],
       'Stephanie J Tanner': ['Michelle Tanner', 'Kimmy Gibbler'],
       'Danny R Tanner': ['Jesse Katsopolis', 'DJ Tanner-Fuller',
                          'Joey Gladstone']}

P2C = {'Michelle Tanner': ['Comet Club'],
       'Danny R Tanner': ['Parent Council'],
       'Kimmy Gibbler': ['Rock N Rollers', 'Smash Club'],
       'Jesse Katsopolis': ['Parent Council', 'Rock N Rollers'],
       'Joey Gladstone': ['Comics R Us', 'Parent Council']}


# Helper functions 

def update_dict(key: str, value: str,
                key_to_values: Dict[str, List[str]]) -> None:
    """Update key_to_values with key/value. If key is in key_to_values,
    and value is not already in the list associated with key,
    append value to the list. Otherwise, add the pair key/[value] to
    key_to_values.

    >>> d = {'1': ['a', 'b']}
    >>> update_dict('2', 'c', d)
    >>> d == {'1': ['a', 'b'], '2': ['c']}
    True
    >>> update_dict('1', 'c', d)
    >>> d == {'1': ['a', 'b', 'c'], '2': ['c']}
    True
    >>> update_dict('1', 'c', d)
    >>> d == {'1': ['a', 'b', 'c'], '2': ['c']}
    True
    """

    if key not in key_to_values:
        key_to_values[key] = []
        
    if value not in key_to_values[key]:
        key_to_values[key].append(value)


# Required functions

def load_profiles(profiles_file: TextIO) -> Tuple[Dict[str, List[str]],
                                                  Dict[str, List[str]]]:
    """Return a two-item tuple containing a "person to friends" dictionary
    and a "person_to_clubs" dictionary with the data from profiles_file.

    NOTE: Functions (including helper functions) that have a parameter of type
          TextIO do not need docstring examples.
    """
    p2f = {}
    p2c = {}
    
    list_text = profiles_file.readlines()
    for i in range(len(list_text)):
        # For initial Key
        if i == 0:
            temp = helper_switch(list_text[i])
        # For other keys
        elif list_text[i] == '\n':
            temp = helper_switch(list_text[i + 1])  
            
        if i + 1 < len(list_text):
            # For P2F
            if ', ' in list_text[i + 1] and \
               helper_switch(list_text[i + 1]) != temp:
                next_value = helper_switch(list_text[i + 1])
                update_dict(temp, next_value, p2f)
            
                # For P2C    
            elif ', ' not in list_text[i + 1] and list_text[i + 1] != '\n':
                next_value = list_text[i + 1].replace('\n', '')
                update_dict(temp, next_value, p2c)            
    
    new_p2f = helper_sortdict(p2f)
    new_p2c = helper_sortdict(p2c)
    return (new_p2f, new_p2c)

def helper_sortdict(sortdict: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Returns a new dictionary that has its value sorted alphabetically or 
    numerically from least to greatest
    
    >>>helper_sortdict({'test': ['b', 'a']})
    {'test': ['a', 'b']}
    
    >>>helper_sortdict({'test': ['2', '1']})
    {'test': ['1', '2']}
    """
    for values in sortdict:
        test = sortdict[values]
        test.sort()
        sortdict[values] = test
    return sortdict    
                                                 

def helper_switch(switch: str) -> str:
    """
    Returns a new string that switches the order of first name and last name
    
    >>>helper_switch('Pritchett, Jay')
    'Jay Pritchett'
    
    >>>helper_switch('Delgado, Manny')
    'Manny Delgado'
    """
    new_text = switch.replace('\n', '')
    new_text = ' '.join(reversed(new_text.split(', ')))
    return new_text

def get_average_club_count(person_to_clubs: Dict[str, List[str]]) -> float:
    """Return the average number of clubs that a person in person_to_clubs
    belongs to.

    >>> get_average_club_count(P2C)
    1.6
    >>> get_average_club_count({})
    0.0
    """
    count_club = 0
    count_ppl = len(person_to_clubs)
    
    for people in person_to_clubs:
        test = person_to_clubs[people]
        count_club += len(test)

    return count_club/count_ppl if count_ppl else 0.0

def get_last_to_first(
        person_to_friends: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Return a "last name to first name(s)" dictionary with the people from the
    "person to friends" dictionary person_to_friends.

    >>> get_last_to_first(P2F) == {
    ...    'Katsopolis': ['Jesse'],
    ...    'Tanner': ['Danny R', 'Michelle', 'Stephanie J'],
    ...    'Gladstone': ['Joey'],
    ...    'Donaldson-Katsopolis': ['Rebecca'],
    ...    'Gibbler': ['Kimmy'],
    ...    'Tanner-Fuller': ['DJ']}
    True
    
    >>> get_last_to_first({'John Doe': ['John Doe']})
    {'Doe': ['John']}
    """
    
    new_dict = {}
    
    for key in person_to_friends:
        word_list = key.split()
        rest_of_word = ' '.join(word_list[0:-1])
        if not word_list[-1] in new_dict: 
            new_dict[word_list[-1]] = [rest_of_word]
        if not rest_of_word in new_dict[word_list[-1]]:
            new_dict[word_list[-1]].append(rest_of_word)
        lst = person_to_friends[key]
        for values in lst:
            split_values = values.split()
            rest_of_word2 = ' '.join(split_values[0:-1])
            if not split_values[-1] in new_dict:
                new_dict[split_values[-1]] = [rest_of_word2]
            if not rest_of_word2 in new_dict[split_values[-1]]:
                new_dict[split_values[-1]].append(rest_of_word2)
    
    new_dict = helper_sortdict(new_dict)       
    return new_dict

def invert_and_sort(key_to_value: Dict[object, object]) -> Dict[object, list]:
    """Return key_to_value inverted so that each key is a value (for
    non-list values) or an item from an iterable value, and each value
    is a list of the corresponding keys from key_to_value.  The value
    lists in the returned dict are sorted.

    >>> invert_and_sort(P2C) == {
    ...  'Comet Club': ['Michelle Tanner'],
    ...  'Parent Council': ['Danny R Tanner', 'Jesse Katsopolis',
    ...                     'Joey Gladstone'],
    ...  'Rock N Rollers': ['Jesse Katsopolis', 'Kimmy Gibbler'],
    ...  'Comics R Us': ['Joey Gladstone'],
    ...  'Smash Club': ['Kimmy Gibbler']}
    True
    
    >>> invert_and_sort({1: '2'})
    {'2': [1]}
    """
    
    new_dic = {}
    for k, v in key_to_value.items():
        #print(type(key_to_value)) # output - dict
        
        if type(v) == list: #list values
            for x in v:
                new_dic.setdefault(x, []).append(k)                        
        elif type(v) != list: #non list
            new_dic.setdefault(v, []).append(k)
    for val in new_dic:
        new_dic[val].sort()            
    return new_dic 
    
def get_clubs_of_friends(person_to_friends: Dict[str, List[str]],
                         person_to_clubs: Dict[str, List[str]],
                         person: str) -> List[str]:
    """Return a list, sorted in alphabetical order, of the clubs in
    person_to_clubs that person's friends from person_to_friends
    belong to, excluding the clubs that person belongs to.  Each club
    appears in the returned list once per each of the person's friends
    who belong to it.

    >>> get_clubs_of_friends(P2F, P2C, 'Danny R Tanner')
    ['Comics R Us', 'Rock N Rollers']
    
    >>> get_clubs_of_friends(P2F, P2C, 'Stephanie J Tanner')
    ['Comet Club', 'Rock N Rollers', 'Smash Club']
    """
    # Find friends of person -> store in list
    # Find clubs of person -> store in another list "list1"
    # Get all clubs friends are part of - "list2"
        # if "list1" items not in "list2" THEN append values
    #sort
    
    new_clubs = []
    if person not in person_to_friends:
        return new_clubs

    friends = person_to_friends[person]
    if person in person_to_clubs:
        clubs_of_person = person_to_clubs[person]
    else:
        clubs_of_person = [] # His/her own set of clubs they're in
    
    for x in friends:
        if x in person_to_clubs:
            clubs = person_to_clubs[x]
            for y in clubs:
                if y not in clubs_of_person: 
                    new_clubs.append(y)
    new_clubs.sort()
    return new_clubs

def recommend_clubs(
        person_to_friends: Dict[str, List[str]],
        person_to_clubs: Dict[str, List[str]],
        person: str,) -> List[Tuple[str, int]]:
    """Return a list of club recommendations for person based on the
    "person to friends" dictionary person_to_friends and the "person
    to clubs" dictionary person_to_clubs using the specified
    recommendation system.

    >>> recommend_clubs(P2F, P2C, 'Stephanie J Tanner')
    [('Comet Club', 1), ('Rock N Rollers', 1), ('Smash Club', 1)]
    
    >>> recommend_clubs(P2F, P2C, 'Jesse Katsopolis')
    [('Comics R Us', 2), ('Smash Club', 1)]
    
    """
    temp_dict = {}
    new_dict = {}
    # Make a dictionary with all clubs and scores starting at 0
    for clubs in person_to_clubs:
        items = person_to_clubs[clubs]
        for j in items:
            if not j in temp_dict:# and j != old_club:<- only applies to 2nd fx
                temp_dict[j] = 0
    
    if person in person_to_friends:
        #call helper_friends function
        temp_dict = helper_friends(temp_dict, person_to_friends,
                                   person_to_clubs, person)
    if person in person_to_clubs:        
        #call helper_clubs function
        temp_dict = helper_clubs(temp_dict, 
                                 person_to_clubs, person)
        
    #remove clubs that have 0 in value
    for not_zeroes in temp_dict:
        if temp_dict[not_zeroes] != 0:
            new_dict.update({not_zeroes:temp_dict[not_zeroes]})
            
    new_dict = helper_sort(new_dict) 
    return new_dict

def helper_sort(sortdict: Dict[str, int]) -> List[Tuple[str, int]]:
    """
    Returns the sorted list of tuple of club recommendations. Sorts
    the numbers numerically then sorts the clubs with the same scores in 
    alphabetical order. 
    
    >>> helper_sort({'club B': 1, 'club A': 2, 'club C': 2, 'club D': 1})
    [('club A', 2), ('club C', 2), ('club B', 1), ('club D', 1)]
    
    >>> helper_sort({'D': 1, 'C': 2, 'B': 2, 'A': 1})
    [('B', 2), ('C', 2), ('A', 1), ('D', 1)]
    """
    new_list = [] # return this
    
    inverted_clubs = invert_and_sort(sortdict)

    keys = list(inverted_clubs.keys())
    keys.sort(reverse=True)
    for num in keys:
        temp = inverted_clubs[num]
        for val in temp:
            new_list.append((val, num))
        
    return new_list
    
def helper_friends(temp_dict: Dict[str, int],
                   person_to_friends: Dict[str, List[str]],
                   person_to_clubs: Dict[str, List[str]],
                   person: str) -> Dict[str, int]:  # WORKING 11/24/19                 
    """
    Returns the updated dictionary with updated points (for club 
    recommendation) based on whether the person has any friends that are a 
    part of another club.
    
    >>> helper_friends({'Club A': 0}, {'John': ['Jane']}, \
                       {'Jane': ['Club A']}, 'John')
    {'Club A': 1}
    
    >>> helper_friends({'Club A': 0, 'Club B': 0}, {'John': ['Jane']}, \
                       {'Jane': ['Club A', 'Club B']}, 'John')
    {'Club A': 1, 'Club B': 1}
    """

    friends_of_person = person_to_friends[person] # friendlist of person
    for each_friend in friends_of_person: # for each friend in ^
        if each_friend in person_to_clubs: # if they're in person_to_clubs
            club_list = person_to_clubs[each_friend] # get list of clubs
            for each_club in club_list:
                temp_dict[each_club] += 1 # update temp_dict (+1) for each club
                
    return temp_dict

def helper_clubs(temp_dict: Dict[str, int], 
                 person_to_clubs: Dict[str, List[str]],
                 person: str) -> Dict[str, int]: 
    """
    Returns the updated dictionary with updated points (for club 
    recommendation) for certain club(s). Points are counted for each different 
    person that goes that certain club and also goes to the same club(s) 
    as person
    
    >>> helper_clubs({'Club A': 0, 'Club B': 0}, {'John': ['Club A'], \
                      'Jane':['Club B', 'Club A']}, 'John')
    {'Club B': 1}
    >>> helper_clubs({'Club A': 0}, {'John': ['Club A'], \
                      'Jane':['Club A']}, 'John')
    {}
    """
    #new_dict = {}
    inverted_clubs = invert_and_sort(person_to_clubs)
    
    clubs_of_person = person_to_clubs[person] # clublist of person
    for each_club in clubs_of_person:	# each club in ^
        people_in_club = inverted_clubs[each_club] # list of ppl in club
        for each_person in people_in_club:
            if each_person is not person and each_person in person_to_clubs:
                clubs = person_to_clubs[each_person] # clubs new person are in
                for new_club in clubs: # for each of new club
                    #new club not in person's clublist
                    #if new_club not in clubs_of_person: 
                        #temp_dict[new_club] += 1
                    temp_dict = cont_helper_clubs(new_club, clubs_of_person, \
                                                  temp_dict)
    
    # eliminate clubs that person is in
    for x in clubs_of_person:
        if x in temp_dict.keys():
            del temp_dict[x]
    return temp_dict

def cont_helper_clubs(new_club: str, clubs_of_person: list, \
                      temp_dict: Dict[str, int]) -> Dict[str, int]:
    """
    Continuation of helper_clubs as there was too many nested loops.
    If the new_club is not a part of the original person's clubslist 
    (clubs_of_person) then add a point to the new_club.
    
    >>> cont_helper_clubs('A', ['B', 'C'], {'A': 0})
    {'A': 1}
    
    >>> cont_helper_clubs('A', ['A', 'C'], {'A': 0})
    {'A': 0}
    """
    if new_club not in clubs_of_person: 
        temp_dict[new_club] += 1  
    return temp_dict

if __name__ == '__main__':
    pass

    # If you add any function calls for testing, put them here.
    # Make sure they are indented, so they are within the if statement body.
    # That includes all calls on print, open, and doctest.

    # import doctest
    # doctest.testmod()
