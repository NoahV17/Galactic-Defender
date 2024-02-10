""" This is my game that uses a scrolling background,
    sprites that move with the background,
    collision detection, score keeping,
    level difficulty, randomness, and a
    playable character
    
                    "Glactic Defender"
                    Noah Vario 4/24/23

        Your suggestions from alpha sprint in order of severity
    -Remove the use of mouse click to move on in levels
            (COMPLETED)
    -Change movement from booleans to _dx and _dy
            (Would not work because I wanted very direction to work simultaneously, glitches occoured)
    -Use pygame level class
            (Too much time to implement on the already structured game)

        -Completed Features-
    -Scrolling background
    -Controllable spaceship
    -Collision between asteroid and ship
        (triggers sound and -1 hp)
    -Randomly spawning asteroids
    -Difficulty choice on start screen,
        win/loss/waiting screens
    -Game can be replayed
    -Player attack using k_space
    -Add boss that takes damage from player attack
    -Add HP for boss
    -Clear ALL SPRITE GROUPS before a new level initiates
    -Boss animation
"""

# Import and initialize pygame.
import random
import pygame
import math
from os import path
pygame.init()
pygame.mixer.init()

class Background(pygame.sprite.Sprite):
    # Annotate object-level fields
    _dy: int
    _images: list
    
    def __init__(self, image_list: list, speed: int) -> None:
        """Initialize a image list with a speed"""
        super().__init__()
        self._images = image_list
        self.image = self._images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self._dy = speed
        
    def update (self, screen: pygame.Surface, level: int) -> None:
        """Update the background every frame"""
        self.image = self._images[int((level-1)/2)]
        self.rect.top += self._dy
        if self.rect.bottom >= 1200:
            self.rect.top = -600
        

class Ship(pygame.sprite.Sprite):
    # Annotate object-level fields
    _current_image: int
    _speed: int
    _up: bool = False
    _down: bool = False
    _left: bool = False
    _right: bool = False
    
    def __init__(self, image: pygame.Surface, speed: int) -> None:
        """Initialize a image with specified movement speed"""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (225, 500)
        self._speed = speed
        
    def update (self, screen: pygame.Surface) -> None:
        """Boundary checking and movement based on direction booleans"""
        if self._up:
            self.rect.top -= 12
        if self._down:
            self.rect.top += 12
        if self._left:
            self.rect.left -= 12
        if self._right:
            self.rect.left += 12

        if self.rect.right > 500:
            self.rect.left = 1
        if self.rect.left < 0:
            self.rect.right = 500
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 599

    def up (self, screen: pygame.Surface) -> None:
        """Makes the ship move up"""
        self._up = True
    def down (self, screen: pygame.Surface) -> None:
        """Makes the ship move down"""    
        self._down = True
    def left (self, screen: pygame.Surface) -> None:
        """Makes the ship move left"""
        self._left = True
    def right (self, screen: pygame.Surface) -> None:
        """Makes the ship move right"""
        self._right = True
    def stop (self, screen: pygame.Surface, direction: str) -> None:
        """Stops moving the ship"""
        if direction == "up":
            self._up = False
        elif direction == "down":
            self._down = False
        elif direction == "left":
            self._left = False
        elif direction == "right":
            self._right = False

    def stopAll (self, screen: pygame.Surface) -> None:
        """Brings ship to a halt"""
        self._up = False
        self._down = False
        self._left = False
        self._right = False

    def getX (self, screen: pygame.Surface) -> int:
        """Returns the ship's x coordinate"""
        return self.rect.left + 20

    def getY (self, screen: pygame.Surface) -> int:
        """Returns the ship's y coordinate"""
        return self.rect.top

class Beam(pygame.sprite.Sprite):
    # Annotate object-level fields
    def __init__(self, image: pygame.Surface, x: int, y: int) -> None:
        """Initialize an image with a given x and y value"""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        
    def update (self, screen: pygame.Surface) -> None:
        """Moves image up"""
        self.rect.top -= 25

class Mothership(pygame.sprite.Sprite):
    # Annotate object-level fields
    _left: bool
    
    def __init__(self, image: pygame.Surface) -> None:
        """Initialize an image"""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (50,-150)
        self._left = True
        
    def update (self, screen: pygame.Surface) -> None:
        """Moves down till it sits at the top of screen"""
        if self.rect.left < 10:
            self._left = False
        if self.rect.right +50 > 590:
            self._left = True

        if self.rect.top < 0:
            self.rect.top += 1
        if self._left:
            self.rect.left -= 2
        else:
            self.rect.left += 2
                
    
class Asteroid(pygame.sprite.Sprite):
    # Annotate object-level fields
    _dy: int
    _dx: int

    def __init__(self, image: pygame.Surface, x: int, dy: int, dx: int) -> None:
        """Initialize an image with an x, y, and dx value"""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self._dy = dy
        self._dx = dx
        self.rect.topleft = (x,-30)
        
    def update (self, screen: pygame.Surface) -> None:
        """Moves asteroid in the correct direction"""
        self.rect.top += self._dy
        self.rect.left += self._dx

class Coin(pygame.sprite.Sprite):
    # Annotate object-level fields
    def __init__(self, image: pygame.Surface, x: int) -> None:
        """Initialize an image with a random x value"""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,-30)
        
    def update (self, screen: pygame.Surface) -> None:
        """Moves image down"""
        self.rect.top += 7

class Heart(pygame.sprite.Sprite):
    # Annotate object-level fields
    def __init__(self, image: pygame.Surface, x: int) -> None:
        """Initialize an image with a random x value"""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,-30)
        
    def update (self, screen: pygame.Surface) -> None:
        """Moves image down"""
        self.rect.top += 7

def make_window(width: int, height: int,
                caption: str) -> pygame.Surface:
    """Create and return a pygame window"""
    screen: pygame.Surface
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def main() -> None:
    """Main program"""
    # Define constants and annotate variables
    screen: pygame.Surface
    event: pygame.event.Event
    
    game_over: pygame.Surface
    winScreen: pygame.Surface
    continueScreen: pygame.Surface
    continue3: pygame.Surface
    start_screen: pygame.Surface
    coin_image: pygame.Surface
    space: pygame.Surface
    space2: pygame.Surface
    space3: pygame.Surface
    spaceship: pygame.Surface
    asteroid: pygame.Surface
    mothership_image: pygame.Surface
    player_heart: pygame.Surface
    
    user_quit: bool = False
    boss_dead: bool = False
    level: int = 0
    score: int = 0
    coinTrigger: int = 0
    heartTrigger: int = 0
    beam_counter: int = 0
    i: int = 0
    collisions: int = 0
    difficulty: str = "Easy"
    difficultySpeed: int = 15
    difficultyTimer: int = 30
    playerHP: int = 3
    bossHP: int = 15
    timeTracker: int = 0
    space_backgrounds: list
    easyButton = pygame.Rect(100, 300, 300, 50)
    mediumButton = pygame.Rect(100, 400, 300, 50)
    hardButton = pygame.Rect(100, 500, 300, 50)
    color = (50, 0, 255)
    black = (0, 0, 0)
    bossBar = pygame.Rect(50, 10, 400, 15)
    barBack = pygame.Rect(48, 8, 404, 19)
    boss_health_size: int
    full_boss_hp: int
    
    # Make sprites
    background: Background
    mothership: Mothership
    ship: Ship
    asteroid: Asteroid
    coin: Coin
    heart: Heart
    beam: Beam
    heart_group: pygame.sprite.Group = pygame.sprite.Group()
    coin_group: pygame.sprite.Group = pygame.sprite.Group()
    asteroid_group: pygame.sprite.Group = pygame.sprite.Group()
    mothership_group: pygame.sprite.Group = pygame.sprite.Group()
    back: pygame.sprite.Group = pygame.sprite.Group()
    ships: pygame.sprite.Group = pygame.sprite.Group()
    beams: pygame.sprite.Group = pygame.sprite.Group()
    
    # Setup assets.
    screen = make_window(500, 600, "Glactic Defence || Choose Difficulty || Level 0")
    start_screen = pygame.image.load(path.join("images","start.png")).convert_alpha()
    game_over = pygame.image.load("images/gameOver.png").convert_alpha()
    player_heart = pygame.image.load("images/playerHeart.png").convert_alpha()
    coin_image = pygame.image.load("images/coin.png").convert_alpha()
    space = pygame.image.load(path.join("images","space.png")).convert_alpha()
    space2 = pygame.image.load(path.join("images","space2.png")).convert_alpha()
    space3 = pygame.image.load(path.join("images","space3.png")).convert_alpha()
    spaceship = pygame.image.load("images/spaceship.png").convert_alpha()
    rock = pygame.image.load("images/asteroid.png").convert_alpha()
    mothership_image = pygame.image.load("images/mothership.png").convert_alpha()
    beam_image = pygame.image.load("images/beam.png").convert_alpha()
    clock: pygame.time.Clock = pygame.time.Clock()

    space_backgrounds = [space, space2, space3]
    background = Background(space_backgrounds, 7)
    back.add(background)
    ship = Ship(spaceship, 10)
    ships.add(ship)
    asteroid = Asteroid(rock, -10,100, 0)
    mothership = Mothership(mothership_image)
    beam = Beam(beam_image, -10, -10)
    beams.add(beam)
    
    # Load sound
    if pygame.mixer:
        crash = pygame.mixer.Sound(file = path.join("sounds","explode.mp3"))
        win = pygame.mixer.Sound(file = path.join("sounds","win.mp3"))
        healthPickup = pygame.mixer.Sound(file = path.join("sounds","hp.wav"))
        coinPickup = pygame.mixer.Sound(file = path.join("sounds","coin.mp3"))
    
    # Start of game loop
    while not user_quit:
        # Loop for 30 fps
        clock.tick(30)
        # Event loop
        for event in pygame.event.get():
            """START OF EVENT LOOP"""
            # Process a quit choice.
            if event.type == pygame.QUIT:
                user_quit = True

            if event.type == pygame.MOUSEBUTTONUP:
                #Set difficulty based on click coordinates
                if level == 0:
                    mouse = pygame.mouse.get_pos()
                    if pygame.Rect.collidepoint(easyButton, mouse):
                        difficulty = "Easy"
                        difficultySpeed = 5
                        difficultyTimer = 60
                        bossHP = 5
                        full_boss_hp = 5
                    elif pygame.Rect.collidepoint(mediumButton, mouse):
                        difficulty = "Medium"
                        difficultySpeed = 8
                        difficultyTimer = 40
                        bossHP = 15
                        full_boss_hp = 15
                    elif pygame.Rect.collidepoint(hardButton, mouse):
                        difficulty = "Hard"
                        difficultySpeed = 15
                        difficultyTimer = 25
                        bossHP = 35
                        full_boss_hp = 35

            #Move player to next level when enter/return is pressed
            if event.type == pygame.KEYDOWN and level != 1 and level != 3 and level != 5:
                if event.key == pygame.K_RETURN:
                    if level == 0 or level == 2 or level == 4:
                        level += 1
                    else:
                        #Else send to start screen if on W/L screen
                        level = 0
                        score = 0
                    ship.stopAll(screen)
                    asteroid_group.empty()
                    coin_group.empty()
                    heart_group.empty()
                
            #Operate ship based on key event      
            if level == 1 or level == 3 or level == 5:
                if event.type == pygame.KEYDOWN:
                    #Move up, down, left, right
                    if event.key == pygame.K_UP:
                        ship.up(screen)
                    if event.key == pygame.K_DOWN:
                        ship.down(screen)
                    if event.key == pygame.K_LEFT:
                        ship.left(screen)
                    if event.key == pygame.K_RIGHT:
                        ship.right(screen)
                    #Shoot a beam if space is pressed
                    if event.key == pygame.K_SPACE and beam_counter > 7 :
                        beam = Beam(beam_image, ship.getX(screen), ship.getY(screen))
                        beams.add(beam)
                        beam_counter = 0
                if event.type == pygame.KEYUP:
                    #Halt the movement of ship
                    if event.key == pygame.K_UP:
                        ship.stop(screen, "up")
                    if event.key == pygame.K_DOWN:
                        ship.stop(screen, "down")
                    if event.key == pygame.K_LEFT:
                        ship.stop(screen, "left")
                    if event.key == pygame.K_RIGHT:
                        ship.stop(screen, "right")
           
            """END OF EVENT LOOP"""

        # SPAWNS IN ASTEROIDS ON A TIMER
        if level != 0 and i < difficultyTimer/level +2:
            if level == 1 or level == 3 or level == 5:
                if i >= difficultyTimer/level:
                    i=0
                    asteroid = Asteroid(rock, random.randint(0,500),
                                        difficultySpeed, random.randint(-1,1))
                    asteroid_group.add(asteroid)
                    coinTrigger += 1
                    heartTrigger += 1
                else:
                    i+=1
                    beam_counter += 1
                    
        if coinTrigger == 3:
            #Spawn a coin for every 3 asteroids spawned
            coin = Coin(coin_image, random.randint(0,400))
            coin_group.add(coin)
            coinTrigger = 0

        if heartTrigger == 20:
            #Spawn a heart for every 20 asteroids spawned
            heart = Heart(player_heart, random.randint(0,450))
            heart_group.add(heart)
            heartTrigger = 0

            
        """START OF ENTITY COLLISION CHECKING"""
        
        beamHits = pygame.sprite.groupcollide(beams, asteroid_group,
                                               True, True, pygame.sprite.collide_mask)
        if len(beamHits) > collisions:
            #Play sounds
            print("beam hit!")
            
        asteroidHits = pygame.sprite.spritecollide(ship, asteroid_group,
                                                   True, pygame.sprite.collide_mask)
        if len(asteroidHits) > collisions:
            #Play sounds and detract HP if collided
            crash.play()
            crash.fadeout(100)
            playerHP -= 1

        heartCollect = pygame.sprite.spritecollide(ship, heart_group,
                                                   True, pygame.sprite.collide_mask)
        if len(heartCollect) > collisions:
            #Increase the HP by 1
            if playerHP != 3:
                healthPickup.play()
                playerHP += 1

        coinCollect = pygame.sprite.spritecollide(ship, coin_group,
                                            True, pygame.sprite.collide_mask)
        if len(coinCollect) > collisions:
            #Increase the player score
            coinPickup.play()
            score += 1000

        if bossHP == 0:
            bossHits = pygame.sprite.groupcollide(beams, mothership_group,
                                               True, True, pygame.sprite.collide_mask)
            boss_dead = True
            mothership_group.empty()
        else:
            bossHits = pygame.sprite.groupcollide(beams, mothership_group,
                                               True, False, pygame.sprite.collide_mask)
        if len(bossHits) > collisions:
            #Play sounds and detract HP from boss if collided
            print("Boss hit!")
            bossHP -= 1

        if pygame.mixer.get_busy() != True:
            crash.stop()
        """END OF ENTITY COLLISION CHECKING"""
        
        # Update and draw sprites based on screen number
        if level == 7:
            #LEVEL 7 IS GAME OVER SCREEN
            screen.blit(game_over, (0,0))
            playerHP = 3
            
        if level == 1 or level == 3 or level == 5:
            #1,3,5 are the active game screens
            timeTracker += 1
            if timeTracker > level*200:
                #Timer for how long each level lasts
                if level == 3:
                    mothership_group.add(mothership)
                if level == 1 or level == 3:
                    level += 1
                    timeTracker = 0
                    i = 0
                if level == 5 and boss_dead:
                    win.play()
                    boss_dead = False
                    level = 6
                    i = 0
                    timeTracker = 0
                elif level == 5 and boss_dead == False:
                    level = 7
                    i = 0
                    timeTracker = 0
                    mothership_group.empty()
                
                
            #Update relevant assets
            back.update(screen, level)
            ships.update(screen)
            mothership.update(screen)
            asteroid_group.update(screen)
            coin_group.update(screen)
            heart_group.update(screen)
            beams.update(screen)
            score += playerHP * level
            #Draw relevant sprites
            back.draw(screen)
            coin_group.draw(screen)
            heart_group.draw(screen)
            beams.draw(screen)
            ships.draw(screen)
            asteroid_group.draw(screen)
            mothership_group.draw(screen)
            #Draw hearts on screen based on HP
            if playerHP == 3:
                screen.blit(player_heart, (175, 540))
                screen.blit(player_heart, (225, 540))
                screen.blit(player_heart, (275, 540))
            elif playerHP == 2:
                screen.blit(player_heart, (200, 540))
                screen.blit(player_heart, (250, 540))
            elif playerHP == 1:
                screen.blit(player_heart, (225, 540))
            else:
                level = 7
                timeTracker = 0
                i = 0
                playerHP = 3
                mothership_group.empty()
            if boss_dead == False and level == 5:
                pygame.draw.rect(screen, black, barBack)
                boss_health_size = (bossHP/full_boss_hp)*400
                bossBar = pygame.Rect(50, 10, int(boss_health_size), 15)
                pygame.draw.rect(screen, color, bossBar)
                print(int(boss_health_size))

        if level == 0 or level == 2 or level == 4 or level == 6:
            #Code for non game screens
            if level != 0:
                temp: str = "images/continue" + str(int(level/2)) + ".png"
                continueScreen = pygame.image.load(temp).convert_alpha()
                screen.blit(continueScreen, (0,0))
                playerHP = 3
                if difficulty == "Easy":
                    bossHP = 5
                    full_boss_hp = 5
                elif difficulty == "Medium":
                    bossHP = 15
                    full_boss_hp = 15
                else:
                    bossHP = 35
                    full_boss_hp = 35
            else:
                #RUN START SCREEN IF NOT PLAYING GAME
                screen.blit(start_screen, (0,0))
        
        pygame.display.flip()
        if level != 7 and level != 6 and level != 0:
            #Normal updating caption
            pygame.display.set_caption("Glactic Defence || " + difficulty +
                                       " || Level " + str(int((level-1)/2)+1) + " || Score " + str(score))
        elif level == 0:
            #Caption for start screen
            pygame.display.set_caption("Click a difficulty then press enter/return to start!")
        elif level == 7:
            #Caption for a loss
            pygame.display.set_caption("Glactic Defence || " + difficulty +
                                       " || Game OVER || Score " + str(score))
        else:
            #Caption for a win
            pygame.display.set_caption("Glactic Defence || " + difficulty +
                                       " || You WIN || Score " + str(score))
    pygame.quit()
main()
