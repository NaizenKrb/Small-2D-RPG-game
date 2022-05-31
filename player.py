import pygame, os
from settings import Settings
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, game):
        super().__init__(groups)
        
        self.game = game
        
        self.image = pygame.image.load(os.path.join(Settings.test_path,"player.png")).convert_alpha()
        self.x, self.y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (self.x*Settings.scaling, self.y*Settings.scaling))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-50, -60)

        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15
        
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = Settings.character_path
        self.animations = {"up": [], "down": [], "left": [], "right": [], "right_idle": [],
                          "left_idle": [], "up_idle": [], "down_idle": [],"right_attack": [],
                          "left_attack": [], "up_attack": [], "down_attack": []}
        
        for animation in self.animations.keys():
            full_path = os.path.join(character_path, animation)
            self.animations[animation] = list(import_folder(full_path).values())
        print(self.animations)

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status and not "idle" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")
        
    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        #self.rect.center += self.direction * speed
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.game.input_manager.attack_time >= self.attack_cooldown:
                self.attacking = False
    
    def animate(self):
        animation = self.animations[self.status]
        
        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
    
    def update(self):
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        

