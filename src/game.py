"""
Defines the structure of the game
"""

from cards import Card, Suit, Rank
from deck import Deck

# The game class
class Game:
    def __init__(self):
        # Games will default to having two players (for now)
        self.current_player = 0
        # The deck at index 0 is the human's deck
        self.decks = [
            Deck([]),
            Deck([]),
        ]
        # Set up the discard and stock piles
        self.stock = Deck.full_deck(False)
        self.discard = Deck([])

    # Set up the game
    def set_up(self):
        # Shuffle the deck
        self.stock.shuffle()
        # Deal each player 5 cards
        for deck in self.decks:
            for _ in range(5):
                deck.push(self.stock.pop())
        # Create the discard pile
        self.discard.push(self.stock.pop())

    # Check for finishing conditions
    def finished(self) -> bool:
        # A game is finished when a player has no cards left
        return any(filter(lambda deck: len(deck.cards) == 0, self.decks))

    # Let the computer take a turn
    # Returns true if the computer could take a turn
    def computer_turn(self) -> bool:
        player_deck = self.decks[self.current_player]
        # Get valid selection
        play_this = player_deck.card_to_play(self.discard)
        if play_this is None:
            # No valid cards left to play, pick up
            new_card = self.stock.pop()
            player_deck.push(new_card)
        else:
            # Valid card at play_this, play it
            choice = self.decks[self.current_player].remove(play_this)
            self.discard.push(choice)
        return play_this is not None

    # Handle special cards (for the computer player)
    def handle_special_card_computer(self, card: Card):
        match card.rank:
            case Rank.EIGHT:
                # Handle 8 card
                self.change_suit_computer()
            case Rank.TWO:
                # Handle 2 card
                self.pickup_2()
            case Rank.ACE:
                # Handle ace card
                self.skip_go()
            case Rank.JOKER:
                # Handle joker card
                self.skip_go()

    # Allow the player to change the suit
    def change_suit_computer(self):
        # Strategy: select the suit which the computer has the most of
        count = { "hearts": 0, "diamonds": 0, "clubs": 0, "spades": 0 }
        for card in self.decks[self.current_player].cards:
            match card.suit:
                case Suit.HEARTS:
                    count["hearts"] += 1
                case Suit.DIAMONDS:
                    count["diamonds"] += 1
                case Suit.CLUBS:
                    count["clubs"] += 1
                case Suit.SPADES:
                    count["spades"] += 1
        choice = sorted(count.items(), key=lambda x: x[1], reverse=True)[0][0]
        match choice:
            case "hearts":
                self.discard.cards[len(self.discard.cards) - 1].suit = Suit.HEARTS
            case "diamonds":
                self.discard.cards[len(self.discard.cards) - 1].suit = Suit.DIAMONDS
            case "clubs":
                self.discard.cards[len(self.discard.cards) - 1].suit = Suit.CLUBS
            case "spades":
                self.discard.cards[len(self.discard.cards) - 1].suit = Suit.SPADES

    # Skip the next go of the player
    def skip_go(self):
        self.next_player()

    # Make the next player pick up 2 cards
    def pickup_2(self):
        next_player_id = (self.current_player + 1) % len(self.decks)
        player_deck = self.decks[next_player_id]
        for i in range(2):
            new_card = self.stock.pop()
            player_deck.push(new_card)

    # Move to the next player
    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.decks)
