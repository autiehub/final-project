import pygame
import random


pygame.init()


WIDTH, HEIGHT = 800, 600
FPS = 60


WHITE = (255, 255, 255)


background_img = pygame.image.load('assets/background.png')
coin_img = pygame.image.load('assets/coin.png')


class Coin:

    def __init__(self):
        self.image = coin_img
        self.rect = self.image.get_rect
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.randint(100, WIDTH - 200)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario Clone")
    clock = pygame.time.Clock()
    pygame.quit()

if __name__ == "__main__":
    main()