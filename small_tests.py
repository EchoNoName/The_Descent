import pygame
import sys

def main():
    pygame.init()

    DISPLAY=pygame.display.set_mode((1600, 900),0,32)

    WHITE=(255,255,255)
    BLUE=(0,0,255)

    DISPLAY.fill(WHITE)

    pygame.draw.rect(DISPLAY,BLUE,(650, 375,300,150))

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

main()