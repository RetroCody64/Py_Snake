"""
Program name: Snake
Author: Ricardo Lopes (Alex128)
Original Release Date: 26/04/20
Current Version Release Date: 28/04/20
Build: 1.1
License: GNU GPL (General Public License)
"""

import pygame, random, sys, platform, os, time  # Game lib, random numb, exit program, windows or linux, get path, sleep

# Initiate program
pygame.init()  # Start pygame module
pygame.font.init()  # Initialize font module
pygame.mixer.init()  # Start mixer module
pygame.display.set_caption("Snake")  # Set title to Snake
icon = pygame.image.load("Snek.ico")  # Load icon
pygame.display.set_icon(icon)  # Set icon

# Determine platform
if platform.system() == "Windows":  # If Windows
    path_char = '\\'  # Set path char

elif platform.system() == "Linux" or platform.system() == "Darwin":  # If Linux or MacOS
    path_char = '/'  # Set path char

# Define variables/constants
XY_SIZE = [20, 20]  # Set size for fruit/snake
xy_snake_dir = [0, 0]  # Snake direction
snake_color = (0, 255, 0)  # Snake color
fruit_color = (255, 0, 0)  # Fruit color
score = 0  # Set score to 0
snake_length = 0  # Snake length
fruit_in_snake = False  # Detect if fruit is inside snake
snake_in_snake = False  # Detect if snake is inside itself
music_state = (0, 255, 0)  # Music label color
startup = True  # Check if program is starting (draw screen despite snake not moving)
big_boss = 0  # Store b presses

SCREEN = pygame.display.set_mode((400, 400))  # Set screen size (x, y) (Must be list)
SCORE_FONT = pygame.font.SysFont("Consolas", 24)  # Set specific font
button_font = pygame.font.SysFont("Consolas", 18)  # Set specific font

fruit = pygame.Rect(xy_snake_dir, XY_SIZE)  # Create fruit rectangle (start position is 0x 0y, 20 width 20 height)
snake = [pygame.Rect(xy_snake_dir, XY_SIZE)]  # Create fruit rectangle
FPS = pygame.time.Clock()  # Set fps to store clock object

# Setup game
snake[0] = snake[0].move(180, 180)  # Move snake head to center of window
fruit = fruit.move(random.randint(0, 380), random.randint(25, 380))  # Place fruit in random position between 25x & 380x and 25y & 380y
pygame.mixer.music.load(os.getcwd() + "{}Music{}snake.mp3".format(path_char, path_char))  # Load music
pygame.mixer.music.set_volume(0.5)  # Set volume to 25%
pygame.mixer.music.play(loops=-1)  # Loop forever

while 1:  # Forever loop
    for event in pygame.event.get():  # Get all events
        if event.type == pygame.QUIT:  # If event is quit
            sys.exit()  # Exit program

# Detect snake collision with itself
    if xy_snake_dir != [0, 0]:  # If snake is moving
        for part in snake[9:]:  # For each part starting on index 9  (9 can never collide with 0 cuz it's too close to it and it's far away that it's not colliding with the head)
            if pygame.Rect.colliderect(snake[0], part):  # If head (snake[0]) collides with part
                snake_in_snake = True  # Snake collided

# Detect if snake is outside borders or collided with self
    if snake[0].left < 0 or snake[0].top < 25 or snake[0].left >= 380 or snake[0].top >= 380 or snake_in_snake:  # If snake colides with limits or is inside body
        snake_in_snake = False  # Reset snake in snake collision detection
        score = 0  # Reset score
        snake_length = 0  # Reset length
        snake[0] = snake[0].move(-snake[0].left, -snake[0].top)  # Zero snake's head xy values
        snake[0] = snake[0].move(180, 180)  # Move snake to middle of window
        snake = [snake[0]]  # Clear body and store only snake's head
        xy_snake_dir = [0, 0]  # Freeze head

# Get mouse position, mouse buttons state and pressed keys. Check if pressed keys equal movement, pause or easter egg
    mouse = pygame.mouse.get_pos()  # Get mouse position (x, y)
    click = pygame.mouse.get_pressed()  # Get mouse buttons states (left, middle, right)
    keys = pygame.key.get_pressed()  # Get all pressed keys
    if keys[pygame.K_LEFT] and xy_snake_dir != [4, 0]:  # If left pressed and not moving right
        xy_snake_dir = [-4, 0]  # Move left

    if keys[pygame.K_RIGHT] and xy_snake_dir != [-4, 0]:  # If right pressed and not moving left
        xy_snake_dir = [4, 0]  # Move right

    if keys[pygame.K_UP] and xy_snake_dir != [0, 4]:  # If up pressed and not moving down
        xy_snake_dir = [0, -4]  # Move up

    if keys[pygame.K_DOWN] and xy_snake_dir != [0, -4]:  # If down pressed and not moving up
        xy_snake_dir = [0, 4]  # Move down

    if keys[pygame.K_p]:  # If p pressed
        xy_snake_dir = [0, 0]  # Pause game

    if keys[pygame.K_b]:  # If b pressed
        if big_boss < 3:  # If big boss counter is less than 3
            big_boss += 1  # Count press
            time.sleep(0.1)  # Sleep for 100ms
            if big_boss == 2:  # If pressed 2x
                pygame.mixer.music.stop()  # Stop music
                pygame.mixer.music.load(os.getcwd() + "{}Music{}snake eater.mp3".format(path_char, path_char))  # Load new song
                pygame.mixer.music.play(loops=-1)  # Play forever
                snake_color = (255, 128, 0)  # Snake color
                fruit_color = (0, 255, 0)  # Fruit color
                music_state = (0, 255, 0)  # Music label color

            elif big_boss == 3:  # If big boss counter is 3
                pygame.mixer.music.stop()  # Stop music
                pygame.mixer.music.load(os.getcwd() + "{}Music{}snake.mp3".format(path_char, path_char))  # Load new song
                pygame.mixer.music.play(loops=-1)  # Play forever
                big_boss = 0  # Reset big boss counter
                snake_color = (0, 255, 0)  # Snake color
                fruit_color = (255, 0, 0)  # Fruit color
                music_state = (0, 255, 0)  # Music label color

# Pause/Unpause mixer according to paused state
    if xy_snake_dir == [0, 0]:  # If game paused
        pygame.mixer.music.pause()  # Pause mixer

    else:  # If mixer not active
        pygame.mixer.music.unpause()  # Unpause music

# Check if snake ate fruit
    if pygame.Rect.colliderect(snake[0], fruit):  # Check if head collided with fruit
        if score == 999:  # If score reaches limit
            score = 0  # Reset score
            snake_length = 0  # Reset length
            snake = [snake[0]]  # Clear body and store only snake's head
        score += 1  # Add 1 point
        snake_length += 2  # Increase length by 2 heads
        fruit = fruit.move(-fruit.left, -fruit.top)  # Zero fruit's position
        fruit = fruit.move(random.randint(0, 380), random.randint(25, 380))  # Set new random position
    # Check fruit isn't inside snake
        for part in snake:  # For every part in snake
            if pygame.Rect.colliderect(part, fruit):  # If part collides with snake
                fruit_in_snake = True  # Fruit is inside snake

    # If fruit inside snake, keep generating new positions until it isn't
        while fruit_in_snake:  # While fruit inside snake
            breaked = False  # Check if for loop was interrupted or finished
            fruit = fruit.move(-fruit.left, -fruit.top)  # Zero fruit's position
            fruit = fruit.move(random.randint(0, 380), random.randint(25, 380))  # Set new random position
            for part in snake:  # For every part in snake
                if pygame.Rect.colliderect(part, fruit):  # If fruit collides with part
                    breaked = True  # For loop interrupted
                    break  # Interrupt loop

            if not breaked:  # If for loop wasn't interrupted
                fruit_in_snake = False  # End loop

# If snake is moving keep saving the head's position (draw long snek)
    if xy_snake_dir != [0, 0]:  # If snake is moving
        snake.insert(1, snake[0])  # Add head's values to snake list on index 1
        if len(snake) - 1 > snake_length:  # If snake has more head values than it's supposed to
            del(snake[-1])  # Delete last stored head

    snake[0] = snake[0].move(xy_snake_dir)  # Move head

# Music button (Control coloring and action on button press)
    SCREEN.fill((0, 0, 0))  # Clear SCREEN (fill with black)
    if mouse[0] >= 2 and mouse[0] <= 55 and mouse[1] >= 2 and mouse[1] <= 20:  # If mouse inside rect
        if music_state[1] == 255:  # If music active
            SCREEN.blit(button_font.render("Music", 1, (music_state[0], music_state[1] - 55, music_state[2])), (2, 2))  # Draw button with darker green

        else:  # If music not active
            SCREEN.blit(button_font.render("Music", 1, (music_state[0] - 55, music_state[1], music_state[2])), (2, 2))  # Draw button with darker red

        if click[0] == 1 and pygame.mixer.music.get_busy():  # Check if left mouse button pressed and mixer is playing
            music_state = (255, 0, 0)  # Store music color (red = off)
            pygame.mixer.music.stop()  # Stop music
            time.sleep(0.1)  # Wait for 100 ms

        elif click[0] == 1 and not pygame.mixer.music.get_busy():  # Check if left mouse button pressed and mixer is not playing
            music_state = (0, 255, 0)  # Store music color (green = on)
            pygame.mixer.music.play(loops=-1)  # Play forever
            time.sleep(0.1)  # Wait for 100 ms

    else:
        SCREEN.blit(button_font.render("Music", 1, music_state), (2, 2))  # Draw button

# Draw and update screen
    SCREEN.blit(SCORE_FONT.render("Score: {}".format(score), 1, (255, 255, 255)), (268, 0))  # Draw text (text, antialias [edge smoothing], color, position)
    pygame.draw.line(SCREEN, (255, 255, 255), (0, 24), (0, 24), 800)  # Draw line (window, color, start position, end position, width) Note: End == start cuz we want a thin line not a thick one

    for part in snake:  # For all parts of the snake's body
        pygame.draw.rect(SCREEN, snake_color, part)  # Draw part (window, color, rect)

    pygame.draw.rect(SCREEN, fruit_color, fruit)  # Draw fruit
    pygame.display.update()  # Update entire window
    FPS.tick(60)  # Run at 60 fps

"""
https://stackoverflow.com/questions/10942011/speed-of-an-object-in-pygame
https://www.pygame.org/docs/ref/rect.html?highlight=move#pygame.Rect.move
https://www.pygame.org/docs/ref/key.html
https://www.youtube.com/watch?v=57bkG0HytI8
https://www.pygame.org/docs/ref/rect.html#pygame.Rect.collidepoint
https://stackoverflow.com/questions/37800894/what-is-the-surface-blit-function-in-pygame-what-does-it-do-how-does-it-work
https://pythonprogramming.net/changing-pygame-icon/
https://stackoverflow.com/questions/40566585/how-to-change-the-name-of-a-pygame-window/40595418

--noconsole
--onefile
--icon=file.filetype
"""
