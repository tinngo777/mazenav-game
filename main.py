#import pygame and other files
import pygame
from tank import Tank
from maze import Maze

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
    starting_position = (WIDTH // 2 - 50, HEIGHT // 1.2)
    tank_speed = 3
    tank = Tank(starting_position, tank_speed)
    maze = Maze()

    # User-defined commands, guests will input here
    user_commands = [
        "forward 3",
        "right",
        "forward 5",
        "left",
        "forward 6"
        # Add more commands as needed
    ]

    command_generator = execute_commands(tank, user_commands)    

    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        try:
            next(command_generator)  # Execute the next step in the command sequence
        except StopIteration:
            pass


        if maze.check_collision(tank.get_position()):
            print("FAILURE. DISOWN. EMOTIONAL DAMAGEEEE insert Steven He")
            run = False
        

        #Draw everything
        screen.fill((255, 255, 255))
        maze.draw(screen)
        tank.draw(screen)
        pygame.display.flip()

        clock.tick(60)


    pygame.quit()


if __name__ == "__main__":
    main()











