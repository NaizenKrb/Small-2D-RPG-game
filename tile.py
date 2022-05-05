import pygame, os
from settings import Settings

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        self.image = pygame.image.load(os.path.join(Settings.test_path,"rock.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)