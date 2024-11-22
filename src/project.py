import pygame
import random


pygame.init()


WIDTH, HEIGHT = 800, 600
FPS = 60


WHITE = (255, 255, 255)


background_img = pygame.image.load('assets/background.png')
coin_img = pygame.image.load('assets/coin.png')


coin_img = pygame.transform.scale(coin_img, (30, 30))




class Coin():

    def __init__(self):
        self.image = coin_img
        self.rect = self.image.get_rect
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.randint(100, HEIGHT - 200)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario Clone")
    clock = pygame.time.Clock()
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    screen.blit(background_img, (0, 0))
    pygame.quit()


if __name__ == "__main__":
    main()