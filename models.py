# models.py
# Anirudh Maddula (aam252) and Jeffrey Zhang (jz674)
# 12/7/16
"""Models module for Breakout


This module contains the model classes for the Breakout game.
That is anything that you interact with on the screen is model:
the paddle, the ball, and any of the bricks.


Technically, just because something is a model does not mean there has to be
a special class for it.  Unless you need something special, both paddle and
individual bricks could just be instances of GRectangle.  However, we do need
something special: collision detection.  That is why we have custom classes.


You are free to add new models to this module.  You may wish to do this when
you add new features to your game.  If you are unsure about whether to make
a new class or not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module
#constants.py.
# If you need extra information from Play, then it should be a parameter in
#your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as
    move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self):
        GRectangle.__init__(self, bottom = PADDLE_OFFSET, x = GAME_WIDTH/2,
                            fillcolor = colormodel.BLACK, width = PADDLE_WIDTH,
                            height = PADDLE_HEIGHT,
                            linecolor = colormodel.BLACK)        
    
    def collides(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        
        if ball.getvy() > 0:
            return False
        
        if self.contains(ball.x - BALL_DIAMETER/2, ball.y + BALL_DIAMETER/2):
            return True
        elif self.contains(ball.x - BALL_DIAMETER/2, ball.y - BALL_DIAMETER/2):
            return True
        elif self.contains(ball.x + BALL_DIAMETER/2, ball.y - BALL_DIAMETER/2):
            return True
        elif self.contains(ball.x + BALL_DIAMETER/2, ball.y + BALL_DIAMETER/2):
            return True
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.
    You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A BRICK

    #x refers to row, y refers to column
    def __init__(self, x, y):
        """Initializer: creates the bricks and positions them across the top
        of the screen"""
        GRectangle.__init__(self, top = GAME_HEIGHT-BRICK_Y_OFFSET -
                            x*BRICK_HEIGHT - BRICK_SEP_V*x, left = BRICK_SEP_H/2
                            + y*BRICK_WIDTH + BRICK_SEP_H*y,
                            fillcolor = BRICK_COLORS[x%10], width = BRICK_WIDTH,
                            height = BRICK_HEIGHT, linecolor =
                            BRICK_COLORS[x%10])        

    # METHOD TO CHECK FOR COLLISION
    
    def collides(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        if self.contains(ball.x - BALL_DIAMETER/2, ball.y + BALL_DIAMETER/2):
            return True
        elif self.contains(ball.x - BALL_DIAMETER/2, ball.y - BALL_DIAMETER/2):
            return True
        elif self.contains(ball.x + BALL_DIAMETER/2, ball.y - BALL_DIAMETER/2):
            return True
        elif self.contains(ball.x + BALL_DIAMETER/2, ball.y + BALL_DIAMETER/2):
            return True
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for
    velocity. This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for
    these instead of using setters?
    This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getvx(self):
        """A getter for the ball's Velocity in x direction """
        return self._vx
    def getvy(self):
        """A getter for the ball's Velocity in y direction """
        return self._vy
        
    def negvx(self):
        """A setter-like function that negates the ball's Velocity in x
        direction"""
        self._vx = -self._vx
    def negvy(self):
        """A setter-like function that negates the ball's Velocity in y
        direction"""
        self._vy = -self._vy
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self,x,y):
        """initializer: creates starting velocities for the ball and creates
        the GEllipse.
        Parameter x: the starting x coordinate of the position of the ball
        Precondition: x is an int >= 0
        
        Parameter y: the starting y coordinate of the position of the ball
        Precondition: y is an int >= 0"""
        
        
        self._vx = random.uniform(1.0,5.0) 
        self._vx = self._vx * random.choice([-1, 1])
        
        self._vy = -5.0

        GEllipse.__init__(self,x=x,y=y,width=BALL_DIAMETER,
                          height=BALL_DIAMETER,fillcolor=colormodel.RED)
    