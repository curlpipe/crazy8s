"""
For handling the UI of the game
"""

import random
import os
from tkinter import Tk, Label, Button, mainloop
from PIL import Image, ImageTk
from cards import Card, Suit, Rank
from game import Game

# UI class
class UI:
    # UI will contain the game
    def __init__(self, jokers: bool):
        self.jokers = jokers
        self.game = Game(self.jokers)
        self.game.set_up()
        self.root = Tk()
        self.root.geometry("900x700")
        self.root.title("Crazy Eights!")
        self.root.config(bg="#033500")

        # Storage to prevent PhotoImages from being garbage collected
        self.storage = []

        self.just_restarted = False
        self.paused = False

        # Show exit and new game buttons
        self.exit_button = Button(
            self.root,
            text="Exit",
            command=self.quit,
            font=("Verdana", 12),
            width=5
        )
        self.exit_button.place(relx=0.01, rely=0.01)
        self.new_game_button = Button(
            self.root,
            text="New\nGame",
            command=self.new_game,
            font=("Verdana", 12),
            width=5
        )
        self.new_game_button.place(relx=0.01, rely=0.07)

        # Show game state
        self.state = Label(
            self.root,
            text="Your Turn!",
            fg="white",
            bg="#033500",
            font=("Verdana", 20),
            pady=10
        )
        self.state.pack(side="bottom")

        # Render discard and stock piles
        self.render_discard()
        self.stock_pile = self.show_card_back(0.6666, 0.4)

        # Provide pick-up behaviour
        self.stock_pile.bind("<Button-1>", self.pick_up)

        # Render the decks of all the players
        self.opponent = []
        self.players = []
        self.render_opponent()
        self.render_player()

        # Load in images of suits (for suit picker)
        self.suits = {}
        for suit in ["heart", "diamond", "spade", "club"]:
            if "src" in os.getcwd():
                path = f"../assets/{suit}.png"
            else: path = f"assets/{suit}.png"
            image = Image.open(path)
            image = image.resize((30, 30))
            photo = ImageTk.PhotoImage(image)
            self.suits[suit] = photo

    # Run the game and show the UI
    def run(self):
        try:
            mainloop()
        except KeyboardInterrupt:
            pass

    # Exit the game
    def quit(self):
        self.root.destroy()

    # Render a card at a certain location
    def show_card(self, card: Card, x: float, y: float) -> Label:
        image = Image.open(card.get_image_path() + ".png")
        image = image.resize((120, 168))
        photo = ImageTk.PhotoImage(image)
        label = Label(self.root, image=photo)
        self.storage.append(photo)
        label.place(relx=x, rely=y, anchor="center")
        return label

    # Render the back of a card at a certain location
    def show_card_back(self, x: float, y: float) -> Label:
        if "src" in os.getcwd():
            path = "../assets/back.png"
        else:
            path = "assets/back.png"
        image = Image.open(path)
        image = image.resize((120, 168))
        photo = ImageTk.PhotoImage(image)
        label = Label(self.root, image=photo)
        self.storage.append(photo)
        label.place(relx=x, rely=y, anchor="center")
        return label

    # Render the discard pile
    def render_discard(self):
        # Destroy the discard pile if possible
        try:
            self.discard_pile.destroy()
        except:
            pass
        # Show the discard pile
        self.discard_pile = self.show_card(self.game.discard.peek(), 0.3333, 0.4)

    # Render the hand of the opponent
    def render_opponent(self):
        # Destroy all of the opponents cards
        for image in self.opponent:
            image.destroy()
        # Render the updated deck
        card_number = len(self.game.decks[1].cards)
        if card_number == 0:
            # Prevent 0 division
            return
        increment = 0.7 / card_number
        self.opponent = []
        for i in range(card_number):
            self.opponent.append(self.show_card_back(0.2 + increment * i, 0.04))

    # Render the player's hand
    def render_player(self):
        # Destroy all of the opponents cards
        for image in self.players:
            image.destroy()
        # Render the updated deck
        card_number = len(self.game.decks[0].cards)
        if card_number == 0:
            # Prevent 0 division
            return
        increment = 0.7 / card_number
        self.players = []
        for i, card in enumerate(self.game.decks[0].cards):
            card = self.show_card(card, 0.2 + increment * i, 0.74)
            card.bind("<Button-1>", lambda event, choice=i: self.play_card(event, choice))
            self.players.append(card)

    # Handle the player wanting to pick up a card
    def pick_up(self, _):
        if self.game.current_player == 0:
            self.just_restarted = False
            player_deck = self.game.decks[self.game.current_player]
            new_card = self.game.stock.pop()
            player_deck.push(new_card)
            self.render_player()
            self.next_player()

    # Handle the player playing a card
    def play_card(self, _, choice):
        if self.game.current_player == 0:
            self.just_restarted = False
            player_deck = self.game.decks[0]
            valid_range = choice >= 0 and choice < len(player_deck.cards)
            valid = valid_range and self.game.discard.can_add_to(player_deck.cards[choice])
            if valid:
                choice = self.game.decks[0].remove(choice)
                self.game.discard.push(choice)
                self.handle_special_card(self.game.discard.peek())
                self.render_discard()
                self.render_player()
                self.render_opponent()
                if self.game.finished():
                    # Game over, player won!
                    self.victory_message = Label(
                        self.root,
                        text="You Won!",
                        font=("Verdana", 60),
                        bg="#033500",
                        fg="white",
                        padx=1000,
                        pady=1000
                    )
                    self.victory_message.place(relx=0.5, rely=0.5, anchor="center")
                    self.exit_button.lift()
                    self.new_game_button.lift()
                else:
                    self.next_player()
            else:
                self.state.config(text="Card doesn't match, please choose another or pick up")

    # Move to the next player
    def next_player(self):
        self.game.next_player()
        if self.game.current_player == 0:
            self.state.config(text="Your Turn")
        else:
            # Update turn display (if not paused)
            if not self.paused:
                self.state.config(text="Computer's Turn")
            # Handle computer's go (simulate thinking time)
            self.root.after(random.randint(2000, 3000), self.handle_computer)
        # Refill the stock pile (to prevent running out)
        top = self.game.discard.pop()
        for card in self.game.discard.cards:
            self.game.stock.cards.insert(0, card)
        self.game.discard.cards = [top]

    # Handle the computer's turn
    def handle_computer(self):
        # Non-blocking way to wait until the game unpauses
        if self.just_restarted:
            self.just_restarted = False
            self.paused = False
            return
        if self.paused:
            self.root.after(random.randint(2000, 3000), self.handle_computer)
            return
        # Handle the computer's go
        if self.game.computer_turn():
            self.game.handle_special_card_computer(self.game.discard.peek())
        self.render_opponent()
        self.render_player()
        self.render_discard()
        self.next_player()
        if self.game.finished():
            # Game over, computer won!
            self.victory_message = Label(
                self.root,
                text="You Lost!",
                font=("Verdana", 60),
                bg="#033500",
                fg="white",
                padx=1000,
                pady=1000
            )
            self.victory_message.place(relx=0.5, rely=0.5, anchor="center")
            self.exit_button.lift()
            self.new_game_button.lift()

    # Handle special cards (player facing)
    def handle_special_card(self, card: Card):
        match card.rank:
            case Rank.EIGHT:
                # Handle 8 card
                self.pick_suit()
            case Rank.TWO:
                # Handle 2 card
                self.game.pickup_2()
            case Rank.ACE:
                # Handle ace card
                self.game.skip_go()
            case Rank.JOKER:
                # Handle joker card
                self.game.skip_go()

    # Show the suit picker and return the selection
    def pick_suit(self):
        # Pause the gameplay for now
        self.paused = True
        # Show the new suit picker
        self.heart_button = Label(self.root, image=self.suits["heart"])
        self.club_button = Label(self.root, image=self.suits["club"])
        self.diamond_button = Label(self.root, image=self.suits["diamond"])
        self.spade_button = Label(self.root, image=self.suits["spade"])
        self.heart_button.place(relx=0.35, rely=0.9, anchor="center")
        self.club_button.place(relx=0.45, rely=0.9, anchor="center")
        self.diamond_button.place(relx=0.55, rely=0.9, anchor="center")
        self.spade_button.place(relx=0.65, rely=0.9, anchor="center")
        self.heart_button.bind(
            "<Button-1>",
            lambda event: self.do_suit_selection(event, Suit.HEARTS)
        )
        self.club_button.bind(
            "<Button-1>",
            lambda event: self.do_suit_selection(event, Suit.CLUBS)
        )
        self.diamond_button.bind(
            "<Button-1>",
            lambda event: self.do_suit_selection(event, Suit.DIAMONDS)
        )
        self.spade_button.bind(
            "<Button-1>",
            lambda event: self.do_suit_selection(event, Suit.SPADES)
        )
        # Display message to player to pick a suit
        self.state.config(text="Choose a suit")

    # Make a suit selection
    def do_suit_selection(self, _, suit: Suit):
        self.state.config(text="Computer's Turn")
        # Set the suit
        self.game.discard.cards[len(self.game.discard.cards) - 1].suit = suit
        self.render_discard()
        # Destroy any old suit picker
        try:
            self.heart_button.destroy()
            self.club_button.destroy()
            self.diamond_button.destroy()
            self.spade_button.destroy()
        except:
            pass
        # Unpause and continue the game
        self.paused = False

    # Replay the game
    def new_game(self):
        self.victory_message.destroy()
        self.just_restarted = True
        self.paused = False
        self.game = Game(self.jokers)
        self.game.set_up()
        self.state.config(text="Your Turn")
        self.render_opponent()
        self.render_player()
        self.render_discard()
        try:
            self.heart_button.destroy()
            self.club_button.destroy()
            self.diamond_button.destroy()
            self.spade_button.destroy()
        except:
            pass

# Function to run code depending on whether or not the user wishes to use jokers
def ask_user_if_jokers(yes_jokers, no_jokers):
    root = Tk()
    root.title("Crazy Eights: Jokers or no Jokers")
    root.config(bg="#033500")

    def handle_event(jokers: bool):
        root.destroy()
        if jokers:
            yes_jokers()
        else:
            no_jokers()

    question = Label(
        root,
        text="Welcome to the Crazy Eights card game\nDo you want to add jokers to the pack?",
        bg="#033500",
        fg="white",
        font=("Verdana", 30)
    )
    question.pack()

    positive = Button(
        root,
        text="Yes, add in jokers",
        pady=10,
        command=lambda: handle_event(True),
        font=("Verdana", 20)
    )
    positive.pack()
    negative = Button(
        root,
        text="No, do not add in jokers",
        pady=10,
        command=lambda: handle_event(False),
        font=("Verdana", 20)
    )
    negative.pack()

    root.mainloop()
