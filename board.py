from button import *

class Character: 
    """Class with attributes letter, row, column"""
    def __init__(self, letter = "", color = "white",button = "na", has_text = False, color_change = True):
        #button is a button object
        self._letter = letter
        self._color = color
        self._button = button #has changeable text
        self._has_text = has_text
        self._color_change = color_change # has changeable color

    def get_color_change(self):
        return self._color_change
    
    def get_has_text(self):
        return self._has_text

    def change_button_color(self,image, color):
        self._button.change_image(image)
        self._color = color
    
    def getButton(self):
        return self._button
    
    def GetLetter(self):
        """returns the letter"""
        return self._letter
    
    def SetLetter(self, letter):
        """sets the letter"""
        self._letter = letter

    def GetColor(self):
        """returns the color"""
        return self._color
    
    def SetColor(self, color):
        """sets the color"""
        self._color = color
    
    # special method for comparing character objects
    def __eq__(self, other): 
        return self._letter.lower() == other._letter.lower() and self._color == other._color
    
    def __str__(self):
        return self._letter

class Board: 
    """Class with attributes size, board and category, wordNum"""
    def __init__(self, board = [], category = "n/a"):
        self._board = board
        self._category = category
    
    def GetBoard(self):
        """returns the board"""
        return self._board
    
    def GetCategory(self):
        """returns the category"""
        return self._category
    
    def SetBoard(self, board):
        """sets the board"""
        self._board = board

    def SetCategory(self, category):
        """sets the category"""
        self._category = category

        
