"""Authors: Giuseppe Pongelupe Giacoia
Date: 03/17/2024
Summary: This game.py file works with the button.py and board.py files and game level desriptions in "answers.json" and "grid.json" 
to create a game where the user can select colors and letters to fill in a cell in a given grid. 
The goal to win the game is to complete the given built in levels by connecting two given cells of a certain color by a continuous path of cells of the same color, 
the path can be horizontal, vertical, and bent, but each cell only has at most 4 other adjacent cells (up, down, right and left), meaning that the path can't go diagonally. 
Once a path is made with colors, users have to also spell out a word of the given category given the starting letter and end position."""

import pygame
from button import *
from board import *
import sys
import json
import time


class Game: 

    def __init__(self): 
        pygame.init() # initializes pygame

        # Setting up 
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Word-Flow")
                
        # attributes to be used if game is paused / in order to pause the game
        self.game_paused = False
        # loading in images and initializing button objects for the paused menu
        pause_button_image = pygame.image.load("images/Menu/Pause Button Solid.png").convert_alpha()
        self.pause_button = Button(self.screen_width-70, 50, pause_button_image,0.6,self)  
        info_image = pygame.image.load("images/Menu/Info Solid.png").convert_alpha() 
        quit_image = pygame.image.load("images/Menu/Quit Solid.png").convert_alpha()
        new_game_image = pygame.image.load("images/Menu/New Game Solid.png").convert_alpha()
        self.new_game_button = Button(self.screen_width/2,self.screen_height/4, new_game_image,1,self) 
        self.info_button = Button(self.screen_width/2,(self.screen_height/4)*2,info_image,1,self)
        self.quit_button = Button(self.screen_width/2,(self.screen_height/4)*3,quit_image,1,self)

        # attributes and buttons used for the main and info menus 
        self.main_menu = True
        self.info_menu2 = False # second page of the menu
        self.info_menu = False 
        new_game_image = pygame.image.load("images/Menu/New Game Solid.png").convert_alpha() 
        self.main_new_button = Button(self.screen_width/2,self.screen_height/5 *2, new_game_image,1,self)
        self.main_info_button = Button(self.screen_width/2,(self.screen_height/5)*3,info_image,1,self)
        self.main_quit_button = Button(self.screen_width/2,(self.screen_height/5)*4,quit_image,1,self)
        self.title_image = pygame.image.load("images/Menu/Word-Flow Logo.png").convert_alpha()
        exit_image = pygame.image.load("images/Menu/Exit Button.png").convert_alpha() 
        self.exit_button = Button(self.screen_width-70, 50,exit_image, 0.6, self)
        next_image = pygame.image.load("images/Menu/Next Button.png").convert_alpha() 
        self.next_button = Button(1000,700,next_image, 0.6, self)
        back_button = pygame.image.load("images/Menu/Back Button.png").convert_alpha() 
        self.back_button = Button(200,700,back_button, 0.6, self)


        # creating the base font for the "character" objects (AKA each cell) 
        self.base_font = pygame.font.Font(None, 32)

        # load in level information and answers
        self.current_level = 0 
        self.levels = []
        json_file = "grid.json"
        self.load_levels(json_file,self.levels) # levels are stored in Board objects and all in a linear list 

        # loading answers from a local json file. 
        self.answers = []
        json_answer = "answers.json"
        self.load_levels(json_answer,self.answers) # answers are 2d lists stored in corresponding indexes in self.answers to self.levels

        # self.characters represents the current level being played 
        self.characters = self.levels[self.current_level].GetBoard()

        # Initializing buttons for color selection 
        self.colors = ["Dark Blue", "Green", "Light Blue", "Medium Blue", "Orange", "Pink", "Red", "Yellow", "Default"] # list of all the colors available
        self.color_buttons = [] 
        self.colors_index = [False, False, False, False, False, False, False, False, False] #status of each button (if a specific color of a corresponding index is currently selected)
        for color in range(len(self.colors)):
            image = pygame.image.load("Images/buttons/"+self.colors[color]+" Button.png").convert_alpha()
            button  = Button(100,80+(color*80),image,0.2,self)
            self.color_buttons.append(button)

        # initializes "check" button that players will use in order to check if their work is correct
        self.check = False
        check_image = pygame.image.load("images/Menu/Check Solid.png").convert_alpha()
        self.check_button =  Button(1000,680, check_image, 0.625, self)


        # used to see if user did all levels
        self.last_level = len(self.levels)



        

    def load_levels(self, json_file,lst):
        """Loads the levels from a json file and creates characters and buttons to represent a grid appropriately. 
        It then stores them in a board object and appends it to the self.levels list.
        Alternatively if lst is self.answers then it stores the answers for a given level in 
        the list"""
        with open(json_file, "r") as file: 
            data = json.load(file)
        i = 0 # i and j are used to know the spacing between cells in a grid
        j = 0

        # below are calculations to find where the center of the grid should be
        grid_cell_width = 212* 0.4
        grid_cell_height = 215* 0.4
        grid_padding = 2 #space between cells
        grid_size = len(data[0])
        grid_width = grid_size * grid_cell_width + (grid_size + 1) * grid_padding 
        grid_height = grid_size * grid_cell_height + (grid_size + 1) * grid_padding

        # Calculate the position to center the grid
        grid_y = ((self.screen_width - grid_width) // 2) * 1.3
        grid_x = ((self.screen_height - grid_height) // 2) - 20

        for grid in data:  #iterating per "level"
            character_grid = []
            i=0
            for row in grid: # iterating per column (as per the structure of the json file)
                character_row = []
                j=0
                for item in row: #iterating per object in a given column 
                    character_image = pygame.image.load("images/"+item['color']+" Key.png").convert_alpha() # starts a cell in the given color
                    image_y = (grid_x + (j * (grid_cell_width + grid_padding)) + grid_padding ) - 135
                    image_x = (grid_y + (i * (grid_cell_height + grid_padding)) + grid_padding) -40 # location of the button in the grid
                    character_button = Button(image_x,image_y,character_image,0.4,self)
                    character = Character(item['letter'], item['color'], character_button, item['has_text'], item['color_change'])
                    character_row.append(character)
                    j+=1
                character_grid.append(character_row)
                i+=1
            temp = Board(character_grid) # creates one board object per level
            lst.append(temp) 

    def run_game(self):
        """Main loop for the game. it will keep running until the game is done
        There are 5 main types of events, game is being paused (pulls up paused menu), 
        game just started or newgame button was clicked, checking answers with check button, 
         main event for game  being played, and Info screen shown. """
        
        while True:
            self.screen.fill(self.bg_color) # fill in background
            self._check_events() #checks for special keyboard events

            if self.current_level == self.last_level: # if player won the game
                print("Hi")
                font = pygame.font.Font("slkscr.ttf", 50)
                text_surface = font.render("You won!", True, (0,0,0))
                self.screen.blit(text_surface, ((self.screen_width-150)/2 - 100,(self.screen_height-50)/2))
                pygame.display.flip()
                break
            elif self.info_menu2: # if the second page of the menu should be up
                self._info_menu2()
            elif self.info_menu: #if the info menu should be up
                self._info_menu()
            elif self.main_menu: # if main menu should be pulled up
                self._main_menu()
            elif self.game_paused: # if the paused menu should be pulled up
                self._paused()
            elif self.check:  # if the player requested to check his answers
                if self.check_answers(): # answer is right, moving on to next level
                    self.current_level +=1
                    self.characters = self.levels[self.current_level].GetBoard()
                    self.screen.fill(self.bg_color)     
                    font = pygame.font.Font("slkscr.ttf", 50)
                    text_surface = font.render(f"Moving on to Level {self.current_level+1}", True, (0,0,0)) # dislpay intermediate message 
                    width, height = text_surface.get_rect().size
                    self.screen.blit(text_surface, (((self.screen_width-width)/2),(self.screen_height/2)-40))
                    pygame.display.flip() 
                    time.sleep(1.5)
                self.check = False 
            else: # main event, where game is running a level
                for row in range(len(self.characters)): # draw the characters/cells on the screen
                    for character in range(len(self.characters[row])):
                        self.character_update(row,character)
                        self.draw_character_text(self.characters[row][character])
                if self.check_button.draw(): # checks if player pressed paused or check buttons
                    self.check = True
                if self.pause_button.draw():
                    self.game_paused = True

                for button_index in range(len(self.color_buttons)): # draws color buttons
                    if self.color_buttons[button_index].draw(): # checks which button was last pressed
                        self.colors_index = [False, False, False, False, False, False, False, False, False]
                        self.colors_index[button_index] = not self.colors_index[button_index]

            pygame.display.flip() # flip the image to show updates

    def _info_menu(self):
        """Displays the info menu of the game which has two pages, 
        each accessed with the next and back bottom in the bottom of the page
        the info button is exited once the exit button is clicked"""
        if self.exit_button.draw(): 
            self.info_menu = False
        elif self.next_button.draw():
            self.info_menu2 = True  


    def _info_menu2(self):
        """Shows second page in the info menu"""
        self.screen.fill((255,0,0))
        if self.back_button.draw(): 
            self.info_menu2 = False
        elif self.exit_button.draw(): 
            self.info_menu = False
            self.info_menu2 = False
    
    def _main_menu(self): 
        """Displays the main starting menu of the game, with options to pull up instructions
        start a new game or quit"""
        image_width, image_height = self.title_image.get_rect().size 
        self.screen.blit(self.title_image, ((self.screen_width-image_width)/2, (self.screen_height-image_height)/14)) # draw logo on the screen
        if self.main_new_button.draw():  # check if new game button was selected
            self.main_menu = False
            self.current_level = 0 # reset the game to level 0
            self.characters = self.levels[self.current_level].GetBoard()
        elif self.main_info_button.draw():  # check if info button was selected to pull up the info page
            self.info_menu = True
        elif self.main_quit_button.draw():  #check if quit button was selected 
            sys.exit()
        time.sleep(0.05) # stops temporarily to avoid collision problems
        

    def check_answers(self): 
        """Checks to see if answers are correct, if they are returns true, if not 
        returns false and changes the color back to default and resets the character letter
        returns True if the answer is correct"""
        x = True
        for i in range(len(self.characters)):
            for j in range(len(self.characters[i])):
                if self.characters[i][j] != self.answers[self.current_level].GetBoard()[i][j]:
                    x = False
                    self.characters[i][j].SetLetter(" ")
                    if self.characters[i][j].get_color_change(): # checks if the mistaken cell is an end cell
                        new_image = pygame.image.load("Images/Default Key.png").convert_alpha() 
                        self.characters[i][j].change_button_color(new_image, "Default") # updates the buttons color
        return x
    

    def character_update(self,i, j):
        """update the character object on the screen
        drawing its button and checking if it is being clicked, 
        and if so changing the color appropriately
        
        once selected places the user in "writing mode" where they can enter
        text input for a given cell/character"""

        if self.characters[i][j].get_button().draw(): # drawing button and seeing if it is selected
            if self.characters[i][j].get_color_change(): # Checks if the character can have its color changed
                for color in range(len(self.colors_index)): 
                    if self.colors_index[color]: 
                        self.characters[i][j].SetColor(self.colors_index[color]) # changes the color attribute once cell changes color
                        new_image = pygame.image.load("Images/"+self.colors[color]+" Key.png").convert_alpha() 
                        self.characters[i][j].change_button_color(new_image, self.colors[color]) # updates the buttons color with a new image
            
            # checks if the button pressed has a modifiable character (isn't a given start or end, and isn't one of the color select buttons)
            if self.characters[i][j].get_has_text(): 
                text = self.characters[i][j].get_letter()
                running = True
                while running: # player stuck in writting mode until he enters "enter" to select new character or selects a cell
                    self.screen.fill(self.bg_color)
                    # redraw up the grid so it doesn't get covered
                    for row in self.characters: 
                        for chars in row:
                            if chars.get_button().draw():
                                running = False # if user selects other cell it kicks out and saves current work
                            self.draw_character_text(chars)
                
                    # draw up the color buttons as well so they dont get covered also kicks player out of writting mode if selected
                    for button_index in range(len(self.color_buttons)): 
                        if self.color_buttons[button_index].draw():
                            running = False 
                        
                    for event in pygame.event.get(): #get user input text 
                        if event.type == pygame.QUIT:
                            sys.exit()
                        # handle text input
                        if event.type == pygame.TEXTINPUT:
                            text = event.text
                        # handle special keys
                        if event.type == pygame.KEYDOWN: 
                            if event.key == pygame.K_RETURN:
                                print(text)  # Print the input text
                                running = False
                            elif event.key == pygame.K_BACKSPACE:
                                text = ""
                    self.characters[i][j].SetLetter(text) # updates the character for the given cell
                    pygame.display.flip()


    def draw_character_text(self, character):
        """Given a character it draws on the screen its text attribute over its image"""
        text_surface = self.base_font.render(character.get_letter(), True, (0,0,0))
        self.screen.blit(text_surface, (character.get_button().rect.x + 35, character.get_button().rect.y +32))


    def _paused(self):
        """Draw the pause screen menu and give 3 different options to the user
        to continue, quit, or start a new game"""
        self.screen.fill(self.bg_color)
        if self.info_button.draw():
            time.sleep(0.1) # stops program temporarily to avoid problems with colission points 
            self.info_menu = True
            self.game_paused = False
        if self.quit_button.draw():
            sys.exit()
        if self.new_game_button.draw():  # pulls up the main menu again for players to restart the game
            self.game_paused = False
            self.main_menu = True
        if self.exit_button.draw(): 
            self.game_paused = False


    def _check_keydown_events(self, event):
        """Checks if user pressed special key m which pulls up the paused menu"""
        if event.key == pygame.K_m:
            if self.game_paused:
                self.game_paused = False
            else:
                self.game_paused = True
        
    def _check_events(self):
        """Checks for special events such as closing the tab and keydown events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Did the player press the right or left arrow key?
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # Did the player stop holding down the arrow key?



x = Game() # Creates a game instance
x.run_game() # Start the game

