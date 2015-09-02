# Blackjack Interactive Game

import simplegui
import random
import math

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# card constants
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10,
            'J':10, 'Q':10, 'K':10}

#BlackJack Board Constants   
BOARD_DIM = 600
BUTTON_WDT = int(math.floor(BOARD_DIM / 3)) 
HDR_FNT_SZ = 32 #header font size
SUB_HDR_FNT_SZ = 25 #sub-header font size
OUTCOME_FNT_SZ = 30 
MAIN_FNT_CLR = 'Black'
SCORE_FNT_CLR = 'Blue'
QSTN_FNT_CLR = 'White'
GAME_BGD_CLR = 'Green'
TITLE = "BlackJack"
PLYR_TITLE = "Player"
DLR_TITLE = "Dealer"
TITLE_HT_FCT = 0.07 #title height factor
PLYR_TTL_HT_FCT = 0.17 #player title height factor 
DLR_TTL_HT_FCT =  0.47 #dealery title height factor
HIT_OR_STND_HT_FCT = 0.75 #hit or stand question height factor
DEAL_HT_FCT = 0.95 #New Deal question height factor 
OUTCOME_HT_FCT = 0.9 #outcome text height factor     
PLAYER_INIT_POS = [int(math.floor(BOARD_DIM/30)), 
                        int(math.floor(BOARD_DIM/5))]
DEALER_INIT_POS = [int(math.floor(BOARD_DIM/30)), 
                        int(math.floor(BOARD_DIM/3)) + CARD_SIZE[1]]
SCORE_POS = [int(math.floor(BOARD_DIM/12)), 
                    int(math.floor(BOARD_DIM*11/12))]


def main():
    new_game = BlackJack()

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
        print str(self.suit) + str(self.rank)
        return str(self.suit) + str(self.rank)

    def draw(self, canvas, pos, is_front):
        if is_front:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, 
                [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

        else:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0], CARD_CENTER[1])
            canvas.draw_image(card_back, card_loc, CARD_SIZE, 
                [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            
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
        # count aces as 1, if the hand has an ace, then add 10 to hand value 
        # if it doesn't bust
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
        #print "deck: ", self.deck
        print "deck size: ", len(self.deck)
        card_idx = random.randrange(len(self.deck))
        a = self.deck.pop(card_idx)
        print "dealt card: ", a
        return a
    
    def __str__(self):
        card_deck = "Card Deck: "
        for card in self.deck:
            card_deck += ' ' + card.__str__()
        return card_deck

class BlackJack:
    
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.outcome = ""
        self.in_play = False
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.game_deck = Deck()

        # initialization frame
        self.frame = simplegui.create_frame(TITLE, BOARD_DIM, BOARD_DIM)
        self.frame.set_canvas_background(GAME_BGD_CLR)
        
        # buttons and canvas callbacks
        self.frame.add_button("Deal", self.deal, BUTTON_WDT)
        self.frame.add_button("Hit",  self.hit, BUTTON_WDT)
        self.frame.add_button("Stand", self.stand, BUTTON_WDT)
        self.frame.set_draw_handler(self.draw)
        
        # initialize board with first deal
        self.deal()
        self.frame.start()

    def deal(self):
        if self.in_play:
            self.losses += 1
        self.outcome = None
        self.game_deck = Deck()
        self.game_deck.shuffle()
        self.dealer_hand = Hand()
        self.player_hand = Hand()
        self.dealer_hand.add_card(self.game_deck.deal_card())
        self.player_hand.add_card(self.game_deck.deal_card())
        self.dealer_hand.add_card(self.game_deck.deal_card())
        self.player_hand.add_card(self.game_deck.deal_card())
        self.in_play = True

    def hit(self):
        if self.in_play:
            hand_value = self.player_hand.get_value()
            if hand_value <= 21:
                self.player_hand.add_card(self.game_deck.deal_card())
            else:
                self.outcome = "Busted!"
                self.losses += 1
        print self.outcome
    
    def stand(self):
        global outcome, in_play, game_deck, player_hand, dealer_hand, wins, losses
        if self.in_play:
            if self.outcome != "Busted!" and self.player_hand.get_value() > 21:
                self.outcome = "Busted!"
                self.losses += 1
            else:
                while self.dealer_hand.get_value() < 17:
                    self.dealer_hand.add_card(self.game_deck.deal_card())
                dealer_value = self.dealer_hand.get_value()
                player_value = self.player_hand.get_value()
                if dealer_value > 21 or player_value > dealer_value:
                    self.outcome = "Player wins"
                    self.wins += 1
                else:
                    self.outcome = "Dealer wins"
                    self.losses += 1
        print self.outcome
        self.in_play = False
    
    def center_x(self, text, y_pos_factor):
        '''
        Returns a list of x, y coordinates. The x is centered based on the board
        width and text length to be centered. The y is position is a fraction of
        the board height, based on the input y_pos_factor.
        '''
        half_board = int(math.floor(BOARD_DIM / 2))
        half_text = 10 * int(math.ceil(len(text) / 2))
        return [half_board - half_text, int(math.floor(BOARD_DIM*y_pos_factor))]
    
    def draw(self, canvas):
        global player_hand, dealer_hand, outcome, in_play, wins, losses
        canvas.draw_text(TITLE, self.center_x(TITLE, TITLE_HT_FCT), HDR_FNT_SZ, 
                        MAIN_FNT_CLR)
        self.player_hand.draw(canvas, PLAYER_INIT_POS, False)
        canvas.draw_text(PLYR_TITLE, self.center_x(PLYR_TITLE, PLYR_TTL_HT_FCT), 
                        SUB_HDR_FNT_SZ, MAIN_FNT_CLR)
        self.dealer_hand.draw(canvas, DEALER_INIT_POS, self.in_play)
        canvas.draw_text(DLR_TITLE, self.center_x(DLR_TITLE, DLR_TTL_HT_FCT), 
                        SUB_HDR_FNT_SZ, MAIN_FNT_CLR)
        if self.wins + self.losses == 0:
            current_score = 0.0
        else:
            current_score = round(float(self.wins)/(self.wins + self.losses), 2)
        canvas.draw_text("Current score: " + str(current_score), SCORE_POS, 
                        SUB_HDR_FNT_SZ, SCORE_FNT_CLR)
        if self.outcome != None:
            canvas.draw_text(str(self.outcome), self.center_x(str(self.outcome),
                             OUTCOME_HT_FCT), OUTCOME_FNT_SZ, SCORE_FNT_CLR)
            canvas.draw_text("New deal?", self.center_x("New deal?", 
                            HIT_OR_STND_HT_FCT), SUB_HDR_FNT_SZ,QSTN_FNT_CLR)
        else:
            canvas.draw_text("Hit or stand?", self.center_x("Hit or stand?", 
                HIT_OR_STND_HT_FCT), SUB_HDR_FNT_SZ, QSTN_FNT_CLR)
main()
