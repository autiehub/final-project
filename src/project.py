import pygame
import random


class Cat(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.animations = {
            "idle": [pygame.transform.scale(pygame.image.load(f'assets/cat_idle{i}.png'), (50, 50)) for i in range(1, 3)],
            "run": [pygame.transform.scale(pygame.image.load(f'assets/cat_run{i}.png'), (50, 50)) for i in range(1, 3)],
            "jump": [pygame.transform.scale(pygame.image.load(f'assets/cat_jump{i}.png'), (50, 50)) for i in range(1, 3)],
            "fall": [pygame.transform.scale(pygame.image.load(f'assets/cat_fall{i}.png'), (50, 50)) for i in range(1, 3)],
            "hurt": [pygame.transform.scale(pygame.image.load(f'assets/cat_hurt{i}.png'), (50, 50)) for i in range(1, 3)]
        }
        self.state = "idle"
        self.current_frame = 0
        self.image = self.animations[self.state][self.current_frame]
        self.rect = self.image.get_rect(topleft=(300, 450))
        self.velocity = [0, 0] 
        self.on_ground = False
        self.frame_timer = 0
        self.animation_lock = False
        self.lock_timer = 0
    
    def update(self, screen_width, screen_height, platforms):
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
        self.on_ground = self.check_collision(platforms)
        if self.animation_lock:
            self.lock_timer += 1
            if self.lock_timer > 20:
                self.animation_lock = False
                self.lock_timer = 0
        if not self.animation_lock:
            self.update_state()
        self.animate()

    def check_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity[1] > 0:  
                    self.rect.bottom = platform.rect.top
                    self.velocity[1] = 0
                    self.on_ground = True
                elif self.velocity[1] < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity[1] = 0
        return self.on_ground

    def update_state(self):
        if self.velocity[1] > 2 and not self.on_ground: 
            self.state = "fall"
        elif self.velocity[1] < -2 and not self.on_ground:  
            self.state = "jump"
        elif self.velocity[0] != 0 and self.on_ground:
            self.state = "run"
        elif self.on_ground and self.velocity == [0, 0]:
            self.state = "idle"

    def animate(self):
        self.frame_timer += 1
        if self.frame_timer >= 10: 
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]

    def jump(self):
        if self.on_ground and not self.animation_lock:
            self.velocity[1] = -15
            self.on_ground = False
            self.animation_lock = True  

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
            Platform(100, 450, 200, 20),
            Platform(300, 350, 200, 20),
            Platform(500, 250, 200, 20)
        ]
        coins = [
            Coin(150, 430),
            Coin(350, 330),
            Coin(550, 230)
        ]
    elif level_num == 2:
        platforms = [
            Platform(150, 450, 250, 20),
            Platform(400, 300, 250, 20),
            Platform(600, 150, 250, 20)
        ]
        coins = [
            Coin(180, 430),
            Coin(430, 280),
            Coin(630, 130)
        ]
    elif level_num == 3:
        platforms = [
            Platform(100, 450, 300, 20),
            Platform(450, 300, 250, 20),
            Platform(600, 150, 300, 20)
        ]
        coins = [
            Coin(150, 430),
            Coin(470, 280),
            Coin(650, 130)
        ]
    elif level_num == 4:
        platforms = [
            Platform(50, 450, 300, 20),
            Platform(350, 300, 300, 20),
            Platform(600, 150, 300, 20)
        ]
        coins = [
            Coin(80, 430),
            Coin(380, 280),
            Coin(610, 130)
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
    backgrounds = {}
    for i in range(1, 5):
        try:
            bg = pygame.image.load(f'assets/background{i}.png')
            backgrounds[i] = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        except pygame.error:
            print(f"Error loading background{i}.png")
            backgrounds[i] = pygame.Surface((WIDTH, HEIGHT))
            backgrounds[i].fill((0, 0, 0))
    initial_platform = platforms[0]
    cat.rect.midbottom = initial_platform.rect.midtop
    cat.velocity[1] = 0
    cat.on_ground = True
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
        if keys[pygame.K_SPACE]:
            cat.jump()
        cat.update(WIDTH, HEIGHT, platforms)
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
                initial_platform = platforms[0]
                cat.rect.midbottom = initial_platform.rect.midtop
                cat.velocity[1] = 0
                cat.on_ground = True
        if current_level <= 4:
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