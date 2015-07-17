# implementation of card game - Memory

import simplegui
import random

def main():
    Memory_game = Memory(20)

class Memory:
    '''
    Memory represents a game where a user has 16 cards face down.
    They can turn over 2 cards at a time. If the cards match, the
    the cards will remain facing up. If they cards don't match,
    they will return facing down. The objective of the came is 
    to achieve all pairs facing up in the lowest amount of self.turns.
    '''
    def __init__(self, num_cards):
        self.turns = 0
        self.state = 0
        self.card_1_idx = None
        self.card_2_idx = None
        if num_cards % 2 > 0:
            raise KeyError("num_cards must be an even integer")
        if num_cards < 8 or num_cards > 20:
            raise KeyError("num_cards must be between [8, 20]")
        self.deck_size = num_cards # deck_size must be an even integer in range [8, 20]
        self.BOARD_WIDTH = 50 * self.deck_size
        self.BOARD_HEIGHT = 100
        
        # create frame and add a button and labels
        self.frame = simplegui.create_frame("Memory", self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.frame.add_button("Reset", self.new_game)
        self.label = self.frame.add_label("Turns = 0")
    
        # register event handlers
        self.frame.set_mouseclick_handler(self.mouseclick)
        self.frame.set_draw_handler(self.draw)
    
        # get things rolling
        self.new_game()
        self.frame.start()

    def new_game(self):
        self.state = 0
        self.turns = 0
        self.deck = []
        for card in range(self.deck_size / 2):
            self.deck.append(card)
            self.deck.append(card)
        random.shuffle(self.deck) 
        self.exposed = [False for i in range(self.deck_size)]

    def expose(self):
        if self.mouse_pos[1] >= 0 and self.mouse_pos[1] <= self.BOARD_HEIGHT:
            increment = self.BOARD_WIDTH / self.deck_size
            x_pos_1 = 0
            x_pos_2 = increment
            card = 0
            found = False
            while x_pos_2 <= self.BOARD_WIDTH and card < self.deck_size and not found:
                if self.exposed[card] != True:
                    if self.mouse_pos[0] >= x_pos_1 and self.mouse_pos[0] <= x_pos_2:
                        self.exposed[card] = True
                        if self.card_1_idx == None:
                            self.card_1_idx = card
                            found = True
                        elif self.card_2_idx == None:
                            self.card_2_idx = card
                            found = True
                x_pos_1 += increment
                x_pos_2 += increment
                card += 1
                    
    def mouseclick(self, pos):
        self.mouse_pos = pos
        if self.state == 2:
            self.state = 1
            if self.card_1_idx != None and self.card_2_idx != None:
                if self.deck[self.card_1_idx] != self.deck[self.card_2_idx]:
                    self.exposed[self.card_1_idx] = False
                    self.exposed[self.card_2_idx] = False
            self.card_1_idx = None
            self.card_2_idx = None
            self.expose()
            self.turns += 1
            
        elif self.state == 1:
            self.state = 2
            self.expose()
            self.turns += 1
        else:
            self.state = 1
            self.expose()
            self.turns +=1
     
    def draw(self, canvas):
        x_pos_1 = 0
        x_pos_2 = self.BOARD_WIDTH / self.deck_size
        for idx, card in enumerate(self.deck):
            if self.exposed[idx] == True:
                canvas.draw_polygon([(x_pos_2,100), (x_pos_1,100), (x_pos_1,0), (x_pos_2,0)], 3, 'Black', 'Red')
                canvas.draw_text(str(card), (x_pos_1 + (self.BOARD_WIDTH / self.deck_size) / 5, 0.7 * self.BOARD_HEIGHT), 0.6 * self.BOARD_HEIGHT, 'Black')
            else:
                canvas.draw_polygon([(x_pos_2,100), (x_pos_1,100), (x_pos_1,0), (x_pos_2,0)], 3, 'Black', 'Green')
            x_pos_1 += self.BOARD_WIDTH / self.deck_size
            x_pos_2 += self.BOARD_WIDTH / self.deck_size
        self.label.set_text("self.turns = " + str(self.turns))  

main()
