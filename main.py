import pygame
import os
pygame.font.init() # font thing
pygame.mixer.init() # sound thing

WIDTH,HEIGHT = 1800, 1050 # game window dimensions
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # sets width and height of the display
pygame.display.set_caption("Somalian version of Space Invaders") # caption

BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

SPACE_BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),(WIDTH, HEIGHT)) # loads space background

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) # defines the border

BULLET_SOUND_HIT = pygame.mixer.Sound(os.path.join('Assets', 'hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'fire.mp3'))

HEALTH_FONT = pygame.font.SysFont('helvetica', 40)
WINNING_FONT = pygame.font.SysFont('helvetica',100)

FPS = 60 #fps cap (keep at 60)
vel = 10 # velocity of spaceship
BULLET_VELOCITY = 20
MAX_BULLETS = 5 # max bullets
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 64, 64 # spaceship dimensions

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'Yellow.png')) # loads the images
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270) # numbers on the end are degree rotations
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'Red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) # numbers on the end are degree rotations

SPACESHIP_WIDTH, SPACESHIP_HEIGHT

# DRAW WINDOW FUNCTION -----------------------------------------------------------------------------------

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health): #draw the window, this function is for drawing shit
    WIN.blit(SPACE_BG, (0,0))
    # WIN.fill((255,255,255))
    pygame.draw.rect(WIN, (255,255,255), BORDER) # goofy ahh drawing method

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, (255,255,255)) # Defines the red health text by rendering the HEALTH_FONT and converting the health into a string
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, (255,255,255)) # same thing for yellow health
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10)) # Draws the health by getting the width of the window, subtracting the width of the red health text and adding padding
    WIN.blit(yellow_health_text, (10, 10)) # Yellow health text

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #draw yellow
    WIN.blit(RED_SPACESHIP, (red.x, red.y))  #draw red

    

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet) # draws a red bullet for every bullet in red bullet array

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet) # draws a YELLOW bullet for every bullet in YELLOW bullet array

    pygame.display.update() #Updates the game display

# END OF DRAW WINDOW FUNCTION -----------------------------------------------------------------------------

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - vel > 0: #left
            yellow.x -= vel # apparently you can't do switch statements with this or i'm just an idiot 
    if keys_pressed[pygame.K_d] and yellow.x + vel + yellow.width < BORDER.x: #right and checks border stuff
            yellow.x += vel
    if keys_pressed[pygame.K_w] and yellow.y - vel > 0: #up
            yellow.y -= vel 
    if keys_pressed[pygame.K_s] and yellow.y + vel + yellow.height < HEIGHT: #down
            yellow.y += vel

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - vel > BORDER.x + BORDER.width: #left
            red.x -= vel # apparently you can't do switch statements with this or i'm just an idiot 
    if keys_pressed[pygame.K_RIGHT] and red.x + vel + red.width < WIDTH: #right
            red.x += vel
    if keys_pressed[pygame.K_UP] and red.y - vel > 0: #up
            red.y -= vel 
    if keys_pressed[pygame.K_DOWN] and red.y + vel + red.height < HEIGHT: #down
            red.y += vel

# BULLET HANDLER #############################################################################################################################
def handle_bullets(yellow_bullets, red_bullets, yellow, red): # bullet handler function
    for bullet in yellow_bullets: # for every bullet in yellow bullet array
        bullet.x += BULLET_VELOCITY # add velocity to bullet x
        if red.colliderect(bullet): # if red collides with bullet
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet) # remove a bullet from yellow
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet) # remove bullet


    for bullet in red_bullets: # same shit but for yellow
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet) # remove bullet

# END OF BULLET HANDLER ####################################################################################################################
        
def drawWinnerText(text):
    draw_text = WINNING_FONT.render(text, 1, (255,255,255)) # defines the draw text
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2)) # blits the draw text in the middle of the screen
    pygame.display.update()
    pygame.time.delay(5000)


# MAIN FUNCTION ------------------------------------------------------------------------------------------------    

def main():

    red = pygame.Rect(1400, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # creates the red object aka the spaceship 
    yellow = pygame.Rect(10, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # same thing but yellow

    red_bullets = []
    yellow_bullets = []

    red_health = 3
    yellow_health = 3


    clock = pygame.time.Clock() # FPS cap

    run = True
    while run: # loop
        clock.tick(FPS) #caps the fps
        for event in pygame.event.get(): # for every event in pygame
            if event.type == pygame.QUIT: #if the event is quit
                run = False # stop running the game
                pygame.quit() 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5) #creates bullet
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS: #if press right ctrl and length of red bullet array is under max bullet count
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5) #creates bullet
                    red_bullets.append(bullet) # add a bullet to red bullet array
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT: # if red gets hit
                red_health -= 1 # -1 health
                BULLET_SOUND_HIT.play()

            if event.type == YELLOW_HIT: # same 4 yellow
                yellow_health -= 1
                BULLET_SOUND_HIT.play()

        winner_text = "" # winner text is blank
        if red_health == 0:
            winner_text = "Yellow Wins!"

        if yellow_health == 0: # self explanatory
            winner_text = "Red wins!"

        if winner_text != "":
            drawWinnerText(winner_text) # draw the winner text 
            main() # breaks

        keys_pressed = pygame.key.get_pressed() # defines key pressed variable which is used to check for keys pressed
        yellow_handle_movement(keys_pressed, yellow) # calls yellow movement handler
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red) # calls handle_bullets while passing 4 params
    
        draw_window(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health) #draws the window of the game with the red and yellow spaceships

    main() # idk

# END OF MAIN ------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__": #checks to see if the class name is main
    main()