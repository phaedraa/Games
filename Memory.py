# Blackjack

import simplegui
import random
import math

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# game global variables
in_play = False
outcome = ""
wins = 0
losses = 0
BOARD_DIM = 600

# card constant globals
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return str(self.suit) + str(self.rank)
    
    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
    
    def get_card(self):
        return self.suit + self.rank

    def draw(self, canvas, pos, is_front):
        if is_front:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

        else:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0], CARD_CENTER[1])
            canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            
class Hand:
    def __init__(self):
        self.card_list = [] # create Hand object

    def __str__(self):
        if len(self.card_list) == 0:
            return "Hand is empty"
        else:
            hand = []
            for card in self.card_list:
                card_type = card.get_suit() + card.get_rank()
                hand.append(card_type)
            return str(hand)

    def add_card(self, card):
        if card.get_suit() not in SUITS and card.get_rank() not in RANKS:
            raise TypeError("Added card must be of type Card")
        self.card_list.append(card) # add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        has_Ace = False
        for card in self.card_list:
            rank = card.get_rank()
            value += VALUES[rank]
            if not has_Ace:
                if rank == 'A':
                    has_Ace = True
        if has_Ace:
            if value + 10 <= 21:
                value += 10
        return value
        
    def draw(self, canvas, pos, dealer_inplay):
        x_pos = pos[0]
        card = self.card_list[0]
        if dealer_inplay:
            card.draw(canvas, [x_pos, pos[1]], False)
        else:
            card.draw(canvas, [x_pos, pos[1]], True)
        x_pos += CARD_SIZE[0]
        for card in self.card_list[1:]:
            card.draw(canvas, [x_pos, pos[1]], True)
            x_pos += CARD_SIZE[0]

class Deck:
    def __init__(self):
        deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                deck.append(card)
        self.deck = deck
        
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal_card(self):
        card_idx = random.randrange(len(self.deck))
        return self.deck.pop(card_idx)
    
    def __str__(self):
        card_deck = "Card Deck: "
        for card in self.deck:
            card_deck += ' ' + card.get_card()
        return card_deck

def deal():
    global outcome, in_play, game_deck, player_hand, dealer_hand, wins, losses
    if in_play:
        losses += 1
    outcome = None
    game_deck = Deck()
    game_deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    dealer_hand.add_card(game_deck.deal_card())
    player_hand.add_card(game_deck.deal_card())
    dealer_hand.add_card(game_deck.deal_card())
    player_hand.add_card(game_deck.deal_card())
    in_play = True

def hit():
    global outcome, in_play, game_deck, player_hand, dealer_hand, wins, losses
    if in_play:
        hand_value = player_hand.get_value()
        if hand_value <= 21:
            player_hand.add_card(game_deck.deal_card())
        else:
            outcome = "Busted!"
            losses += 1
    print outcome
    
def stand():
    global outcome, in_play, game_deck, player_hand, dealer_hand, wins, losses
    if in_play:
        if outcome == "Busted!":
            print outcome
        elif player_hand.get_value() > 21:
            outcome = "Busted!"
            print outcome
            losses += 1
        else:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(game_deck.deal_card())
            dealer_value = dealer_hand.get_value()
            player_value = player_hand.get_value()
            if dealer_value > 21 or player_value > dealer_value:
                outcome = "Player wins"
                print outcome
                wins += 1
            else:
                outcome = "Dealer wins"
                print outcome
                losses += 1
    in_play = False
    
def center_x(text, y_pos_factor):
    half_board = int(math.floor(BOARD_DIM / 2))
    half_text = 10 * int(math.ceil(len(text) / 2))
    return [half_board - half_text, int(math.floor(BOARD_DIM * y_pos_factor))]
    
def draw(canvas):
    global player_hand, dealer_hand, outcome, in_play, wins, losses
    canvas.draw_text("BlackJack", center_x("BlackJack", .07), 32, 'Black')
    player_hand.draw(canvas, [20, 120], False)
    canvas.draw_text("Player", center_x("Player", .17), 25, 'Black')
    dealer_hand.draw(canvas, [20, 200 + CARD_SIZE[1]], in_play)
    canvas.draw_text("Dealer", center_x("Dealer", .47), 25, 'Black')
    if wins + losses == 0:
        current_score = 0.0
    else:
        current_score = round(float(wins)/(wins + losses), 2)
    canvas.draw_text("Current score: " + str(current_score), [50, 550], 25, 'Blue')
    if outcome != None:
        canvas.draw_text(str(outcome), center_x(str(outcome), 0.9), 30, 'White')
        canvas.draw_text("New deal?", center_x("New deal?", .95), 25, 'White')
    else:
        canvas.draw_text("Hit or stand?", center_x("Hit or stand?", .75), 25, 'White')
    
# initialization frame
frame = simplegui.create_frame("Blackjack", BOARD_DIM, BOARD_DIM)
frame.set_canvas_background("Green")

# buttons and canvas callbacks
button_width = int(math.floor(BOARD_DIM / 3))
frame.add_button("Deal", deal, button_width)
frame.add_button("Hit",  hit, button_width)
frame.add_button("Stand", stand, button_width)
frame.set_draw_handler(draw)

# initialize board with first deal
deal()
frame.start()