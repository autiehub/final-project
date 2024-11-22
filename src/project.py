import pygame
import random


WIDTH = 800
HEIGHT = 600


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario Clone")
    background_img = pygame.image.load('assets/background.png')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        for x in range(0, WIDTH, background_img.get_width()):
            for y in range(0, HEIGHT, background_img.get_height()):
                screen.blit(background_img, (x,y))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()