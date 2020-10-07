import sys
import random
import pygame


def finish():
    pygame.quit()
    sys.exit()

H = 500
W = 500

SIZE_A = 30
SIZE_B = 90

display = pygame.display.set_mode((W, H))

FPS = 20
fpsClock = pygame.time.Clock()

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish()

main()





