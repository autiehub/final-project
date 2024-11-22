import pygame
import random


WIDTH = 1920
HEIGHT = 1080


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Mario Clone")
    background_img = pygame.image.load('assets/background.png')
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT)).convert()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        for x in range(0, WIDTH, background_img.get_width()):
            for y in range(0, HEIGHT, background_img.get_height()):
                screen.blit(background_img, (x,y))
        pygame.display.flip()
        clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    main()