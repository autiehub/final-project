import pygame
import random


class Platform():
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 128, 0), self.rect)


class Coin():
    
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/coin.png') 
        self.image = pygame.transform.scale(self.image, (30, 30))  
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def load_level(level_num):
    platforms = []
    coins = []
    if level_num == 1:
        platforms = [
            Platform(100, 500, 200, 20),
            Platform(300, 400, 200, 20),
            Platform(500, 300, 200, 20)
        ]
        coins = [
            Coin(150, 480),
            Coin(350, 380),
            Coin(550, 280)
        ]
    elif level_num == 2:
        platforms = [
            Platform(150, 550, 250, 20),
            Platform(400, 400, 250, 20),
            Platform(600, 250, 250, 20)
        ]
        coins = [
            Coin(180, 530),
            Coin(430, 380),
            Coin(630, 230)
        ]
    elif level_num == 3:
        platforms = [
            Platform(100, 500, 300, 20),
            Platform(450, 350, 250, 20),
            Platform(600, 200, 300, 20)
        ]
        coins = [
            Coin(150, 480),
            Coin(470, 330),
            Coin(650, 180)
        ]
    elif level_num == 4:
        platforms = [
            Platform(50, 550, 300, 20),
            Platform(350, 400, 300, 20),
            Platform(600, 250, 300, 20)
        ]
        coins = [
            Coin(80, 530),
            Coin(380, 380),
            Coin(610, 230)
        ]
    return platforms, coins


def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario Clone")
    clock = pygame.time.Clock()
    FPS = 60
    BLUE = (0, 0, 255)
    player_size = (50, 50)
    player_pos = [WIDTH // 2, HEIGHT - 100]
    player_velocity = [0, 0]
    GRAVITY = 1
    JUMP_STRENGTH = -15
    current_level = 1
    platforms, coins = load_level(current_level)
    collected_coins = 0
    required_coins = 3
    background_images = {
        1: pygame.image.load('assets/background1.png'),
        2: pygame.image.load('assets/background2.png'),
        3: pygame.image.load('assets/background3.png'),
        4: pygame.image.load('assets/background4.png')
    }
    for level in background_images:
        background_images[level] = pygame.transform.scale(background_images[level], (WIDTH, HEIGHT))
    running = True
    win = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_velocity[0] = -5
        elif keys[pygame.K_RIGHT]:
            player_velocity[0] = 5
        else:
            player_velocity[0] = 0
        if keys[pygame.K_SPACE]:
            if player_velocity[1] == 0:
                player_velocity[1] = JUMP_STRENGTH
        player_velocity[1] += GRAVITY
        player_pos[0] += player_velocity[0]
        player_pos[1] += player_velocity[1]
        player_rect = pygame.Rect(player_pos[0], player_pos[1], *player_size)
        on_platform = False
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                if player_velocity[1] > 0 and player_rect.bottom >= platform.rect.top:
                    player_pos[1] = platform.rect.top - player_size[1]
                    player_velocity[1] = 0
                    on_platform = True
        if player_pos[1] > HEIGHT - player_size[1]:
            player_pos[1] = HEIGHT - player_size[1]
            player_velocity[1] = 0
            on_platform = True
        for coin in coins[:]:
            if player_rect.colliderect(coin.rect):
                coins.remove(coin)
                collected_coins += 1
        if collected_coins >= required_coins:
            win = True
            if current_level < 4:
                current_level += 1
                platforms, coins = load_level(current_level)
                collected_coins = 0
                win = False
            else:
                running = False
        screen.blit(background_images[current_level], (0, 0))
        pygame.draw.rect(screen, BLUE, (*player_pos, *player_size))
        for platform in platforms:
            platform.draw(screen)
        for coin in coins:
            coin.draw(screen)
        font = pygame.font.SysFont(None, 36)
        coin_text = font.render(f'Coins: {collected_coins}', True, (0, 0, 0))
        screen.blit(coin_text, (10, 10))
        if win:
            win_text = font.render("You Win!", True, (0, 255, 0))
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()