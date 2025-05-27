import pygame

class Zbran(pygame.sprite.Sprite):
    def __init__():
        self.image = pygame.image.load("sprites/dinosaur.png")
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect(midbottom = (100, 0.75*window_height))