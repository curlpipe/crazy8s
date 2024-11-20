"""
Defines the structure of the game
"""

from deck import Deck

# The game class
class Game:
    def __init__(self):
        # Games will default to having two players (for now)
        # The deck at index 0 is the human's deck
        self.decks = [
            Deck([]),
            Deck([]),
        ]
        # Set up the discard and stock piles
        self.stock = Deck.full_deck(True)
        self.discard = Deck([])

    def set_up(self):
        # Shuffle the deck
        self.stock.shuffle()
        # Deal each player 5 cards
        for deck in self.decks:
            for _ in range(5):
                deck.push(self.stock.pop())
        # Create the discard pile
        self.discard.push(self.stock.pop())
