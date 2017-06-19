#breakout.py
# Anirudh Maddula (aam252) and Jeffrey Zhang (jz674)
# 12/7/16

# We based a few methods off of Walker White's sample code (wmw2). 
# update() is based off of state.py. The strategy for checkClick() to
# determine when a click occurs is based off of subcontroller.py.

"""Primary module for Breakout application
This module contains the main controller class for the Breakout application.
There is no need for any any need for additional classes in this module.
If you need more classes,99% of the time they belong in either the play module
or the models module. If you are ensure about where a new class should go, post
a question on Piazza.
"""
from constants import *
from game2d import *
from play import *


# PRIMARY RULE: Breakout can only access attributes
    #in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py


class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods
    necessary for processing the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED,
                STATE_ACTIVE]: the current state of the game represented
                a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle,
                ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or
                                                        STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification
    for the method update().
    
    You may have more attributes if you wish (you might need an attribute
    to store any text messages you display on the screen). If you add new
    attributes, they need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
        last_keys contains the number of keys pressed in the previous frame.
                  [int >= 0]
        _check    is True if a key was pressed in the previous frame
                  [must be a boolean]
        lives     the amount of lives the player has at a given time
                  [int from 0 to 3]
        time      the amount of frames passed
                  [mmust be an int >0][60frames/sec]
        _mssg2    [Glabel, message is always displayed]
                  the currently active score message
    """

    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__
        (which you should not override or change). This method is called once
        the game is running. You should use it to initialize any game specific
        attributes.
        
        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE
        and create a message (in attribute _mssg) saying that the user
        should press to play a game."""
        
        scorestr = '0'
        
        self._image = GImage(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=GAME_WIDTH,
                                height=GAME_HEIGHT,source='beach-ball.png')
        
        self._mssg = GLabel(text='Click any button to start',font_size=30,
                            halign='left',valign='top',x=GAME_WIDTH/2,y=500,)
        
        self._mssg2 = GLabel(text="Score:" + scorestr,font_size=30,
                             halign='left',valign='top',left=0,y=600,
                             font_name = 'ComicSansBold')
        
        self._state = STATE_INACTIVE
        self._game = None
        self.last_keys = 0
        self._check = False
        self.time = 0
        self.lives = 3
        
    
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Play.
        The primary purpose of this game is to determine the current
        state, and -- if the game is active -- pass the input to the Play object
        _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWGAME, STATE_COUNTDOWN, STATE_PAUSED,
        and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.
        It displays a simple message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows
        it on the screen. This state only lasts one animation frame before
        switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball
        is served.  The player can move the paddle during the countdown,
        but there is no ball on the screen.  Paddle movement is handled by the
        Play object.Hence the Play class should have a method called
        updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the paddle and the ball moves on its own about the board.
        Both of these
        should be handled by methods inside of class Play (NOT in this class).
        Hence
        the Play class should have methods named updatePaddle() and
        updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state
        so long as the player never presses a key.  In addition, the
        application switches to this state if the previous state was
        STATE_ACTIVE and the game is over (e.g. all balls are lost or
        no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one
        frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent
        3 seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there
        are still some tries remaining.
                
        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.
                
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        ---------------------------------------------------------------------
        Added:
        STATE_WIN: the application switches to this state if all the bricks
        are hit with the ball previously in STATE_ACTIVE. A message is displayed
        congraduating the player

        STATE_COMPLETE: THE application switches to this state once the game is
        complete to signalify the end of the game.
        
        -------------------------------------------------------------------
        Acknowledgement: Walker White (wmw2) - state.py
        """
        
        if self._state == STATE_INACTIVE:
            self.checkClick()
            if self._check == True:
                self._state = STATE_NEWGAME
                self._mssg = None
                self._check = False
        elif self._state == STATE_NEWGAME:
            self._game = Play()
            self._state = STATE_COUNTDOWN
            self._game.updatePaddle(self.input)
        elif self._state == STATE_COUNTDOWN:
            #print 'im in state countdown'
            self.determineNumber()
            self._game.updatePaddle(self.input)
            self.determineScore()
        elif self._state == STATE_ACTIVE:
            self._game.updatePaddle(self.input)
            self._game.updateBall()
            self.determineScore()
            if len(self._game.getBricks()) == 0:
                self._check = False
                self._state = STATE_WIN
            self.bottomBall()
        elif self._state == STATE_PAUSED:
            self.livesMessage()
            self.determineScore
        elif self._state == STATE_WIN:
            self.determineScore()
            self.checkClick()
            self._mssg = GLabel(text='congrats u win noob',font_size=30,
                                halign='left',valign='top',x=225,y=200)
            self._state == STATE_COMPLETE
    
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.
        To draw a GObject g, simply use the method g.draw(self.view).
        It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks)
        are attributes in Play. In order to draw them, you either need to
        add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.
        See the example subcontroller.py from class."""
        
        if self._image is not None:
            self._image.draw(self.view)
        
        if self._mssg is not None:
            self._mssg.draw(self.view)
            
        if self._mssg2 is not None:
            self._mssg2.draw(self.view)
        
        if self._game is not None:
            self._game.draw(self.view)
                    
    def checkClick(self):
        """Returns: True if the user has pressed a key for the first time.
        The user must release the key and press it again to count as a
        new click.
        
        Acknowledgement: Walker White (wmw2) - subcontroller.py
        """
        # Determine the current number of keys pressed
        curr_keys = self.input.key_count
        
        # Only change if we have just pressed the keys this animation frame
        change = curr_keys > 0 and self.last_keys == 0
        
        if change:
            self._check = True
            
        #print str(self._check)
        # Update last_keys
        self.last_keys = curr_keys        
        
    def determineNumber(self):
        """Displays a countdown from 3,2,1 before the game starts and iterates
        to STATE_ACTIVE. Keep in mind 60frames/second"""
        
        self.time = self.time + 1
        if self.time<60:
            self._mssg = GLabel(text='3',font_size=30,halign='left',
                                valign='top',x=225,y=200)
        elif 60<self.time<120:
            self._mssg = GLabel(text='2',font_size=30,halign='left',
                                valign='top',x=225,y=200)
        elif 120<self.time<180:
            self._mssg = GLabel(text='1',font_size=30,halign='left',
                                valign='top',x=225,y=200)
        elif 180<self.time<240:
            self._mssg = None
            self._state = STATE_ACTIVE
            self._game.makeBall()
                
    def bottomBall(self):
        """Determine when the ball hits the ground. And if so, the game will
        iterate to STATE_PAUSED"""
    
        if self._game.getBall().bottom < 5:
            self.lives = self.lives - 1
            #print str(self.lives)
            self._state = STATE_PAUSED

    def livesMessage(self):
        """Displays countdown messages whenever the ball hits the bottom of the
        screen. It then iterates back to STATE_COUNTDOWN if any lives are left.
        Otherwise, it ends the game by going to STATE_COMPLETE and display a
        'Game Over' message. The player will start out with 3 lives. Once the
        player loses a life, he/she will need to press a key to play
        their next life. """
        
        if self.lives == 2:
            self._mssg = GLabel(text='2 lives left! Press to play agian ',
                                font_size=30,halign='left',valign='top',
                                x=225,y=200)
            self.checkClick()
            if self._check == True:    
                self._state = STATE_COUNTDOWN
                self._check = False
                self._game is None
                self.time = 0        
            
        if self.lives == 1:
            self._mssg = GLabel(text='1 life left! Press to play agian',
                                font_size=30,halign='left',valign='top',
                                x=225,y=200)
            self.checkClick()
            if self._check == True:
                self._state = STATE_COUNTDOWN
                self._check = False
                self._game is None
                self.time = 0 
        
        if self.lives == 0:
            self._mssg = GLabel(text='Game Over!',font_size=30,
                                halign='left',valign='top',x=225,y=200)
            self._state = STATE_COMPLETE

    def determineScore(self):
        """Determines the score by subtracting the original amount of bricks
        from the current amount of bricks. Dislplays this with a Glabel."""
        score = self._game.getTotalBricks() - len(self._game.getBricks())
        scorestr = str(score)
        self._mssg2.text = "Score:" + scorestr
            