import pygame
from network import network
import time
import threading
import sys
pygame.init()
pygame.font.init()

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

def message_display(text):
    mytext = pygame.font.Font("freesansbold.ttf", 40)
    TextSurf, TextRect = text_objects(text, mytext)
    TextRect.center = (500 / 2, 500 / 2)
    win.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(3)


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

keepthread=True
anotherc = 0
def to_receive_data(n, p, p2):
    while keepthread:
        try:
            x = n.receivedata()
            print("received: ", x)
            if type(x) is list:
                p2[:] = x
            elif isinstance(x, str):
                if x == "dead":
                    p.life_status = "dead"
                    anotherc=1
                else:
                    str1 = x.split(":")
                    p.foodx = int(str1[0])
                    p.foody = int(str1[1])
                    p.eatenfood = False
        except:
            pass
        if keepthread==False:
            break


def redrawWindow(win, player, otherplayers):
    win.fill((255, 255, 255))
    if player.life_status == "alive":
        player.draw(win)
    for i in range(len(otherplayers)):
        if otherplayers[i].life_status == "alive":
            otherplayers[i].draw(win)
    pygame.display.update()

p2 = []

def main():
    n = network()
    p = n.get_p()
    run = True
    clock = pygame.time.Clock()
    ithread = threading.Thread(target=to_receive_data, args=(n, p, p2))
    ithread.daemon = True
    ithread.start()
    counter=0
    while run:
        try:
            n.send(p)
        except:
            pass
        clock.tick(25)
        if p.life_status=="alive":
            p.keymove()
            p.move()
            p.snakecollision(p2)
            if (p.check_collision() == 1):
                p.gameover()
        if p.life_status=="dead" and counter == 0 and anotherc==0:
            keepthread=False
            print("passing for the first time")
            counter += 1
        elif counter==1:
            print("breaking")
            message_display("you crashed")
            run=False
        redrawWindow(win, p, p2)
    pygame.quit()
    sys.exit()

main()
