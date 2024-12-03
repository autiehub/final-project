import pygame
import random


class Cat(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.animations = {
            "idle": [pygame.image.load(f'assets/cat_idle{i}.png') for i in range(1, 3)],
            "run": [pygame.image.load(f'assets/cat_run{i}.png') for i in range(1, 3)],
            "jump": [pygame.image.load(f'assets/cat_jump{i}.png') for i in range(1, 3)],
            "fall": [pygame.image.load(f'assets/cat_fall{i}.png') for i in range(1, 3)],
            "hurt": [pygame.image.load(f'assets/cat_hurt{i}.png') for i in range(1, 3)]
        }
        self.state = "idle"
        self.current_frame = 0
        self.image = self.animations[self.state][self.current_frame]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(300, 500))
        self.velocity = [0, 0] 
        self.on_ground = False
        self.frame_timer = 0  
    
    def update(self, screen_width, screen_height):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.on_ground:
            self.velocity[1] += 1
        self.rect.x = max(0, min(screen_width - self.rect.width, self.rect.x))
        self.rect.y = min(screen_height - self.rect.height, self.rect.y)
        if self.rect.y >= screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height
            self.velocity[1] = 0
            self.on_ground = True
        self.update_state()
        self.animate()

    def update_state(self):
        if self.velocity[1] > 0 and not self.on_ground:
            self.state = "fall"
        elif self.velocity[1] < 0 and not self.on_ground:
            self.state = "jump"
        elif self.velocity[0] != 0 and self.on_ground:
            self.state = "run"
        elif self.on_ground:
            self.state = "idle"

    def animate(self):
        self.frame_timer += 1
        if self.frame_timer >= 10:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]
            self.image = pygame.transform.scale(self.image, (50, 50))

    def jump(self):
        if self.on_ground:
            self.velocity[1] = -15
            self.on_ground = False

    def move_left(self):
        self.velocity[0] = -5 

    def move_right(self):
        self.velocity[0] = 5

    def stop(self):
        self.velocity[0] = 0

    def hurt(self):
        self.state = "hurt"
        print("Cat is hurt!")


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
    cat = Cat()
    current_level = 1
    platforms, coins = load_level(current_level)
    collected_coins = 0
    required_coins = 3
    backgrounds = {
        1: pygame.image.load('assets/background1.png'),
        2: pygame.image.load('assets/background2.png'),
        3: pygame.image.load('assets/background3.png'),
        4: pygame.image.load('assets/background4.png')
    }
    for level, bg in backgrounds.items():
        backgrounds[level] = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cat.move_left()
        elif keys[pygame.K_RIGHT]:
            cat.move_right()
        else:
            cat.stop()
        if keys[pygame.K_UP]:
            cat.jump()
        cat.update(WIDTH, HEIGHT)
        cat.on_ground = False
        for platform in platforms:
            if cat.rect.colliderect(platform.rect):
                if cat.velocity[1] > 0:
                    cat.rect.bottom = platform.rect.top
                    cat.velocity[1] = 0
                    cat.on_ground = True
        for coin in coins[:]:
            if cat.rect.colliderect(coin.rect):
                coins.remove(coin)
                collected_coins += 1
                print(f"Collected coins: {collected_coins}")
        if collected_coins >= required_coins:
            collected_coins = 0
            current_level += 1
            if current_level > 4:
                print("You Win!")
                running = False
            else:
                platforms, coins = load_level(current_level)
        screen.blit(backgrounds[current_level], (0, 0))
        screen.blit(cat.image, cat.rect)
        for platform in platforms:
            platform.draw(screen)
        for coin in coins:
            coin.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()