"""A simple checker for types of functions in tweet.py."""

import unittest
import checker_generic
import tweet


class CheckTest(unittest.TestCase):
    """Sanity checker for assignment functions."""

    def testIsValidTweet(self):
        """Function is_valid_tweet."""

        self._check(tweet.is_valid_tweet, ['Hello!'], bool)

    def testCompareTweetLengths(self):
        """ Function compare_tweet_lengths."""

        self._check(tweet.compare_tweet_lengths, ['abc', 'ab'], int)

    def testAddHashtag(self):
        """Function add_hashtag."""
        self._check(tweet.add_hashtag, ['Hello', 'greeting'], str)

    def testContainsHashtag(self):
        """Function contains_hashtag."""

        self._check(tweet.contains_hashtag, ['#hash', 'hash'], bool)

    def testIsMentioned(self):
        """Function is_mentioned."""

        self._check(tweet.is_mentioned, ['@mention', 'mention'], bool)

    def testAddMentionExclusive(self):
        """"Function add_mention_exclusive."""
        self._check(tweet.add_mention_exclusive, [
                    'Hello, World', 'World'], str)

    def testNumTweetsRequired(self):
        """Function num_tweets_required."""
        self._check(tweet.num_tweets_required, ['hello'], int)

    def testGetNthTweet(self):
        """Function get_nth_tweet."""
        self._check(tweet.get_nth_tweet, ['abcdef', 1], str)

    def testCheckConstants(self):
        """Checking constants"""
        print('\nChecking that constants refer to their original values')
        self.assertEqual(tweet.MAX_TWEET_LENGTH, 50,
                         'Set MAX_TWEET_LENGTH to its original value: 50')
        self.assertEqual(tweet.HASHTAG_SYMBOL, '#',
                         'Set HASHTAG_SYMBOL to its original value: \'#\'')
        self.assertEqual(tweet.MENTION_SYMBOL, '@',
                         'Set MENTION_SYMBOL to its original value: \'@\'')
        self.assertEqual(tweet.UNDERSCORE, '_',
                         'Set UNDERSCORE to its original value: \'_\'')
        self.assertEqual(tweet.SPACE, ' ',
                         'Set SPACE to its original value: \' \'')
        print('  check complete')

    def _check(self, func: callable, args: list,
               ret_type: type) -> None:
        """Check that func called with arguments args returns a value of type
        ret_type. Display the progress and the result of the check.

        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker_generic.check(func, args, ret_type)
        self.assertTrue(result[0], result[1])
        print('  check complete')


TARGET_LEN = 79
print(''.center(TARGET_LEN, "="))
print(' Start: checking coding style '.center(TARGET_LEN, "="))
checker_generic.run_pyta('tweet.py', 'pyta/a1_pyta.txt')
print(' End checking coding style '.center(TARGET_LEN, "="))

print(' Start: checking type contracts '.center(TARGET_LEN, "="))
unittest.main(exit=False)
print(' End checking type contracts '.center(TARGET_LEN, "="))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')
