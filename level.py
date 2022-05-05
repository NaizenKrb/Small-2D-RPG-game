import pygame
from settings import Settings
from tile import Tile
from player import Player

class Level():
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()  # Group of sprites that are visible
        self.obstacle_sprites = pygame.sprite.Group() # Group of the sprites that the Player can collide with


        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(Settings.world_map):
            for col_index, col in enumerate(row):
                x = col_index * Settings.tilesize
                y = row_index * Settings.tilesize
                if col == "x":
                    Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
                if col == "p":
                    self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)



    def update(self):
        self.visible_sprites.update()
        

    def draw(self):

        self.visible_sprites.custom_draw(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100,200)

    def custom_draw(self, player):

        self.offset.x = player.rect.x - self.half_width
        self.offset.y = player.rect.y - self.half_heigth

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
    