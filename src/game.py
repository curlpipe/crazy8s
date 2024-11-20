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

    # Find out who won this game
    def winner_id(self) -> int:
        for id, deck in enumerate(self.decks):
            if len(deck.cards) == 0:
                return id
        return None

    # Play the game (text mode)
    def play_text(self):
        # Players take turns
        while not self.finished():
            for player_id in range(len(self.decks)):
                # Decide whether human or computer should play
                if player_id == 0:
                    self.player_turn(player_id)
                else:
                    self.computer_turn(player_id)
                # Finish the game if there's a winner after this turn
                if self.finished():
                    break
        # Game over! Somebody won
        print(f"Player {self.winner_id() + 1} wins!")

    # Let a player take a turn
    def player_turn(self, player_id: int):
        player_deck = self.decks[player_id]
        # Display game state
        print(f"Player {player_id + 1}'s turn")
        print(f"Your deck: {player_deck}")
        print(f"Top of discard: {self.discard.peek()}")
        # Get selection and ensure it is valid
        valid = False
        while not valid:
            choice = input("Which card (or `pick up`): ")
            if choice == "pick up":
                # User wishes to pick up a card
                new_card = self.stock.pop()
                player_deck.push(new_card)
                print()
                break
            else:
                # User wishes to play a card (work out if valid)
                choice = int(choice)
                valid_range = choice >= 0 and choice < len(player_deck.cards)
                valid = valid_range and self.discard.can_add_to(player_deck.cards[choice])
                if not valid:
                    print("Invalid choice! Try again")
        # If the user entered a valid card to play
        if valid:
            # Remove card from deck and place on discard pile
            choice = self.decks[player_id].remove(choice)
            self.discard.push(choice)
            print()

    # Let the computer take a turn
    def computer_turn(self, player_id: int):
        player_deck = self.decks[player_id]
        print(f"Computer player {player_id + 1}'s turn")
        print(f"It's deck: {player_deck}")
        print(f"Top of discard: {self.discard.peek()}")
        # Get valid selection
        play_this = player_deck.card_to_play(self.discard)
        if play_this is None:
            # No valid cards left to play, pick up
            print("Picking up...")
            new_card = self.stock.pop()
            player_deck.push(new_card)
        else:
            # Valid card at play_this, play it
            print("Playing card...")
            choice = self.decks[player_id].remove(play_this)
            self.discard.push(choice)
        print()
