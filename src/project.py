import pygame
import random


class Platform():
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 128, 0), self.rect) 


class Coin():
    
    def __init__(self, x, y):
        self.image = pygame.Surface((20, 20)) 
        self.image.fill((255, 255, 0))  
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario Clone")
    clock = pygame.time.Clock()
    FPS = 60
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    player_size = (50, 50)
    player_pos = [WIDTH // 2, HEIGHT - 100]
    player_velocity = [0, 0]
    GRAVITY = 1
    JUMP_STRENGTH = -15
    platforms = [
        Platform(200, 500, 200, 20),
        Platform(400, 400, 200, 20),
        Platform(100, 300, 200, 20),
    ]
    coins = []
    for platform in platforms:
        x = random.randint(platform.rect.left + 20, platform.rect.right - 40)
        y = platform.rect.top - 20
        coins.append(Coin(x, y))
    collected_coins = 0
    required_coins = 5
    trophy_image = pygame.image.load('assets/trophy.png')
    trophy_rect = trophy_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
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
            running = False
        screen.fill(WHITE)
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
            screen.blit(trophy_image, trophy_rect)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()