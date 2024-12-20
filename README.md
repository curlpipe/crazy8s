<img width="150px" src="https://raw.githubusercontent.com/curlpipe/crazy8s/refs/heads/main/assets/logo.gif"></img>

# Crazy Eights Card Game

A fun card game, see below for installation instructions and how to play.

You will play against the computer in an attempt to try and win the game.

This game has automated tests, install and run `pytest` to ensure everything is working as intended

More information: [here](https://en.wikipedia.org/wiki/Crazy_Eights), note that my implementation is a slight variation on the original to allow for jokers, but similar nonetheless.

## Installation

This game is written in Python, and will require a minimum version of 3.10 in order to work.

You will also need to run the following command at the root of the project:

```sh
python -m pip install -r requirements.txt
```

this will install all dependencies required.

After installation, you can run the `main.py` file in the folder `src`.

## Rules

### Setting Up

1. Take a standard pack of cards (with or without jokers).
2. Shuffle the deck
3. Each player is dealt 5 cards
4. The cards remaining in the shuffled deck are placed face-down in the middle (this is the *stock pile*)
5. Take the first card from the *stock pile* and place it face-up on a different pile (this is the *discard pile*)

### Getting Started

Players take turns.

During each turn, the player must do the following:

Choose a card from their deck that fits one or more of the following criteria:

- The selected card matches the suit of the card on the top of the discard pile
- The selected card matches the rank of the card on the top of the discard pile
- The card is an 8
- The card is a Joker

So, say you have a 2 of clubs on the top of the discard pile, you may play a card that is either a 2, 8 or club.

Once the card is placed, the player finishes their turn.

*If the player has no valid cards they can play*: they must pick up 1 card from the stock pile and then finish their turn.

### Special Cards

There are several cards that exhibit specific behaviour, these are as follows:

- 8 cards allow the player to change the current suit (e.g. if you were to play an 8, and change the suit to clubs, the players after you must now play a card that matches that suit)
- 2 cards make the next player pick up two cards from the stock pile and miss their go
- Joker and Ace cards make the next player miss their go

### Objective

The player who wins is the one who is first to get rid of their cards.

## Implementation

### Decisions

- I used python for simplicity
- I used tkinter for simplicity and easy installation (it almost always comes pre-packaged with python installations)
- I wrote tests to ensure that core gameplay wasn't modified or broken during subsequent updates and verify that the card game works

### Ideas for improvement

- Adding more players to games e.g. 4 players
- Allowing more configuration such as how many starting cards
- Adding in cards that change the direction of play, e.g. Jacks

## Credits

- [Luke](https://github.com/curlpipe) - Creator
- [me.uk](https://www.me.uk/cards) - Card Images

