import turtle
import random
from functools import partial

"""Global variables."""
g_screen = None
g_snake = None   # Turtle represents the head of the snake.
g_monster = None   # Turtle represents the monster.
g_snake_sz = 5    # The length of the snake tail (does not include the head).
g_intro = None
g_keypressed = None   # What keyboard the user pressed at the moment.
g_status = None
g_status_motion = None
g_status_timer = None
g_status_contact = None
g_extend = 0    # The index of the last-eaten food.
g_foods = [[1, None], [2, None], [3, None], [4, None], [5, None]]
g_hiddenFood = []    # Record the hidden food at the moment.
g_snakePositions = [(0, 0)]  # Record all the positions of the snake body and head at the moment.
g_motions = []    # Record the motions.
g_keyboard_num = 0   # Count how many times the user has pressed the keyboard.
g_timeup = 0   # Timer, will add 1 every 1 sec.
g_contact = 0   # Count how many times monster have contact with snake's tail (not include the snake's head).
g_curr_motion = ''
g_s_tRate = 250    # The timer rate for the snake.
g_eatFoods = []    # Record the value of each food consumed by the snake.

# Color of different creatures.
COLOR_BODY = ("blue", "black")
COLOR_HEAD = "red"
COLOR_MONSTER = "purple"

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = "Up", "Down", "Left", "Right", "space"
HEADING_BY_KEY = {KEY_UP: 90, KEY_DOWN: 270, KEY_LEFT: 180, KEY_RIGHT: 0}


def configScreen():
    """Set up the screen and the title. Turn off auto screen refresh."""
    s = turtle.Screen()
    s.tracer(0)    # Disable auto screen refresh, 0=disable, 1=enable.
    s.title("Snake by Misaka")
    s.setup(500+80, 500+80+80)
    s.mode("standard")
    return s


def createTurtle(x, y, color="red", border="black"):
    """
    Create hidden turtle with shape "square".
    Parameters: x,y: where the turtle will be located.
                color,border: the filling and border color for the turtle.
    """
    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x, y)
    return t


def configurePlayArea():
    """
    Create the motion border and status border. Display brief introduction on how to start the game.
    Create motion, timer, contact status which record the motion of the snake, total time and contact times separately.
    """
    # motion border
    m = createTurtle(0, 0, "", "black")
    m.shapesize(25, 25, 5)
    m.goto(0, -40)  # Shift down half the status.

    # status border 
    s = createTurtle(0, 0, "", "black")
    s.shapesize(4, 25, 5)
    s.goto(0, 250)  # Shift up half the motion.

    # introduction
    intro = createTurtle(-200, 60)
    intro.hideturtle()
    intro.write("Snake by Misaka\
                \n\nUse the 4 arrow keys to move the snake. \
                \nEat all the food before the monster catches you!!\
                \nClick anywhere to start. \
                \nHave fun!", font=("Arial", 15, "normal"))
    
    # statuses
    status_motion = createTurtle(60, s.ycor(), "", "black")
    status_motion.hideturtle()
    status_timer = createTurtle(-50, s.ycor(), "", "black")
    status_timer.hideturtle()
    status_contact = createTurtle(-200, s.ycor(), "", "black")
    status_contact.hideturtle()
    return intro, status_motion, status_timer, status_contact


def updateMotion():
    """
    Update the motion status every time the snake changes its motion, if the movement is valid.
    It will repeat every 0.01 sec.
    """
    if (not success()) and (not gameOver()):
        if (not crushWall()) and (not crushSelf()):   # Judge if the movement is valid.
            g_status_motion.clear()
            g_status_motion.write('Motion: '+g_curr_motion, font=('arial', 15, 'bold'))
            g_screen.update()
            g_screen.ontimer(updateMotion, 10)
        else:
            g_screen.update()
            g_screen.ontimer(updateMotion, 10)


def updateTimer():
    """
    Update the timer status every 1 sec.
    Called in onTimer().
    """
    g_status_timer.clear()
    g_status_timer.write('Time: '+str(g_timeup), font=('arial', 15, 'bold'))
    g_screen.update()


def updateContact():
    """
    Update the contact status every time the snake changes its motion, if the movement is valid.
    Called in bodyContact().
    """
    g_status_contact.clear()
    g_status_contact.write('Contact: ' + str(g_contact), font=('arial', 15, 'bold'))
    g_screen.update()


def onArrowKeyPressed(key):
    """Record the pressed keyboard by the user."""
    global g_keypressed
    global g_curr_motion
    global g_motions
    global g_keyboard_num
    g_keypressed = key
    g_motions.append(g_keypressed)
    g_keyboard_num += 1
    if g_keypressed in HEADING_BY_KEY.keys():
        g_curr_motion = g_keypressed
        g_snake.setheading(HEADING_BY_KEY[key])
    elif g_keypressed == KEY_SPACE:
        g_curr_motion = 'Pause'


def onTimerSnake():
    """
    Ontimer function for the snake. If the user press space bar, the snake stop.
    After this, if the user press space bar again, the snake moves in the direction as the last arrow-keyboard pressed;
    or if the user press "up" or "down" or "left" or "right", the snake will move in the corresponding direction.
    Only move when the movement is valid. Repeat every 0.2 sec.
    When the snake is eating food, it slows down, with the time rate increases.
    """
    global g_curr_motion
    global g_motions
    global g_keyboard_num
    global g_keypressed
    global g_s_tRate
    global g_eatFoods
    global g_extend

    if g_keypressed == None:
        g_screen.ontimer(onTimerSnake, g_s_tRate)
        return
    elif g_keypressed == 'space':
        if g_keyboard_num >= 2:
            if g_motions[g_keyboard_num-2] != 'space':
                g_screen.ontimer(onTimerSnake, g_s_tRate)
                return
            else:
                # Snake moves in the direction as the last arrow-keyboard pressed.
                g_motions.pop()
                g_motions.pop()
                g_keyboard_num -= 2
                if g_keyboard_num >= 1:
                    g_curr_motion = g_motions[g_keyboard_num-1]
                    g_keypressed = g_motions[g_keyboard_num-1]
                else:
                    g_screen.ontimer(onTimerSnake, g_s_tRate)
                    return
        else:
            g_screen.ontimer(onTimerSnake, g_s_tRate)
            return

    if (not success()) and (not gameOver()):
        lengthenBody()
        g_extend += eatFood()
        # Slow down the snake when it is extending, by increasing its timer rate.
        if len(g_snake.stampItems) < 5:
            g_s_tRate = 350
        else:
            if g_extend > 0:
                g_s_tRate = 350
                g_extend -= 1
            else:
                g_s_tRate = 250
        g_screen.update()
        g_screen.ontimer(onTimerSnake, g_s_tRate)


def onTimerMonster():
    """
    Ontimer function for the monster.
    The monster keep tracking the snake's head at a random timer rate slightly above or below that of the snake.
    It will not move diagonally. Only move when the movement is valid.
    Calls bodyContact and check whether the monster contact with the snake's body every time the monster moves.
    """
    angle = g_monster.towards(g_snake)
    directions = {0: 0, 1: 90, 2: 90, 3: 180, 4: 180, 5: 270, 6: 270, 7: 0}
    m_speed = random.randint(210, 340)   # Set random timer rate around that of the snake.

    if (directions[angle//45] == 0) and (g_monster.xcor() > 220):
        g_screen.update()
        g_screen.ontimer(onTimerMonster, m_speed)
        return
    if (directions[angle // 45] == 90) and (g_monster.ycor() > 180):
        g_screen.update()
        g_screen.ontimer(onTimerMonster, m_speed)
        return
    if (directions[angle // 45] == 180) and (g_monster.xcor() < -220):
        g_screen.update()
        g_screen.ontimer(onTimerMonster, m_speed)
        return
    if (directions[angle // 45] == 270) and (g_monster.ycor() < -260):
        g_screen.update()
        g_screen.ontimer(onTimerMonster, m_speed)
        return
    g_monster.setheading(directions[angle//45])

    if (not success()) and (not gameOver()):
        g_monster.forward(20)
        if not gameOver():
            bodyContact()
        g_screen.update()
        g_screen.ontimer(onTimerMonster, m_speed)


def onTimer():
    """Ontimer function for the timer. Record the total game time. Repeat every 1 sec."""
    global g_timeup
    g_timeup += 1
    if (not success()) and (not gameOver()):
        g_screen.update()
        g_screen.ontimer(onTimer, 1000)
        updateTimer()


def crushWall():
    """
    Judge whether the snake crushes wall or not.
    If the snake already crushed the wall, press another arrow-keyboard will make the snake moving again,\
    in the direction of the new direction.
    """
    flag = False
    if (g_snake.xcor() >= 230) and (g_keypressed == 'Right'):
        flag = True
    if (g_snake.xcor() <= -230) and (g_keypressed == 'Left'):
        flag = True
    if (g_snake.ycor() >= 190) and (g_keypressed == 'Up'):
        flag = True
    if (g_snake.ycor() <= -270) and (g_keypressed == 'Down'):
        flag = True
    return flag


def crushSelf():
    """
    Judge whether the snake crosses itself or not.
    If the snake already crossed itself, press another arrow-keyboard will make the snake moving again,\
    in the direction of the new direction.
    """
    global g_snakePositions
    flag = False
    x, y = int(g_snake.xcor()), int(g_snake.ycor())
    for i in g_snakePositions:
        if g_keypressed == 'Right':
            if (abs((x + 20)-i[0]) <= 2) and (abs(y-i[1]) <= 2):
                flag = True
        elif g_keypressed == 'Left':
            if (abs((x - 20) - i[0]) <= 2) and (abs(y - i[1]) <= 2):
                flag = True
        elif g_keypressed == 'Up':
            if (abs(x - i[0]) <= 2) and (abs((y + 20) - i[1]) <= 2):
                flag = True
        elif g_keypressed == 'Down':
            if (abs(x - i[0]) <= 2) and (abs((y - 20) - i[1]) <= 2):
                flag = True
    return flag


def lengthenBody():
    """Lengthen the body of the snake. Update the positions taken by the snake."""
    global g_snakePositions
    if (not crushWall()) and (not crushSelf()):
        # Clone the head as body.
        g_snake.color(*COLOR_BODY)
        g_snake.stamp()  # Shifting or extending the tail.
        g_snake.color(COLOR_HEAD)
        g_snake.forward(20)  # Advance snake the same length as the length of turtle shape.
        x, y = int(g_snake.xcor()), int(g_snake.ycor())
        g_snakePositions.append((x, y))
        if len(g_snakePositions) > g_snake_sz + 1:
            del g_snakePositions[0]   # Remove the position when the snake is not on it.
        if len(g_snake.stampItems) > g_snake_sz:
            g_snake.clearstamps(1)   # Remove the last square on Shifting.


def putFood():
    """
    Randomly put 5 food within the motion area (without overlapping).
    Call hideFood().
    """
    global g_foods
    foodsPos = []
    n = 0
    while n <= 4:
        food_x = random.randrange(-243, 232, 20)
        food_y = random.randrange(-270, 180, 20)
        if (food_x, food_y) in foodsPos:   # Check if overlaps.
            continue
        g_foods[n][1] = createTurtle(food_x, food_y)
        g_foods[n][1].hideturtle()
        foodsPos.append((food_x, food_y))
        g_foods[n][1].write(str(n+1), font=("Arial", 15, "normal"))
        n += 1
    sec = random.randint(5, 10)
    g_screen.ontimer(hideFood, 1000*sec)


def hideFood():
    """
    Randomly pick one unconsumed food, if it is unhidden, hide it, or unhidden it.
    Repeat evey few random seconds between 5 sec and 10 sec.
    """
    global g_hiddenFood
    if success() or gameOver():
        pass
    if len(g_foods) != 0:
        curr_food = random.choice(g_foods)    # Randomly choose one unconsumed food.
        # Unhide food which is hidden.
        if curr_food in g_hiddenFood:
            g_hiddenFood.remove(curr_food)
            foodID = curr_food[0]
            curr_food[1].write(foodID, font=("Arial", 15, "normal"))
        # Hide food which is unhidden.
        else:
            g_hiddenFood.append(curr_food)
            curr_food[1].clear()
        g_screen.update()
        sec = random.randint(5, 10)
        g_screen.ontimer(hideFood, 1000*sec)


def eatFood():
    """
    Judge whether the snake eats food.
    If yes, delete the food item from the food list and clear the displayed number of it.
    """
    global g_snake_sz
    for food in g_foods:
        if food not in g_hiddenFood:
            if (6 <= g_snake.ycor()-food[1].ycor() <= 12) and (0 <= g_snake.xcor() - food[1].xcor() <= 6):
                food[1].clear()
                g_foods.remove(food)
                g_eatFoods.append(food[0])
                g_snake_sz += food[0]    # Lengthen the size of the snake.
                return food[0]
    return 0


def bodyContact():
    """
    Check if the monster has contacted the snake's body every time the monster moves.
    If the monster contact the snake's head, game over and this contact will not be count.
    """
    global g_contact
    x_m, y_m = g_monster.xcor(), g_monster.ycor()
    for i in g_snakePositions[0:len(g_snakePositions)-1]:
        # Each time the monster moves, it will only touch the snake once.
        if (abs(x_m-i[0]) <= 13) and (abs(y_m-i[1]) <= 13):
            g_contact += 1
            updateContact()
            break


def success():
    """
    Judge if the user win.
    If the snake has eaten all 5  food, game ends and user wins, returns True. Or returns False.
    """
    if (len(g_foods) == 0) and (len(g_snake.stampItems) == 20):
        if g_snake.xcor() > 200:
            g_snake.write('Winner!',  align='right', font=('arial', 15, 'normal'))
        elif g_monster.xcor() < -200:
            g_snake.write('Winner!', font=('arial', 15, 'normal'))
        else:
            g_snake.write('Winner!', align='center', font=('arial', 15, 'normal'))
        return True
    else:
        return False


def gameOver():
    """
    Judge if the user lose.
    If the snake was caught up by the monster, game ends and user loses, returns True. Or returns False.
    Only head-on collision is regarded as being caught up.
    """
    if g_snake.distance(g_monster) <= 16:
        if g_monster.xcor() > 200:
            g_monster.write('Game Over!',  align='right', font=('arial', 15, 'normal'))
        elif g_monster.xcor() < -200:
            g_monster.write('Game Over!', font=('arial', 15, 'normal'))
        else:
            g_monster.write('Game Over!', align='center', font=('arial', 15, 'normal'))
        return True
    else:
        return False


def startGame(x,y):
    """Start the game if the user click on the screen."""
    g_screen.onscreenclick(None)
    g_intro.clear()
    g_status_contact.clear()
    g_status_motion.clear()
    g_status_timer.clear()
    g_status_motion.write('Motion: ', font=('arial', 15, 'bold'))
    g_status_timer.write('Time: '+str(g_timeup), font=('arial', 15, 'bold'))
    g_status_contact.write('Contact: ' + '0', font=('arial', 15, 'bold'))

    # Bind the keyboard pressed by the user to the function onArrowKeyPressed.
    g_screen.onkey(partial(onArrowKeyPressed, KEY_UP), KEY_UP)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_DOWN), KEY_DOWN)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_LEFT), KEY_LEFT)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_RIGHT), KEY_RIGHT)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_SPACE), KEY_SPACE)

    putFood()

    g_screen.ontimer(onTimerSnake, 100)
    g_screen.ontimer(onTimerMonster, 1000)
    g_screen.ontimer(onTimer, 1000)
    g_screen.ontimer(updateMotion, 100)


if __name__ == "__main__":
    g_screen = configScreen()
    g_intro, g_status_motion, g_status_timer, g_status_contact = configurePlayArea()

    updateTimer()
    updateContact()
    g_status_motion.write('Motion: ', font=('arial', 15, 'bold'))

    # Random put the monster inside the motion area, with a fair distance from the snake.
    while True:
        ini_mon_x = random.randrange(-230, 230, 20)
        ini_mon_y = random.randrange(-270, 190, 20)
        if (abs(ini_mon_x - 0) > 100) and (abs(ini_mon_y - 0) > 100):
            break
    g_monster = createTurtle(ini_mon_x, ini_mon_y, "purple", "purple")
    g_snake = createTurtle(0,0,"red", "red")

    g_screen.onscreenclick(startGame)
    g_screen.update()
    g_screen.listen()
    g_screen.mainloop()



