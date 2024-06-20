# 2023 Spring CSC1002 HW Snake Game

# Overview

The game is composed of 3 objects: a **snake**, a **monster** and some **food** items represented by a set of numbers between 1 and 9.  

The snake is represented by a sequence of squares where its head and its tail are displayed in red and black colors respectively, while the monster by a purple square.  
The numbers are food items to be consumed by the snake. 
![](https://raw.githubusercontent.com/Misaka999/MarkdownPhotos/main/ui.png)


The goal of the game is to maneuver the snake within the game area in four directions (up, down, left and right), trying to consume all the food items while avoiding head-on collision with the monster.  
As each food item is consumed, the tail of the snake lengthens in size equal to the value of the number crossed.  
Furthermore, the monster is also programmed to be motioned in the direction towards the head of the snake at a variable speed. 



# Implementation Details

1. The snake game is designed using the standard module ``turtle``, including the following components:
  - Game Area (status and motion area)
   - A Snake 
   - A Monster 
   - Food Items 
   - Game Status 
   - Controls  
   - Motion
   
  2. Game Area 
  - The game area is composed of an upper area for statuses and a motion area where the snake and monster are moved around, surrounded by a fixed margin along the four sides, with the following dimensions: 
    - Upper status area = 500 (w) x 80 (h) 
    - Lower motion area = 500 (w) x 500 (w)   
    - Margins = around 40 pixels 
  - A border for both the status area and motion area. 
    >Note: the dimension of the motion area is chosen in multiple of standard turtle shape (default 20 pixels) 


3. Food Items 
- Display 5 food items from 1 to 5 within the motion area in random locations.  These numbers will be kept visible all time until they are consumed by the snake.  When the head of the snake crosses one of these numbers, the number being crossed is considered consumed and it will be removed from the game area permanently.  So, any one food item can be consumed once. 
- During the game, randomly hide and unhide any unconsumed food items.  Use appropriate random timer rate, say few seconds between 5 and 10, then randomly pick one of the unconsumed items (including hidden), if the chosen item is visible, hide it, or unhide it otherwise. 
- Hidden food items cannot be consumed by the snake. 
- Use appropriate font size to show the food items. 
- Align food items to match to the center position of the snake.
4. Font Size 
- For displaying text on the canvas, use appropriate font size such as: 
  - Arial, 16, bold or normal 
5. Snake 
  -  The snake is composed of a head with a tail which extends as the snake consumes any food items.  
  -  Use only simple, built-in shape “square” for both head and tail, and default size. 
  -  Use different colors for the head (ex: red) and the tail (ex: black with blue outline color); choose outline color for the tail so that the length of the tail can be counted easily. 
  - The tail extends as the snake moves, not at the point when the food item being consumed; in other words, at the moment the snake crosses a food item, the snake doesn’t change in size; as the snake moves the tail extends in the direction of the movement as if the end of the tail sticks onto the screen. The tail extension ends when the length of the snake has grown in size equal to the value of the number being crossed. The following figure shows the sequence of moves of the snake crossing a food item. 
  - As the tail is being extended, the movement of the snake will slow down.  See “Timer” below. 
  - At the start of the game, the length of the tail is set to 5.  One square shape counts as one unit length, so the tail will be composed of 5 square shapes when fully extended.
6. Monster 
- A fixed size object to be programmed to move towards the snake, trying to make a head-on collision. 
- On startup, place the monster on a random position with a fair distance from the snake.  
- The monster should move at a random rate, a rate that is slightly faster or slower than that of the snake.  See “Timer” below. 
- Use only simple, built-in shape “square” for the monster, default size.  
- Use a different color such as purple. 
- Set the initial position of the monster such that the shape of the monster will partially overlap the shape of the snake when contacted. 
7. Game Status 
- Show the motion of the snake (Left, Right, Up, Down, Paused), in other words, the last motion key pressed (including the space bar), regardless of whether the snake is in motion or being blocked. 
- Show the total count of body contact of the snake with the monster.  The count should be based on the motion of the monster timer.  Each time the monster is re-positioned, it should then check if it overlaps with any part of the snake. 
- Keep track of the total elapsed game time in seconds.  The time counter starts as soon as the game starts and will stop only when game is over.  In other words, the counter will not be stopped when the snake is being paused.   

8. Motion via Timer 
- `Timer` controls the frequency that a specific event to take place at a regular interval, in this case the event is the movement of either the snake or the monster. 
- Use **separate** timers to manually refresh the movement of both snake and the monster
  - Turn off the built-in automatic screen refresh 
- Set an appropriate timer rate, say no faster than 0.2 second. 
- On each timer event, always advance the snake or the monster in a distance equivalent to the length of the turtle shape (square).  If the square’s dimension is 20x20 (pixels), then your logic should advance the turtle object 20 pixels at a time. 
- Both snake and monster move in four directions, left, right, up or down, NOT diagonally.
- Design the timers in such a way: 
  - i. the monster should move in a random time range slightly above or lower than that of the snake, while snake always move at a fixed rate. 
  - ii. when the snake crosses a food item (a number) slow down its movement by increasing its timer rate until its tail is fully extended, that is, the snake will motion slower while the tail being extended  
  - iii. furthermore, you don’t want the snake to move too fast that the monster will never catch up with the snake, or vice versa.  That is, you don’t want the monster moves so quickly that it always catch the snake before it has a chance to consume all the food items. 
 9. Controls 
 - Use the four `arrow keys` (Up, Down, Left, Right) to maneuver the snake in Up, Down, Left and Right motion respectively. 
 - The motion will continue in the direction of the last arrow key pressed.  For an example, If Left key is pressed, the snake will continuously move in the left direction until a different arrow key is pressed. 
 - Use `Space Bar` to toggle (pause and un-pause) snake motion
  (note: monster never pause).  While in motion, pressing the spacebar will pause the snake (not the monster).  While paused, pressing the `space bar` the snake will resume motion in the direction of the last arrow key pressed.  Furthermore, while paused, pressing any of the four arrow keys will un-pause the snake motion and move in the direction of the arrow key being pressed.   
 - Both snake and monster cannot move beyond the motion area; when the head of the snake is moved against any of the 4 sides, the snake will be stopped and it will remain blocked until its heading is changed away from the edges including its tail. 
 - Snake **CANNOT** cross itself, left to right, up to down or vice versa. 
 - Timer for the game will never be paused. 
10. Game Termination
 The game ends when the snake consumes all the food items and its body is fully extended, in this case “Winner” or the monster caught the snake, in this case “Game Over”. 

![](https://raw.githubusercontent.com/Misaka999/MarkdownPhotos/main/fail.png)

 ![](https://raw.githubusercontent.com/Misaka999/MarkdownPhotos/main/win.png)

 
11. Game Startup  
-  On startup, show (1) a brief reminder on how the game starts, (2) the snake (in red) positioned at center and (3) the monster (purple) at a random position far enough from the snake. 
- User mouse-click anywhere on the screen to start the game, all the food items will be shown subsequently, user then moves the snake around using the 4 arrow keys.
