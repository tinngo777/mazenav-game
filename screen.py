import pygame
pygame.init()

# Set up window 
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode([WIDTH, HEIGHT])

#Choose a font and size 
font = pygame.font.SysFont('arial', 36)

#Load the tank image
tank_image = pygame.image.load('tank.png')

#Position of tank
tank_x, tank_y = WIDTH // 2 - 50, HEIGHT // 1.2

#Speed of the tank
tank_speed = 0.3


def main():
    run = True
    global tank_x, tank_y
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Check for key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            tank_x -= tank_speed
        if keys[pygame.K_RIGHT]:
            tank_x += tank_speed
        if keys[pygame.K_UP]:
            tank_y -= tank_speed
        if keys[pygame.K_DOWN]:
            tank_y += tank_speed


        # Fill background
        screen.fill((255, 255, 255))  # Corrected color values

        # Draw a solid blue circle in the center
        #pygame.draw.circle(screen, (0, 0, 255), (WIDTH * 2 // 3, HEIGHT // 2), 25)  # Corrected color values
        #pygame.draw.circle(screen, (255, 0, 0), (WIDTH // 3, HEIGHT // 2), 25)

        #Blit the tank image
        screen.blit(tank_image, (tank_x, tank_y))

        #Render text



        # Flip the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


