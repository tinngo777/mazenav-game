#import pygame and other files
import pygame
import sys
from tank import Tank
from maze import Maze
from user import user_commands

#Initialize the game
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2)


#Setup Window
WIDTH = 1280
HEIGHT = 720

#Window setup, etc.
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

def execute_commands(tank, commands):
    for command in commands:
        action, *value = command.split()
        if action == 'forward':
            steps = int(value[0]) * 20  # Adjust the multiplier as needed
            for _ in range(steps):
                tank.update(0, 1)
                yield pygame.time.wait(50)
        elif action == 'right':
            tank.update(90, 0)
            yield pygame.time.wait(50)
        elif action == 'left':
            tank.update(-90, 0)
            yield pygame.time.wait(50)


def show_popup(message):

    #Choose font and size
    font = pygame.font.SysFont('arial', 36)

    popup_width, popup_height = 300, 150
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    pygame.draw.rect(screen, white, popup_rect)
    pygame.draw.rect(screen, black, popup_rect, 2)

    text = font.render(message, True, black)
    text_rect = text.get_rect(center=popup_rect.center)
    screen.blit(text, text_rect)

    pygame.display.flip()

    # Wait for user to close the pop-up
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def check_collision_with_circle(tank_position, circle_center, circle_radius):
    distance = ((tank_position[0] - circle_center[0]) ** 2 + (tank_position[1] - circle_center[1]) ** 2) ** 0.5
    return distance <= circle_radius

def check_collision_with_star(tank_rect, star_rect):
    return tank_rect.colliderect(star_rect)

def main():

    #Setup Window
    WIDTH = 1280
    HEIGHT = 720

    #Window setup, etc.
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    #Choose font and size
    font = pygame.font.SysFont('arial', 36)
    
    #Init tank and maze
    starting_position = (WIDTH * 19 // 20, HEIGHT // 1.086)
    tank_speed = 7.69
    tank = Tank(starting_position, tank_speed)
    maze = Maze()

    #Circle 
    yellow_circle_center = (WIDTH * 1 // 30, HEIGHT * 1 // 20)
    yellow_circle_radius = 15

    #Yellow Star
    star_size = (30, 30)
    yellow_star = pygame.image.load('resources/yellow-star.png')
    yellow_star = pygame.transform.scale(yellow_star, star_size)
    yellow_star_rect = yellow_star.get_rect(center = yellow_circle_center)

    #Explosion sound
    explosion_sound = pygame.mixer.Sound('resources/Bomb_Exploding-Sound_Explorer-68256487.wav')
    explosion_sound.set_volume(1.0)  # Set volume to maximum

    #Winning sound
    winning_sound = pygame.mixer.Sound('resources/Ta Da-SoundBible.com-1884170640.wav')
    winning_sound.set_volume(1.0)  # Set volume to maximum

    #Load the fire streak image
    fire_streak_image = pygame.image.load('resources/fire-flames-explosion-free-png-3770450750.png')
    fire_streak_image = pygame.transform.scale(fire_streak_image, (30, 30))


    #user's command will go here 
    command_generator = execute_commands(tank, user_commands)    

    clock = pygame.time.Clock()
    run = True

    game_over = False  # Add this variable to track game state
    wait_time = 500000  # Set the initial wait time to 5000 milliseconds (5 seconds)
    wait_start_time = 0  # Variable to store the time when waiting started

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not game_over:
            try:
                next(command_generator)  # Execute the next step in the command sequence
            except StopIteration:
                game_over = True  # Set game_over to True when the command sequence is completed

            if maze.check_collision(tank.get_position()):
                explosion_sound.play()
                show_popup("FAILUREEEE")
                game_over = True  # Set game_over to True when a collision is detected
                wait_start_time = pygame.time.get_ticks()  # Record the start time of waiting
            #Check if tank hit the circle
            tank_rect = tank.get_rect() 
            if check_collision_with_star(tank_rect, yellow_star_rect):
                winning_sound.play()
                show_popup("You Win!")
                game_over = True

        # Draw everything
        road = (0, 0, 200)
        screen.fill(road)
    
        #Draw the yellow circle 
        #pygame.draw.circle(screen, (255, 255, 0), yellow_circle_center, yellow_circle_radius)
        screen.blit(yellow_star, yellow_star_rect.topleft)
        
        
        #Draw tank trail (skip this part)
        #for position in tank.trail:
        #    screen.blit(fire_streak_image, position)
        
        maze.draw(screen)
        tank.draw(screen)
        pygame.display.flip()

        clock.tick(60)

        if game_over:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - wait_start_time

            if elapsed_time >= wait_time:
                run = False  # Set run to False after freezing the screen

        # Check for user input during the wait time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
    