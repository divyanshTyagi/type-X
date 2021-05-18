import sys
import time
from funcmodule import interact
from colorama import init as colorama_init
from cfonts import render, say
import pygame
colorama_init()



def main():


    output = render('Type X', colors=['red', 'yellow'], align='center')
    print(output)
    time.sleep(2)
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play()
    interact()


if(__name__ == '__main__'):
    main()
