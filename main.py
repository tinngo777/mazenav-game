#import pygame and other files
import pygame
from tank import Tank
from maze import Maze
from user import user_commands

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


def main():
    pygame.init()

    #Window setup, etc.
    #Setup Window
    WIDTH = 1280
    HEIGHT = 720
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    #Choose font and size
    font = pygame.font.SysFont('arial', 36)

    #Init tank and maze
    starting_position = (WIDTH * 19 // 20, HEIGHT // 1.086)
    tank_speed = 4
    tank = Tank(starting_position, tank_speed)
    maze = Maze()

    #user's command will go here 
    command_generator = execute_commands(tank, user_commands)    

    clock = pygame.time.Clock()
    run = True

    game_over = False  # Add this variable to track game state
    wait_time = 15000  # Set the initial wait time to 5000 milliseconds (5 seconds)
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
                print("FAILUREEEEEEEE")
                game_over = True  # Set game_over to True when a collision is detected
                wait_start_time = pygame.time.get_ticks()  # Record the start time of waiting

        # Draw everything
        screen.fill((255, 255, 255))
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
    