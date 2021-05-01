"""Assignment 1.
Lance Uy 1006123570
Sept, 2019
Prof J. Calver
"""

import math

# Maximum number of characters in a valid tweet.
MAX_TWEET_LENGTH = 50

# The first character in a hashtag.
HASHTAG_SYMBOL = '#'

# The first character in a mention.
MENTION_SYMBOL = '@'

# Underscore is the only non-alphanumeric character that can be part
# of a word (or username) in a tweet.
UNDERSCORE = '_'

SPACE = ' '


def is_valid_tweet(text: str) -> bool:
    """Return True if and only if text contains between 1 and
    MAX_TWEET_LENGTH characters (inclusive).

    >>> is_valid_tweet('Hello Twitter!')
    True
    >>> is_valid_tweet('')
    False
    >>> is_valid_tweet(2 * 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    False

    """
    return bool(1 <= len(text) <= MAX_TWEET_LENGTH)

def compare_tweet_lengths(tweet_1: str, tweet_2: str) -> int:
    """ Returns a value based on the difference in length of the two tweets
    Returns 1: if the first tweet (tweet_1) is longer than the second (tweet_2)
    Returns -1: if the second tweet (tweet_2)is longer than the first (tweet_1)
    Returns 0: if both tweets are equal in length
    
    Precondition: both tweets are valid
    
    >>>compare_tweet_lengths("longer","short")
    1
    >>>compare_tweet_lengths("short","longer")
    -1
    >>>compare_tweet_lengths("same","same")
    0
    
    """
    
    if len(tweet_1) > len(tweet_2):
        return 1
    elif len(tweet_1) < len(tweet_2):
        return -1
    else:
        return 0

def add_hashtag(val_tweet: str, tweet: str) -> str:
    """ Returns a potential tweet given a valid tweet (val_tweet) and a 
    tweet word (tweet). 
    
    add_hashtag will add a hashtag symbol onto the tweet word. It will return
    the potential tweet if it does not exceed MAX_TWEET_LENGTH. Otherwise, 
    it will only return the valid tweet.
    
    Precondition: 0 <= val_tweet <= MAX_TWEET_LENGTH
    
    >>>add_hashtag("Statement is", "true")
    'Statement is #true'
    
    >>>add_hashtag("Very", "short")
    'Very #short'
    
    """
    combine = val_tweet + ' ' + HASHTAG_SYMBOL + tweet
    
    if (is_valid_tweet(combine)):
        return combine
    else:
        return val_tweet

def contains_hashtag(val_tweet: str, tweet: str) -> bool:
    """ Returns True if and only if tweet contains a HASHTAG_SYMBOL and the 
    exact tweet word that is in the string val_tweet.
    
    Precondition: 0 <= val_tweet <= MAX_TWEET_LENGTH
    
    >>>contains_hashtag("I like #csc108","csc108")
    True
    
    >>>contains_hashtag("I like #csc108","csc")
    False
    
    >>>contains_hashtag("I like #csc108, dd","csc108")
    True
    
    """
    clean_val_tweet = clean(val_tweet)
    
    return bool(HASHTAG_SYMBOL + tweet + ' ' in ' ' + clean_val_tweet + ' ')
    

def is_mentioned(val_tweet: str, tweet: str) -> bool:
    """ Returns True if and only if tweet contains a MENTION_SYMBOL and the 
    exact tweet word that is in the string val_tweet.
    
    Precondition: 0 <= val_tweet <= MAX_TWEET_LENGTH
    
    >>>is_mentioned("I like @csc108","csc108")
    True
    
    >>>is_mentioned("I like @csc108","csc")
    False
    
    >>>is_mentioned("I like @csc108, dd","csc108")
    True
    
    """    
    clean_val_tweet = clean(val_tweet)
    
    return bool(MENTION_SYMBOL + tweet + ' ' in ' ' + clean_val_tweet + ' ')

def add_mention_exclusive(val_tweet: str, tweet: str) -> str:
    """ Returns a potential tweet (combines val_tweet and tweet while adding 
    a MENTION_SYMBOL in front of tweet) only if the potential tweet (combined) 
    is valid, val_tweet contains tweet and val_tweet does not mention tweet. 
    Otherwise, it will return val_tweet.
    
    Precondition: 0 <= val_tweet <= MAX_TWEET_LENGTH
    
    >>>add_mention_exclusive("Go Raptors!", "Raptors")
    'Go Raptors! @Raptors'
    
    >>>add_mention_exclusive("Go @Raptors!", "Raptors")
    'Go @Raptors!'
    """
    clean_val_tweet = clean(val_tweet)
    
    combine = val_tweet + ' ' + MENTION_SYMBOL + tweet
    
    if ' ' + tweet + ' ' in ' ' + clean_val_tweet + ' ' \
       and MENTION_SYMBOL not in val_tweet and is_valid_tweet(combine):
        return combine
    else:
        return val_tweet
        
def num_tweets_required(message: str) -> int:
    """ Returns the number of tweets required to display entire
    message 
    
    >>>num_tweets_required("Will return 1 tweet")
    1
    >>>num_tweets_required("This sentence has more than 50 characters 
    and will return 2 tweets")
    2
    """    
    return math.ceil(len(message) / MAX_TWEET_LENGTH)

def get_nth_tweet(message: str, n: int) -> str:
    """ Returns the nth valid tweet in a sequence of tweets 
    (message variable will be split into n tweets). 
    
    Each tweet has a maximum of 50 characters (MAX_TWEET_LENGTH) and the index 
    of the first tweet is 0, the second tweet is 1 and so on. If the value of 
    the second parameter (nth tweet) is too large and there
    is no index-n tweet in the sequence, it will return an empty string.
    
    Precondition n >= 0
    
    >>>get_nth_tweet("This message is short", 0)
    'This message is short'
    
    >>>get_nth_tweet("This message is short", 1)
    ''
    
    >>>get_nth_tweet("This message has more than 50 characters and 
    I will get the 1st sequence", 1)
    'l get the 1st sequence'
    
    """    
    
    num_tweets_text = message[:n * MAX_TWEET_LENGTH]
    
    if n == 0:
        return message[:MAX_TWEET_LENGTH]
    elif n > 0 and len(message) > MAX_TWEET_LENGTH:
        return message[len(num_tweets_text):len(message)]
    else:
        return ""

# A helper function.  Do not modify this function, but you are welcome
# to call it.

def clean(text: str) -> str:
    """Return text with every non-alphanumeric character, except for
    HASHTAG_SYMBOL, MENTION_SYMBOL, and UNDERSCORE, replaced with a
    SPACE, and each HASHTAG_SYMBOL replaced with a SPACE followed by
    the HASHTAG_SYMBOL, and each MENTION_SYMBOL replaced with a SPACE
    followed by a MENTION_SYMBOL.

    >>> clean('A! lot,of punctuation?!!')
    'A  lot of punctuation   '
    >>> clean('With#hash#tags? and@mentions?in#twe_et #end')
    'With #hash #tags  and @mentions in #twe_et  #end'
    """

    clean_str = ''
    for char in text:
        if char.isalnum() or char == UNDERSCORE:
            clean_str = clean_str + char
        elif char == HASHTAG_SYMBOL or char == MENTION_SYMBOL:
            clean_str = clean_str + SPACE + char
        else:
            clean_str = clean_str + SPACE
    return clean_str
