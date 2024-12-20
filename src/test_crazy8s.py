"""
Automated tests for the card game to squash out any bugs and provide peace of mind
"""

from cards import Card, Suit, Rank
from deck import Deck
from game import Game
import os

# Test cards
def test_cards():
    # Check out suit and rank enums
    assert Suit.HEARTS == Suit.HEARTS
    # Test images are retrieved correctly
    card = Card(Suit.DIAMONDS, Rank.ACE)
    path = "assets/AD.svg"
    if "src" in os.getcwd():
        path = "../" + path
    f = open(path, "r", encoding="utf-8")
    data = f.read()
    f.close()
    assert card.get_image() == data
    card = Card(Suit.JOKER, Rank.JOKER)
    path = "assets/1J.svg"
    if "src" in os.getcwd():
        path = "../" + path
    f = open(path, "r", encoding="utf-8")
    data = f.read()
    f.close()
    assert card.get_image() == data

# Test decks
def test_decks():
    # Test creation of deck
    deck = Deck()
    assert deck == Deck([])
    deck = Deck([Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.SIX)])
    assert deck == Deck([Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.SIX)])
    # Test adding to decks
    deck.push(Card(Suit.SPADES, Rank.TEN))
    assert deck == Deck([Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.SIX), Card(Suit.SPADES, Rank.TEN)])
    # Test removing from decs
    deck.remove(1)
    assert deck == Deck([Card(Suit.HEARTS, Rank.KING), Card(Suit.SPADES, Rank.TEN)])
    # Test getting the top of the deck
    assert deck.peek() == Card(Suit.SPADES, Rank.TEN)
    # Test discard pile card validation
    assert deck.can_add_to(Card(Suit.SPADES, Rank.TEN)) # Yes, based on suit and rank
    assert deck.can_add_to(Card(Suit.SPADES, Rank.NINE)) # Yes, based on suit
    assert deck.can_add_to(Card(Suit.DIAMONDS, Rank.TEN)) # Yes, based on rank
    assert deck.can_add_to(Card(Suit.SPADES, Rank.EIGHT)) # Yes, card is an eight
    assert deck.can_add_to(Card(Suit.DIAMONDS, Rank.EIGHT)) # Yes, card is an eight
    assert deck.can_add_to(Card(Suit.JOKER, Rank.JOKER)) # Yes, card is a joker
    assert not deck.can_add_to(Card(Suit.CLUBS, Rank.THREE)) # No, not eight, no matches of rank or suit
    assert not deck.can_add_to(Card(Suit.HEARTS, Rank.FIVE)) # No, not eight, no matches of rank or suit
    # Test selection of valid cards to play
    hand = Deck([Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.TEN)])
    assert hand.card_to_play(deck) == 1
    hand = Deck([Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.FOUR)])
    assert hand.card_to_play(deck) == None
    # Test shuffling
    deck = Deck.full_deck(True)
    deck.shuffle()
    assert not deck == Deck.full_deck(True)
    # Test popping from deck
    deck = Deck.full_deck(True)
    assert deck.pop() == Card(Suit.CLUBS, Rank.KING)

def test_game():
    game = Game(False)
    # Test finishing condition
    assert game.finished()
    # Test setting up
    game.set_up()
    assert len(game.decks[0].cards) == 5
    assert len(game.decks[1].cards) == 5
    assert len(game.discard.cards) == 1
    assert len(game.stock.cards) == 41
    # Test finishing condition
    assert not game.finished()
