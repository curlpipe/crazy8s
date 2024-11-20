"""
Crazy Eight Card Game

Author: Luke Williams
"""

from cards import Card, Suit, Rank
from deck import Deck
from game import Game
from ui import UI, ask_user_if_jokers

# Work out whether or not to use jokers and run the correct version of the game
use_jokers = ask_user_if_jokers(
    lambda: UI(True).run(), # User doesn't want jokers
    lambda: UI(False).run(), # User does want jokers
)
