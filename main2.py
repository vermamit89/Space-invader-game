import pygame  
import random 
import math

# Initialising pygame
pygame.init()

# Screen Display
screen=pygame.display.set_mode((800,600))

#Title and logo 
Title=pygame.display.set_caption("Space Invader Game")
logo= pygame.image.load("logo.png")
pygame.display.set_icon(logo)

#Background image - load
SB= pygame.image.load("SpaceBackground.png")

#Player
playerImg=pygame.image.load("spaceship.png")
playerX=380
playerY=480
player_changeX=0

#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]

no_of_enemy=5

for i in range(no_of_enemy):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(10)
    enemyY_change.append(25)

#Bullet Image
bulletImg= pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=20
bullet_state="ready"


def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+20,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance< 25:
        return True
    else:
        return False

#Score
score_value=0
font=pygame.font.Font('Candyshop.ttf',32)
textX=10
textY=10

def show_score(x,y):
    score=font.render("score : "+ str(score_value),True,(0,255,255))
    screen.blit(score,(x,y))

over_font=pygame.font.Font('Candyshop.ttf',72)
#Game over function
def game_over():
    over_text=font.render("GAME OVER  ",True,(0,255,255))
    screen.blit(over_text,(300,300))

# Game Loop
running= True
while running:

    #Background Colour
    Backgroud_colour=screen.fill((0,0,0))

    #Background image-draw
    screen.blit(SB,(0,0))
 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        #check keystroke is pressed
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                player_changeX=-10
            if event.key==pygame.K_RIGHT:
                player_changeX=10
            if event.key==pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or  event.key==pygame.K_RIGHT:
                player_changeX=0

    playerX+=player_changeX
    if playerX<0:
        playerX=0
    elif playerX>=736:
        playerX=736
 
     #enemy movement
    for i in range(no_of_enemy):
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=10
            enemyY[i]+= enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-10
            enemyY[i]+= enemyY_change[i]

        #Game Over
        if enemyY[i]>430:
            for j in range(no_of_enemy):
                enemyY[j]=2000
            game_over()
            break

    # Collision
        collision=iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY=480
            bullet_state="ready"
            score_value+=1
            
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)

    #bulletMovement
    if bulletY<0:
        bulletY=480
        bullet_state="ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()