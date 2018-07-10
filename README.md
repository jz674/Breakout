# Breakout
Created the breakout game from scratch and practied with reading official class documentations and APIs as well as using stateful controllers to handle complex, interactive applications. While completing this opened-ended program with little specification, I experienced with designing helper functions to structure my code properly and with using constants to make my code more readable. 

In addition to creating the famous arcade game, I also added multiple extensions:

I included sound to the ball bounces. Whenever it collides with a paddle it plays the 'cup1.wav' file, and the 'bounce.wav' file for a brick collision.

I also added the background picture 'beach-ball.png', which is at the beginning of start (in breakout.py), and drawn first in the draw method.

I also included more functionality to the paddle by making it possible to move up and down. To do this, in updatePaddle() in play.py, I checked 'is_key_down' for the up and down buttons similar to how we called left and right. I also added boundaries so it doesn't go off the screen.

I added a score board at the top left of the screen using a GLabel object. Also, used another attribute (_mssg2) that gets created in start() and drawn in draw(). I also created a new attribute _total in play.py, which starts as an accumlator that gets incremented every time a brick is created. This turns into the total number of bricks. 
I called on the _total in breakout.py with a getter from play, and subtracted the total inital bricks from the current bricks. This changed the text attribute of the GLabel. Every frame, the score will update. I have written all this in a helper function in breakout.py called determineScore(). 

