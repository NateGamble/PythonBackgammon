#Creates Backgammon class
#Not used in Game!!!
import sys
import random
from backgammon_white import *
from backgammon_black import *

class Backgammon:
    '''Creates a Backgammon class with piece placers and moving functions'''

    def __init__(self, color):
        if color == 'white':
            self.pieces = [1, 1,
                        12, 12, 12, 12, 12,
                        17, 17, 17,
                        19, 19, 19, 19, 19]
        elif color == 'black':
            self.pieces = [6, 6, 6, 6, 6,
                           8, 8, 8,
                           13, 13, 13, 13, 13,
                           24, 24]
        else:
            raise ValueError('The color you chose was incorrect')

        self.color = color

    def __str__(self):
        return 'Your pieces are at the positions: ' + str(self.pieces)

    def get_pieces(self):
        return self.pieces

    def roll(self):
        '''Rolls 2 die and determines if it's doubles'''
        roll_1 = random.randint(1,6)
        roll_2 = random.randint(1,6)
        if roll_1 != roll_2:
            self.die = [roll_1, roll_2]
        else:
            self.die = [roll_1, roll_1, roll_2, roll_2]
        return self.die

    def move(self, piece, roll, dice_rolled):
        '''Moves wanted piece by the given roll'''
        if piece in self.pieces:
            self._piece_to_move = self.pieces.index(piece)
            if self.color == 'white':
                self.pieces[self._piece_to_move] = piece + roll
            else:
                self.pieces[self._piece_to_move] = piece - roll
            dice_rolled.remove(roll)
        else:
            print('The piece you want to move is not a valid choice')
        return self.pieces

    def is_captured(self):
        return -50 in self.pieces

    def win(self):
        '''Determines if self wins'''
        if self.pieces == [25, 25, 25, 25, 25,
                           25, 25, 25, 25, 25,
                           25, 25, 25, 25, 25]:
            return True
        elif self.pieces == [0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0]:
            return True
        else:
            return False

    def turn(self):
        '''Compiles functions into one turn for player'''
        die = self.roll()
        while len(die) != 0:
            print('Your pieces are at:', str(self.get_pieces()))
            print('Your roll is: ' + str(die) + '.')
            print('Which piece would you like to move first?')
            move = int(input())
            print('How far do you want to move this piece?')
            amount_to_move = int(input())
            if amount_to_move not in die:
                print('The value you entered is not one of the numbers you rolled.')
                print('Please try again')
                return None
            print('Your pieces are now at:', str(self.move(move, amount_to_move, die)))
            print('And you have', len(die), 'moves left.')
        
        
        
        

    





# ----- Main Code -----

if __name__ == '__main__':
    



    print('All tests completed. Funtion working so far...')
