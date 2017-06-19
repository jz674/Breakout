# play.py
# Anirudh Maddula (aam252) and Jeffrey Zhang (jz674)
# 12/7/16

# We based a methods off of Walker White (wmw2).
# updatePaddle() is adapted from arrows.py

"""Subcontroller module for Breakout


This module contains the subcontroller to manage a single game in the Breakout
App. Instances of Play represent a single game.  If you want to restart a
new game,you are expected to make a new instance of Play.


The subcontroller Play manages the paddle, ball, and bricks.  These are model
objects.  Their classes are defined in models.py.


Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *

# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks.
    It animates the ball, removing any bricks as necessary.
    When the game is won, it stops animating. You should create a NEW instance
    of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that
    you want to access an attribute in class Breakout. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Breakout.
    Only add the getters and setters that you need for Breakout.
    
    You may change any of the attributes above as you see fit. For example, you
    may want to add new objects on the screen (e.g power-ups).  If you make
    changes, please list the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _total [int >= 0]: the number of bricks to start with
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBricks(self):
        """a getter of bricks"""
        return self._bricks
    
    def getBall(self):
        """a getter of ball"""
        return self._ball
    
    def getPaddle(self):
        """a getter of paddle"""
        return self._paddle
    
    def getTotalBricks(self):
        """a getter for total number
        of bricks at the start of the game"""
        return self._total
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """initializer: creat the row of bricks and columns. Also set the
        _total to the amount of bricks."""
        
        self._total = 0
        x = 0
        acc = []
        #i refers to row, j refers to column
        for x in range(0,BRICK_ROWS):
            for y in range(0,BRICKS_IN_ROW):
                new = Brick(x,y)
                acc.append(new)
                self._total +=1
        self._bricks = acc
        self._paddle = Paddle()
        
        self._ball = None
        
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, input):
        """Animates the paddle.
        
        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        
        Acknowledgement: Walker White (wmw2) - arrows.py
        """
        ANIMATION_STEP = 6
        da = 0
        ds = 0
        if input.is_key_down('left'):
            da -= ANIMATION_STEP
        if input.is_key_down('right'):
            da += ANIMATION_STEP
            
        if input.is_key_down('up'):
            ds += ANIMATION_STEP
        if input.is_key_down('down'):
            ds -= ANIMATION_STEP
        
        pos = self._paddle.x + da
        pos2 = self._paddle.y + ds
        
        if pos<PADDLE_WIDTH:
            pos = max(pos, PADDLE_WIDTH/2)
        elif pos>0:
            pos = min(pos, GAME_WIDTH-PADDLE_WIDTH/2)
        
        if pos2<PADDLE_HEIGHT:
            pos2 = max(pos2, PADDLE_HEIGHT/2)
        elif pos2>0:
            pos2 = min(pos2, GAME_HEIGHT-PADDLE_HEIGHT/2)
            
        # Change the x position
        self._paddle.x = pos
        self._paddle.y = pos2
    
    def updateBall(self):
        """Updates the balls velocity and the functions checkBrick(),
        ballBounce() and self.checkPaddle()."""
        self._ball.x = self._ball.x + self._ball.getvx()
        self._ball.y = self._ball.y + self._ball.getvy()     
        
        self.checkBrick()
        self.ballBounce()
        self.checkPaddle()
                
    def makeBall(self):
        """Constructor for the ball"""
        self._ball = Ball(GAME_WIDTH/2,GAME_HEIGHT/2)
        
    def checkBrick(self):
        """Checks if the ball collides with the bricks and if so,
        remove bricks and negate velocity. Also everytime the
        ball a brick, play a sound"""
        bounceSound = Sound('bounce.wav')
        for x in self.getBricks():
            if x.collides(self.getBall()):
                 self.getBricks().remove(x)
                 #self._ball.negvx()
                 self._ball.negvy()
                 bounceSound.play()

    def checkPaddle(self):
        """checks if the ball collides with paddle and if so, negate the
        velocity, and produce a sound"""
        bounceSound2 = Sound('cup1.wav')
        if self.getPaddle().collides(self.getBall()):
            self._ball.negvy()
            bounceSound2.play()
    
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
   
    def draw(self, view):
        """draws the bricks, paddle, and ball"""
        for x in self._bricks:
            x.draw(view)
        self._paddle.draw(view)
        if self._ball is not None:
            self._ball.draw(view)
            
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION    
    def ballBounce(self):
        """determines what happens when the ball bounces on the screen.
        If the ball's mostleft side touches the left side of the screen,
        the ball's x-direction would be negated. The same goes for the right
        side of the screen. If the balls' top or bottom touches the screen,
        the ball's y-direction would be negated."""
        if self._ball.left <= 0 or self._ball.right > GAME_WIDTH:
            self._ball.negvx()
        if self._ball.bottom <= 0 or self._ball.top > GAME_HEIGHT:
            self._ball.negvy()
           
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE