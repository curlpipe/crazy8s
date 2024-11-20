"""
Crazy Eight Card Game

Author: Luke Williams
"""

from cards import Card, Suit, Rank
from deck import Deck
from game import Game
from ui import UI

# Create a game
game = Game()
game.set_up()

# Attach a UI and get playing
ui = UI(game)
ui.run()
