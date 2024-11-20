"""
For handling the UI of the game
"""

from tkinter import *
from PIL import Image, ImageTk
from cards import Card, Suit, Rank
from game import Game
import random
import time
import os

# UI class
class UI:
    # UI will contain the game
    def __init__(self, game: Game):
        self.game = game
        self.root = Tk()
        self.root.geometry("800x600")
        self.root.title("Crazy Eights!")
        self.root.config(bg="#033500")

        # Storage to prevent PhotoImages from being garbage collected
        self.storage = []

        self.paused = False

        # Show exit button
        self.exit_button = Button(self.root, text="Exit", command=self.quit, font=("Verdana", 12))
        self.exit_button.place(relx=0.01, rely=0.01)
        
        # Show game state
        self.state = Label(self.root, text=f"Your Turn!", fg="white", bg="#033500", font=("Verdana", 20), pady=10)
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
            if "src" in os.getcwd(): path = f"../assets/{suit}.png"
            else: path = f"assets/{suit}.png"
            image = Image.open(path)
            image = image.resize((30, 30))
            photo = ImageTk.PhotoImage(image)
            self.suits[suit] = photo

    def run(self):
        try:
            mainloop()
        except KeyboardInterrupt:
            print("Goodbye")

    def quit(self):
        self.root.destroy()

    def show_card(self, card: Card, x: float, y: float) -> Label:
        image = Image.open(card.get_image_path() + ".png")
        image = image.resize((120, 168))
        photo = ImageTk.PhotoImage(image)
        label = Label(self.root, image=photo)
        self.storage.append(photo)
        label.place(relx=x, rely=y, anchor="center")
        return label
    
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

    def render_discard(self):
        # Destroy the discard pile if possible
        try: self.discard_pile.destroy()
        except: pass
        # Show the discard pile
        self.discard_pile = self.show_card(self.game.discard.peek(), 0.3333, 0.4)

    def render_opponent(self):
        # Destroy all of the opponents cards
        for image in self.opponent:
            image.destroy()
        # Render the updated deck
        card_number = len(self.game.decks[1].cards)
        if card_number == 0: return # Prevent 0 division
        increment = 0.7 / card_number
        self.opponent = []
        for i in range(card_number):
            self.opponent.append(self.show_card_back(0.2 + increment * i, 0.04))

    def render_player(self):
        # Destroy all of the opponents cards
        for image in self.players:
            image.destroy()
        # Render the updated deck
        card_number = len(self.game.decks[0].cards)
        if card_number == 0: return # Prevent 0 division
        increment = 0.7 / card_number
        self.players = []
        for i, card in enumerate(self.game.decks[0].cards):
            card = self.show_card(card, 0.2 + increment * i, 0.74)
            card.bind("<Button-1>", lambda event, choice=i: self.play_card(event, choice))
            self.players.append(card)

    def pick_up(self, event):
        if self.game.current_player == 0:
            player_deck = self.game.decks[self.game.current_player]
            new_card = self.game.stock.pop()
            player_deck.push(new_card)
            self.render_player()
            self.next_player()

    def play_card(self, event, choice):
        if self.game.current_player == 0:
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
                    self.victory_message = Label(self.root, text="You Won!", font=("Verdana", 60), bg="#033500", fg="white", padx=1000, pady=1000)
                    self.victory_message.place(relx=0.5, rely=0.5, anchor="center")
                    self.root.after(5000, self.quit)
                else:
                    self.next_player()
            else:
                print("Invalid choice! Try again")

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
        for card in self.game.discard.cards: self.game.stock.cards.insert(0, card)
        self.game.discard.cards = [top]

    def handle_computer(self):
        # Non-blocking way to wait until the game unpauses
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
            self.victory_message = Label(self.root, text="You Lost!", font=("Verdana", 60), bg="#033500", fg="white", padx=1000, pady=1000)
            self.victory_message.place(relx=0.5, rely=0.5, anchor="center")
            self.root.after(5000, self.quit)

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
        self.heart_button.bind("<Button-1>", lambda event: self.do_suit_selection(event, Suit.HEARTS))
        self.club_button.bind("<Button-1>", lambda event: self.do_suit_selection(event, Suit.CLUBS))
        self.diamond_button.bind("<Button-1>", lambda event: self.do_suit_selection(event, Suit.DIAMONDS))
        self.spade_button.bind("<Button-1>", lambda event: self.do_suit_selection(event, Suit.SPADES))
        # Display message to player to pick a suit
        self.state.config(text="Choose a suit")

    # Make a suit selection
    def do_suit_selection(self, event, suit: Suit):
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
