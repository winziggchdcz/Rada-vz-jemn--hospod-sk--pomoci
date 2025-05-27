import random
import pygame # klíčová knihovna umožňující vytvářet jednoduše nejen hry
pygame.init() # nutný příkaz hned na začátku pro správnou inicializaci knihovny

text_font = pygame.font.Font("PixelifySans.ttf",100) # 100 je velikost písma
score_font = pygame.font.Font("PixelifySans.ttf",50) # 100 je velikost písma

framerate = 60
score = 0
enemy_cooldown = 0

class Player(pygame.sprite.Sprite):
    def __init__(self): # konstruktor - volá se vždy při vytvoření (inicializaci)
        super().__init__() # volá konstruktor třídy Sprite pro správnou inicializaci
        self.image = pygame.image.load("dinosaur.png")
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect(midbottom = (100, 0.75*window_height))
        self.gravity = 0

    def player_input(self): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300: # výskok po zmáčknutí mezerníku
            self.gravity = -20

    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= 0.75*window_height:
            self.rect.bottom = 0.75*window_height

    def update(self):
        self.player_input()
        self.apply_gravity()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = random.randrange(25, 75)

        self.image = pygame.image.load("kaktus.png")
        self.image = pygame.transform.scale(self.image, (self.size,self.size))
        self.rect = self.image.get_rect(midbottom = (window_width, 0.75*window_height))
        self.speed = 5
    
    def move(self):
        global score
        self.rect.left -= self.speed
        if self.rect.right < 0:
            self.rect.left = window_width
            score += 1
            self.kill()

    def update(self):
        self.move()

def is_collision():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty() # smažeme všechny překážky
        return False # hra má skončit
    return True # hra má pokračovat

# herní okno
window_width = 800
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))
    # dvojice (w,h) v parametru se nazývá *tuple*
pygame.display.set_caption("Dinosauří hra") # nastavíme do hlavičky okna název hry

clock = pygame.time.Clock() # díky hodinám nastavíme frekvenci obnovování herního okna

# přidání objektů (tzv. surface) do scény
sky_surface = pygame.Surface((window_width,0.75*window_height))
sky_surface.fill("darkslategray1")
ground_surface = pygame.Surface((window_width,0.25*window_height))
ground_surface.fill("lightsalmon4")

# GROUPS
# GroupSingle - skupina s 1 objektem (hráč)
# Group - skupina s více objekty (nepřátelé)
player = pygame.sprite.GroupSingle() #vytvoříme skupinu pro hráče
player.add(Player()) # přidáme do ní novéh hráče typu Player (třída, co jsme vytvořili)

obstacle_group = pygame.sprite.Group()

game_active = True

# herní smyčka
while True:
    # zjistíme co dělá hráč za akci
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # zavřeme herní okno
            exit() # úplně opustíme herní smyčku, celý program se ukončí
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active == False: # když je GAME OVER stav
                    game_active = True
                    obstacle_group.add(Obstacle())
                    score = 0

    if game_active:
        # pozadí
        screen.blit(sky_surface,(0,0)) # položíme sky_surface na souřadnice [0,0]
        screen.blit(ground_surface,(0,0.75*window_height)) # položíme ground_surface na souřadnice [0,300] (pod oblohu)

        #skore
        score_surface = score_font.render(f"Skóre: {score}", True, "Black")
        screen.blit(score_surface, (0 , 0))

        # nepřítel
        obstacle_group.draw(screen)
        obstacle_group.update()

        enemy_cooldown += 1

        if enemy_cooldown > framerate:
            obstacle_group.add(Obstacle()) 
            enemy_cooldown = 0

        # HRÁČ
        player.draw(screen)
        player.update()
        
        game_active = is_collision() # nastala kolize? pokud ano -> konec hry

    else:  # hra neběží
        screen.blit(sky_surface,(0,0))

        text_font = pygame.font.Font("PixelifySans.ttf",100) # 100 je velikost písma
        text_surface = text_font.render("GAME OVER!", True, "Black") # text, anti-aliasing, černá barva písma
        screen.blit(text_surface, (0, 0))
        pygame.display.update()

    pygame.display.update() # updatujeme vykreslené okno
    clock.tick(framerate) # herní smyčka proběhne maximálně 60x za sekundu