import pygame
import random
import os


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Clone")


WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)


def load_image(name):
    return pygame.image.load(os.path.join('assets', name))


class Platform(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Coin(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('coin.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Cat(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.velocity = [0, 0]  
        self.state = "idle"
        self.animations = {
            "idle": self.load_frames("idle"),
            "jumping": self.load_frames("jumping"),
            "running": self.load_frames("running"),
            "hurt": self.load_frames("hurt"),
            "falling": self.load_frames("falling")
        }
        self.current_frame = 0
        self.image = self.animations["idle"][self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def load_frames(self, action):
        """Load frames for a specific action."""
        frames = []
        frame_index = 1
        while True:
            frame_name = f'assets/cat/{action}_{frame_index}.png'
            if os.path.exists(frame_name):
                frames.append(pygame.image.load(frame_name))
                frame_index += 1
            else:
                break
        return frames

    def update(self):
        """Update the animation frame based on state."""
        if self.state == "running":
            self.current_frame = (self.current_frame + 1) % len(self.animations["running"])
            self.image = self.animations["running"][self.current_frame]
        elif self.state == "jumping":
            self.current_frame = (self.current_frame + 1) % len(self.animations["jumping"])
            self.image = self.animations["jumping"][self.current_frame]
        elif self.state == "falling":
            self.current_frame = (self.current_frame + 1) % len(self.animations["falling"])
            self.image = self.animations["falling"][self.current_frame]
        else:  # idle or hurt
            self.current_frame = (self.current_frame + 1) % len(self.animations["idle"])
            self.image = self.animations["idle"][self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        """Draw the cat on the screen."""
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
    clock = pygame.time.Clock()
    cat = Cat(WIDTH // 2, HEIGHT // 2)
    cat_group = pygame.sprite.Group()
    cat_group.add(cat)
    current_level = 1
    platforms, coins = load_level(current_level)
    collected_coins = 0
    required_coins = 3
    background_images = {
        1: load_image('background1.png'),
        2: load_image('background2.png'),
        3: load_image('background3.png'),
        4: load_image('background4.png')
    }

    for level in background_images:
        background_images[level] = pygame.transform.scale(background_images[level], (WIDTH, HEIGHT))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cat.state = "running"
            cat.x -= 5
        elif keys[pygame.K_RIGHT]:
            cat.state = "running"
            cat.x += 5
        else:
            cat.state = "idle"
        if keys[pygame.K_SPACE]:
            if cat.velocity[1] == 0:
                cat.velocity[1] = -15 
        cat.velocity[1] += 1  
        cat.y += cat.velocity[1]
        if cat.y > HEIGHT - 100:
            cat.y = HEIGHT - 100
            cat.velocity[1] = 0
        for platform in platforms:
            if cat.rect.colliderect(platform.rect):
                if cat.velocity[1] > 0 and cat.rect.bottom >= platform.rect.top:
                    cat.y = platform.rect.top - 50
                    cat.velocity[1] = 0
        for coin in coins[:]:
            if cat.rect.colliderect(coin.rect):
                coins.remove(coin)
                collected_coins += 1
        if collected_coins >= required_coins:
            if current_level < 4:
                current_level += 1
                platforms, coins = load_level(current_level)
                collected_coins = 0
            else:
                print("You win!")
                running = False
        screen.fill(WHITE)
        screen.blit(background_images[current_level], (0, 0))
        for platform in platforms:
            platform.draw(screen)
        for coin in coins:
            coin.draw(screen)
        cat_group.draw(screen)
        font = pygame.font.SysFont(None, 36)
        coin_text = font.render(f'Coins: {collected_coins}', True, BLUE)
        screen.blit(coin_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()