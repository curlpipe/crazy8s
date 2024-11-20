"""
This defines decks, a list of cards, used to represent player's hands and the stock / discard piles
"""

from cards import Card

# The deck class
class Deck:
    # By default, a deck is empty unless otherwise provided through arguments
    def __init__(self, cards=[]):
        self.cards = cards

    # Method to add a card
    def push(self, card_to_add: Card):
        self.cards.append(card_to_add)

    # Method to remove a card from the deck
    def remove(self, idx: int):
        del self.cards[idx]

    # Method to get the card at the top of the deck
    def peek(self) -> Card:
        return self.cards[len(self.cards) - 1]

    # Assuming this is the discard pile, work out if a card can be added
    def can_add_to(self, card_to_check: Card) -> bool:
        top_card = self.peek()
        # Check various conditions (not the most efficient - but the code is clean)
        is_eight = card_to_check.rank == Rank.EIGHT
        common_rank = card_to_check.rank == top_card.rank
        common_suit = card_to_check.suit == top_card.suit
        # Work out if any condition is met
        return is_eight or common_rank or common_suit

    # Assuming this is a player's hand, get the index of a valid card to play
    def card_to_play(self, discard_pile) -> int:
        for index, card in enumerate(self.cards):
            if discard_pile.can_add_to(card):
                return index
        # No cards are valid, represent this state as None
        return None

    # Allow comparison of decks
    def __eq__(self, other):
        # Discrepancy based on length
        if len(self.cards) != len(other.cards):
            return False
        # Discrepancy based on contents
        for ours, theirs in zip(self.cards, other.cards):
            if ours != theirs:
                return False
        # Passed all checks, these decks are identical
        return True
