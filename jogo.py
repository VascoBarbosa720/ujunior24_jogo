# Example file showing a circle moving on screen
import pygame
import random
import math

# pygame setup
pygame.init()
pygame.display.set_caption('Flappy Bird do Vasco e do André')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

running = True
dt = 0
start = False
v = 0
a = 1
player_pos = pygame.Vector2(590, 329)
bird = pygame.image.load("./birdsm.png").convert_alpha()
bird_cima = pygame.transform.rotate(bird, -10)
bird_baixo = pygame.transform.rotate(bird, 10)

score = 0

class Obstacle:
    def __init__(self):
        self.gap_height = random.randint(20, 460)
        self.top_rect = pygame.Rect(1280, 0, 150, self.gap_height)
        self.bottom_rect = pygame.Rect(1280, self.gap_height + 240, 150, 480 - self.gap_height)
        self.left = 1280
        self.right = self.left + 150
        self.is_behind_bird = False
        self.generation_triggered = False
    
    def update_pos(self, dt):
        self.left -= 250 * (math.log(math.log(math.log(score + 1) + 1) + 1) + 1) * dt
        self.right = self.left + 150
        self.top_rect.left = self.left
        self.bottom_rect.left = self.left
    
    def render(self):
        pygame.draw.rect(screen, "darkgreen", self.top_rect)
        pygame.draw.rect(screen, "darkgreen", self.bottom_rect)

obstacles = []
app = True
tobedeleted = []

font = pygame.font.Font('freesansbold.ttf', 50)
text = font.render('Click SPACE to play', True, "black", "lightblue")

while not start:
    screen.fill("lightblue")
    screen.blit(bird, player_pos)
    pygame.draw.rect(screen, "darkgreen", pygame.Rect(0, 700, 1280, 20))
    screen.blit(text, (400, 500))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        start = True
        v = -10
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            start = True
            
    pygame.display.flip()
    clock.tick(60)
 
while running:

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("lightblue")

    #ground
    pygame.draw.rect(screen, "darkgreen", pygame.Rect(0, 700, 1280, 20))

    if app:
        obstacles.append(Obstacle())
        app = False
    
    #render obstacles, update position, and check collision with bird
    for n, obs in enumerate(obstacles):
        obs.update_pos(dt)
        obs.render()

        if (obs.right > (player_pos.x + 20) and obs.left < (player_pos.x + 80)) and (obs.top_rect.bottom > player_pos.y or obs.bottom_rect.top - 62 < player_pos.y):
            running = False
            break
        
        if obs.right < (player_pos.x + 20) and not obs.is_behind_bird:
            obs.is_behind_bird = True
            score += 1
        
        if obs.left <= -160:
            tobedeleted.append(n)
        
        if ((player_pos.x + 80) < (obs.left - 0)) and ((player_pos.x + 80) > (obs.left - 80)) and not obs.generation_triggered:
            obs.generation_triggered = True
            app = True 
  
    #delete offscreen obstacles
    for index in tobedeleted:
        obstacles.pop(index)

    tobedeleted = []

    if player_pos.y > 638:
        running = False
    
    #update player position and velocity
    v += a
    player_pos.y += v 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        v = -10

    #render bird
    if (v > -5 and v < 5):
        screen.blit(bird, player_pos)
    elif (v < -5):
        screen.blit(bird_baixo, player_pos)
    else:
        screen.blit(bird_cima, player_pos)

    #render score
    score_text = font.render(str(score), True, "black").convert_alpha()
    screen.blit(score_text, (630, 40))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

#print(score)
pygame.quit()
