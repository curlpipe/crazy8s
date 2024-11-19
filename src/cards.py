"""
This file defines the structure and behaviour of cards
"""

from enum import Enum
import os

# Suits
class Suit(Enum):
    HEARTS = 1
    DIAMONDS = 2
    SPADES = 3
    CLUBS = 4
    JOKER = 5

# Ranks
class Rank(Enum):
    ACE = 1 # Note: ACE represents a value of 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    JOKER = 14

# The card class
class Card:
    # Cards are defined as having a suit and a rank
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
    
    # Method to get the svg data representing this card
    def get_image(self) -> str:
        # Calculate the suit component
        match self.suit:
            case Suit.HEARTS:
                suit = "H"
            case Suit.DIAMONDS:
                suit = "D"
            case Suit.SPADES:
                suit = "S"
            case Suit.CLUBS:
                suit = "C"
            case Suit.JOKER:
                suit = "J"
        # Calculate the rank component
        match self.rank:
            case Rank.ACE:
                rank = "A"
            case Rank.TWO:
                rank = "2"
            case Rank.THREE:
                rank = "3"
            case Rank.FOUR:
                rank = "4"
            case Rank.FIVE:
                rank = "5"
            case Rank.SIX:
                rank = "6"
            case Rank.SEVEN:
                rank = "7"
            case Rank.EIGHT:
                rank = "8"
            case Rank.NINE:
                rank = "9"
            case Rank.TEN:
                rank = "10"
            case Rank.JACK:
                rank = "J"
            case Rank.QUEEN:
                rank = "Q"
            case Rank.KING:
                rank = "K"
            case Rank.JOKER:
                rank = "1"
        
        # Build the path
        path = f"assets/{rank}{suit}.svg"
        if "src" in os.getcwd():
            path = "../" + path
        # Read the data from the svg
        f = open(path, "r")
        data = f.read()
        f.close()
        # Return the data
        return data
            
            
