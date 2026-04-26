import pygame
from ayarlar import *

pygame.font.init()

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((KARE, KARE))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()

        if self.text != "empty":
            self.font = pygame.font.SysFont("Georgia", 55, bold=True)

            # taş zemin
            self.image.fill(STONE)

            # dış altın çerçeve
            pygame.draw.rect(self.image, GOLD, (0, 0, KARE, KARE), 5)

            # iç yosunlu taş çerçeve
            pygame.draw.rect(self.image, MOSS_GREEN, (9, 9, KARE - 18, KARE - 18), 3)

            # küçük tapınak süs çizgileri
            pygame.draw.line(self.image, STONE_LIGHT, (18, 18), (KARE - 18, 18), 2)
            pygame.draw.line(self.image, STONE_LIGHT, (18, KARE - 18), (KARE - 18, KARE - 18), 2)

            font_surface = self.font.render(self.text, True, ANCIENT_YELLOW)
            self.font_size = self.font.size(self.text)

            draw_x = (KARE / 2) - self.font_size[0] / 2
            draw_y = (KARE / 2) - self.font_size[1] / 2

            self.image.blit(font_surface, (draw_x, draw_y))

    def update(self):
        self.rect.x = self.x * KARE
        self.rect.y = self.y * KARE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    def right(self):
        return self.rect.x + KARE < OYUN_BOYUTU * KARE

    def left(self):
        return self.rect.x - KARE >= 0

    def up(self):
        return self.rect.y - KARE >= 0

    def down(self):
        return self.rect.y + KARE < OYUN_BOYUTU * KARE


class Menu:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont("Georgia", 30, bold=True)
        text = font.render(self.text, True, ANCIENT_YELLOW)

        # yazı gölgesi
        shadow = font.render(self.text, True, BLACK)
        screen.blit(shadow, (self.x + 2, self.y + 2))
        screen.blit(text, (self.x, self.y))


class Button:
    def __init__(self, x, y, width, height, text, renk, text_rengi):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.renk = renk
        self.text_rengi = text_rengi

        self.font = pygame.font.SysFont("Georgia", 30, bold=True)

    def draw(self, screen):
        # tahta/tapınak butonu
        pygame.draw.rect(screen, WOOD, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, GOLD, (self.x, self.y, self.width, self.height), 4)
        pygame.draw.rect(screen, MOSS_GREEN, (self.x + 6, self.y + 6, self.width - 12, self.height - 12), 2)

        text = self.font.render(self.text, True, ANCIENT_YELLOW)
        self.font_size = self.font.size(self.text)

        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2

        shadow = self.font.render(self.text, True, BLACK)
        screen.blit(shadow, (draw_x + 2, draw_y + 2))
        screen.blit(text, (draw_x, draw_y))

    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height