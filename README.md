# Crazy Eights Card Game

A fun card game, see below for installation instructions and how to play

More information: [here](https://en.wikipedia.org/wiki/Crazy_Eights)

## Installation

This game is written in Python, and will require a minimum version of 3.10 in order to work.

You will also need to run the following command at the root of the project:

```sh
python -m pip install -r requirements.txt
```

this will install all dependencies required.

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

Choose a card from their deck that fits one or more of following criteria:

- The selected card matches the suit of the card on the top of the discard pile
- The selected card matches the rank of the card on the top of the discard pile
- The card is an 8

So, say you have a 2 of clubs on the top of the discard pile, you may play a card that is either a 2, 8 or club.

Once the card is placed, the player finishes their turn.

*If the player has no valid cards they can play*: they must pick up 2 cards from the stock pile and then finish their turn.

### Special Cards

There are several cards that exhibit specific behaviour, these are as follows:

- 8 cards allow the player to change the current suit (e.g. if you were to play an 8, and change the suit to clubs, the players after you must now play a card that matches that suit)
- 2 cards make the next player pick up 2 cards and miss their go
- Joker and Ace cards make the next player miss their go

### Objective

The player who wins is the one who is first to get rid of their entire deck.

## Credits

- [Luke](https://github.com/curlpipe) - Creator
- [me.uk](https://www.me.uk/cards) - Card Images

