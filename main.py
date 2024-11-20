"""
Crazy Eight Card Game

Author: Luke Williams
"""

from cards import Card, Suit, Rank
from deck import Deck

# Create a test deck
deck = Deck([
    Card(Suit.HEARTS, Rank.TEN),
    Card(Suit.CLUBS, Rank.EIGHT),
    Card(Suit.SPADES, Rank.TWO),
    Card(Suit.JOKER, Rank.JOKER),
    Card(Suit.HEARTS, Rank.ACE),
    Card(Suit.DIAMONDS, Rank.KING),
])

# Look at the top of the deck
print(deck.peek())

# See if we can play the three of diamonds
print(deck.can_add_to(Card(Suit.DIAMONDS, Rank.THREE)))

# See if we can play the three of clubs
print(deck.can_add_to(Card(Suit.CLUBS, Rank.THREE)))
