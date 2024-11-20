"""
Crazy Eight Card Game

Author: Luke Williams
"""

from cards import Card, Suit, Rank
from deck import Deck
from game import Game
from ui import UI

# Attach a UI and get playing
ui = UI()
ui.run()
