import pygame
import random


pygame.init()


WIDTH = 1920
HEIGHT = 1080

sprite_sheet = pygame.image.load('assets/mario_sprite_sheet.png')
background_img = pygame.image.load('assets/background.png')
coin_img = pygame.image.load('assets/coin.png')


coin_img = pygame.transform.scale(coin_img, (30, 30))


class Player():

    def __init__(self):
        self.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 70
        self.velocity_y = 0
        self.on_ground = True

    def update(self):
        self.rect.y += self.velocity_y
        if not self.on_ground:
            self.velocity_y += 1
        if self.rect.y >= HEIGHT - 70:
            self.rect.y = HEIGHT - 70
            self.velocity_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.velocity_y = -15
            self.on_ground = False


class Coin():

    def __init__(self):
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.radint(100, HEIGHT - 200)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Mario Clone")
    clock = pygame.time.Clock()
    player = Player()
    coins = [Coin() for coin in range(5)]
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            player.rect.x -= 5
        player.update()
        for coin in coins[:]:
            if player.rect.colliderect(coin.rect):
                coins.remove(coin)
                score += 1
                print(f"Score: {score}")
        screen.blit(background_img, (0,0))
        screen.blit(player.image, player.rect)
        for coin in coins:
            screen.blit(coin.image, coin.rect)
        pygame.display.flip()
        clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    main()