#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.image
from pygame import font, surface, rect

from code.const import COLOR_PINK, SCREEN_WIDTH, COLOR_PURPLE, COLOR_WHITE, MENU_SELECTION


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.surface = pygame.image.load('./asset/MenuBGimg.png')  # loading the image
        self.rect = self.surface.get_rect()  # surface(img) getting a rectangle and specifying its coordinates

    def run(self, ):
        menu_selection = 0
        while True:
            self.screen.blit(source=self.surface, dest=self.rect)  # drawing the img inside the rectangle

            for i, item in enumerate(MENU_SELECTION):  # for text color and selection color
                color = COLOR_WHITE if i == menu_selection else COLOR_PINK
                self.menu_text(40, item, color, ((SCREEN_WIDTH / 2), 290 + 40 * i))
            for event in pygame.event.get():  # checking for events
                if event.type == pygame.QUIT:  # closing the screen
                    pygame.quit()
                    quit()  # end
                if event.type == pygame.KEYDOWN:  # for menu selection while pressing the key
                    if event.key == pygame.K_DOWN:  # key down
                        menu_selection = (menu_selection + 1) % len(MENU_SELECTION)
                    elif event.key == pygame.K_RETURN:  # enter
                        return MENU_SELECTION[menu_selection]

            pygame.display.flip()  # loads into the screen

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_position: tuple):
        text_surface = pygame.font.SysFont("System", text_size).render(text, True, text_color)
        text_surface.set_alpha(255)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_position))
