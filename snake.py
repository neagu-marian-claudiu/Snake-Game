import pygame
import random
import time

pygame.init()
width , height = 400,400
game_screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("The Snake...Game in progress...")

x, y = 200,200
delta_x, delta_y = 10,0
food_x,food_y = random.randrange(0,width)//10*10,random.randrange(0,height)//10*10
bomb_x,bomb_y = random.randrange(0,width)//10*10,random.randrange(0,height)//10*10
poison_x,poison_y = random.randrange(0,width)//10*10,random.randrange(0,height)//10*10
body_list = [(x, y)]
clock = pygame.time.Clock()

game_over = False
font = pygame.font.SysFont("bahnschrift",25)

image = pygame.image.load(r"play.png")
image = pygame.transform.scale(image, (50, 50))
bomb_img = pygame.image.load(r"bomb.png")
bomb_img = pygame.transform.scale(bomb_img, (20, 20))
food_img = pygame.image.load(r"food.png")
food_img = pygame.transform.scale(food_img, (20, 20))
poison_img = pygame.image.load(r"poison.png")
poison_img = pygame.transform.scale(poison_img, (20, 20))
pause = False
game_speed = 10
contor = 0
t1 = pygame.time.get_ticks()
t3 = pygame.time.get_ticks()

def snake():
    global x,y,food_x,food_y,game_over,pause,game_speed,contor,bomb_x,bomb_y,t1,t3,poison_x,poison_y
    x = (x + delta_x)%width
    y = (y + delta_y)%height
    if((x,y) in body_list):
        if pause != True:
            game_over = True
            return
    body_list.append((x,y))
    if(food_x == x and food_y == y):
        contor = 0
        while((food_x,food_y) in body_list):
            food_x,food_y = random.randrange(0,width)//10*10,random.randrange(0,height)//10*10
    else:
        del body_list[0]
    if ((len(body_list)-1)*100)%300 == 0 and ((len(body_list)-1)*100) != 0 and contor != 1:
        if game_speed < 20:
            game_speed += 2
            contor = 1
    game_screen.fill(pygame.Color('grey12'))
    score = font.render("Score: "+str((len(body_list)-1)*100),True,(215,118,255))
    game_screen.blit(score,[0,0])
    game_screen.blit(food_img, (food_x, food_y))
    t2 = pygame.time.get_ticks()
    if((food_x == bomb_x and food_x == bomb_y ) or (poison_x == bomb_x and poison_x == bomb_y ) or ((bomb_x,bomb_y) in body_list)):
        bomb_x,bomb_y = random.randrange(0,width)//10*10,random.randrange(0,height)//10*10
    if ((t2-t1) >= 5000) and ((t2-t1) < 10000):
        game_screen.blit(bomb_img, (bomb_x, bomb_y))
        if(abs(bomb_x - x) <= 10 and abs(bomb_y - y) <= 10):
            game_over = True
    if ((t2-t1) > 10000):
        t1 = t2
        bomb_x,bomb_y = random.randrange(0,width)//10*10,random.randrange(0,height)//10*10
    
    t4 = pygame.time.get_ticks()
    if((poison_x == bomb_x and poison_x == bomb_y ) or (poison_x == food_x and poison_x == food_y ) or 
    ((poison_x,poison_y) in body_list)):
        poison_x,poison_y = random.randrange(0,width)//10*10,random.randrange(0,height)//10*10
    if ((t4-t3) >= 3000) and ((t4-t3) < 8000):
        if((len(body_list)-1)*100) > 300:
            game_screen.blit(poison_img, (poison_x, poison_y))
            if(abs(poison_x - x) <= 10 and abs(poison_y - y) <= 10):
                del body_list[0]
                t3 = t4
                game_speed -= 2
                
    if ((t4-t3) > 10000):
        t3 = t4
        poison_x,poison_y = random.randrange(0,width)//10*10,random.randrange(0,height)//10*10
    for (i,j) in body_list:
        pygame.draw.rect(game_screen,(255,255,255),[i,j,10,10])
    pygame.display.update()


while True:
    if(game_over):
        game_screen.fill(pygame.Color('grey12'))
        score = font.render("Score: "+str((len(body_list)-1)*100),True,(215,118,255))
        game_screen.blit(score,[0,0])
        msg = font.render("GAME OVER!",True,(255,255,255))
        game_screen.blit(msg,[width//3,height//3])
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        quit()
    events = pygame.event.get()
    for event in events:
        if(event.type == pygame.QUIT):
            pygame.quit()
            quit()
        if(event.type ==pygame.KEYDOWN):
            if(event.key == pygame.K_LEFT):
                if(delta_x != 10):
                    delta_x = -10
                delta_y = 0
            elif(event.key == pygame.K_RIGHT):
                if(delta_x != -10):
                    delta_x = 10
                delta_y = 0
            elif(event.key == pygame.K_UP):
                if(delta_y != 10):
                    delta_y = -10
                delta_x = 0
            elif(event.key == pygame.K_DOWN):
                if(delta_y != -10):
                    delta_y = 10
                delta_x = 0
            elif event.key == pygame.K_ESCAPE:
                pause = True
            elif event.key == pygame.K_SPACE:
                pause = False
            else:
                continue
            if pause == False:
                snake()
    if(not events):
        if(not pause):
            snake()
        else:
            game_screen.blit(image, (width/2 - 25, height/2 - 25))
    if pause == True:
        game_screen.blit(image, (width/2 - 25, height/2 - 25))
        pygame.display.set_caption('Press SPACE to continue the game')
        pygame.display.update()
    else:
        pygame.display.set_caption("The Snake...Game in progress...")
    clock.tick(game_speed)