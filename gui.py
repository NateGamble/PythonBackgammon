'''GUI for Backgammon game
Created April 2017
@author: Nate Gamble (neg6)
'''

from tkinter import *
from backgammon_black import *
from backgammon_white import *
import random
import time
from Backgammon_Game import roll

TRI_HEIGHT = 100
TRI_WIDTH = 20

class BackgammonGame:
    
    def __init__(self, window):
        self.window = window
        
        self._rgrid = Grid()
        self._canvas = Canvas(self.window, width = 13 * TRI_WIDTH, height = 3 * TRI_HEIGHT)
        
        self.rolls = StringVar()
        self.roll_frame = Frame(self.window)
        
        self.whosTurn = StringVar()
        self.whosTurn.set("It's your turn! Roll the dice!")
        
        self.rollButton = Button(self.roll_frame, text = 'Roll', command = self.roll)
        self.dieLabel = Label(self.roll_frame, textvariable = self.rolls)
        self.turnLabel = Label(self.window, textvariable = self.whosTurn)
        self.endButton = Button(self.roll_frame, text = 'End Turn (if stuck)',command = self.end_turn)
                
        for space in range(12):
            self._canvas.create_polygon(space * TRI_WIDTH, 0, (space + 1) * TRI_WIDTH, 0, (space + .5) * TRI_WIDTH, TRI_HEIGHT, fill = '#C19A6B')
        for s in range(12):
            #Found .cget() function online at bytes.com
            self._canvas.create_polygon(s * TRI_WIDTH, int(self._canvas.cget('height')), (s + 1) * TRI_WIDTH, int(self._canvas.cget('height')), (s + .5) * TRI_WIDTH, int(self._canvas.cget('height')) - TRI_HEIGHT, fill = '#C19A6B')
        
        self.black = Backgammon_Black()
        self.white = Backgammon_White()
        
        self.rollButton.pack(side = LEFT, anchor = W)
        self.dieLabel.pack(anchor = N)
        self.endButton.pack(anchor = E)
        self.roll_frame.pack()
        self._canvas.pack()
        self.turnLabel.pack()
        
        self._canvas.bind('<Button-1>', self.whiteMove1)
        self._canvas.bind('<Button-3>', self.whiteMove2)
        
        self.render()
        
        
        
    def roll(self):
        self.r = roll()
        self.r.sort()
        rolled = self.r[:]
        rolled = str(rolled)
        rolled = rolled[1:-1]
        rolled = rolled.replace(',', '')
        self.rolls.set(rolled)
        self.rollButton.config(state = DISABLED)
        self.whosTurn.set('Choose a piece to move')
        
    def render(self):
        '''Renders the game board every 50 milliseconds'''
        self._canvas.delete('piece')
        bp = self.black.get_pieces()
        bp_nodups = bp[:]
        bp_nodups = list(set(bp_nodups))
        for piece in bp_nodups:
            idx = [i for i,x in enumerate(bp) if x==piece]
            if piece <= 12:
                for pos in range(len(idx)):
                    self._canvas.create_oval((12 - piece) * TRI_WIDTH, pos * TRI_WIDTH, (13 - piece) * TRI_WIDTH, (pos + 1) * TRI_WIDTH, fill = 'black', tags = 'piece')
            elif piece < 25:
                for pos in range(len(idx)):
                    self._canvas.create_oval((piece - 12) * TRI_WIDTH, int(self._canvas.cget('height')) - ((pos + 1) * TRI_WIDTH), (piece - 13) * TRI_WIDTH, int(self._canvas.cget('height')) - (pos * TRI_WIDTH), fill = 'black', tags = 'piece')
        wp = self.white.get_pieces()
        wp_nodups = wp[:]
        wp_nodups = list(set(wp_nodups))
        for piece in wp_nodups:
            #The following line was taken almost straight from stackoverflow (http://stackoverflow.com/questions/9542738/python-find-in-list)
            idx = [i for i,x in enumerate(wp) if x==piece]
            if piece <= 12:
                for pos in range(len(idx)):
                    self._canvas.create_oval((12 - piece) * TRI_WIDTH, pos * TRI_WIDTH, (13 - piece) * TRI_WIDTH, (pos + 1) * TRI_WIDTH, fill = 'white', tags = 'piece')
            elif piece < 25:
                for pos in range(len(idx)):
                    self._canvas.create_oval((piece - 12) * TRI_WIDTH, int(self._canvas.cget('height')) - ((pos + 1) * TRI_WIDTH), (piece - 13) * TRI_WIDTH, int(self._canvas.cget('height')) - (pos * TRI_WIDTH), fill = 'white', tags = 'piece')
        self._canvas.after(50, self.render)
        
    def whiteMove1(self, event):
        '''checks if the selected piece is valid to move'''
        die = self.rolls.get()
        self.select(event)
        piece = self.selected
        if piece not in self.white.get_pieces():
            self.whosTurn.set("That's an invalid piece to pick")
            self.rollButton.config(state=NORMAL)
            return
        self.whosTurn.set('Choose a position to move it to (right click)')

    def select(self, event):
        '''Selects a piece clicked on'''
        x = event.x
        y = event.y
        x = x // TRI_WIDTH
        y = y // TRI_HEIGHT
        if y == 0:
            self.selected = 12 - x
        elif y == 1:
            self.selected = 0
        else:
            self.selected = 13 + x
            
    def whiteMove2(self, event):
        '''Takes the selected piece and moves it to the destination right-clicked by user'''
        self.goto(event)
        distance = self.destination - self.selected
        if str(distance) not in self.rolls.get() and self.white.get_pieces()[-1] < 6:
            self.whosTurn.set("You can't move your piece there!")
            return
        else:
            try:
                if str(distance) in self.rolls.get() or self.white.get_pieces()[-1] <=6:
                    self.white.move_piece(distance, self.selected, self.black)
            except Exception as e:
                self.whosTurn.set(e)
                return
            r = self.rolls.get()
            if len(r) > 1:
                r = r.split()
                if str(distance) in r:
                    r.remove(str(distance))
                    r = str(r)
                    r = r[1:-1]
                    r = r.replace(',', '')
                    r = r.replace("'", '')
                    self.rolls.set(r)
                elif self.white.get_pieces()[-1] <= 6:
                    r.remove(str(r[random.randint(0,len(r) - 1)]))
                    r = str(r)
                    r = r[1:-1]
                    r = r.replace(',', '')
                    r = r.replace("'", '')
                    self.rolls.set(r)
                
            else:
                if str(distance) in self.rolls.get() or self.white.get_pieces()[-1] <= 6:
                    self.rolls.set('')
            if self.white.win():
                self.rolls.set('')
        if self.white.win():
            self.whosTurn.set('You won! Congratulations!')
        elif self.rolls.get() == '':
            self.black_turn()
        elif self.rolls.get() != '':
            self.whosTurn.set('Choose a piece to move')
        
            
    
    def goto(self, event):
        '''sets destination of piece based on where the user right-clicked'''
        x = event.x
        y = event.y
        x = x // TRI_WIDTH
        y = y // TRI_HEIGHT
        if y == 0:
            self.destination = 12 - x
        elif y == 1:
            self.destination = 0
        else:
            self.destination = 13 + x
    
    def end_turn(self):
        self.rolls.set('')
        self.black_turn()
            
    def black_turn(self):
        '''Chooses random pieces and distances for black pieces to move'''
        #Black's turn using random pieces and moving while there are rolls left and black hasn't won
        black_roll = roll()
        while black_roll != [] and not self.black.win():
            roll_idx = random.randint(0, len(black_roll) - 1)
            roll_to_use = black_roll[roll_idx]
            piece_to_use = 0
            invalid = []
            unable = 0
            while True:
                try:
                    if piece_to_use in invalid:
                        bpcopy = self.black.get_pieces()[:]
                        piece_to_use = bpcopy[random.randint(0,15)]
                    if len(invalid) == 15:
                        break
                    self.black.move_piece(roll_to_use, piece_to_use, self.white)
                    break
                except:
                    invalid.append(piece_to_use)
            black_roll.remove(roll_to_use)
        #If black wins, end game. Else, let player roll
        if self.black.win():
            self.whosTurn.set("I won this time. That's too bad")
        else:
            self.rollButton.config(state=NORMAL)
            self.whosTurn.set('Roll the die')
        
    
        
            
if __name__ == '__main__':
    root = Tk()
    root.title('Backgammon')    
    app = BackgammonGame(root)
    root.mainloop()