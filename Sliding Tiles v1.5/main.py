import pygame
import time
import random
from sprite import *
from ayarlar import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        self.karistir_time = 0
        self.start_karistir = False
        self.old_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0

        self.difficulty = "easy"
        self.oyun_boyutu = 3

        self.best_scores = self.get_best_scores()
        self.best_score = self.best_scores[self.difficulty]

    def get_best_scores(self):
        scores = {
            "easy": None,
            "medium": None,
            "hard": None
        }

        try:
            with open("slidingtiles_best_score.txt", "r") as file:
                lines = file.read().splitlines()

            for line in lines:
                if "=" in line:
                    mode, score = line.split("=")
                    if mode in scores and score.strip() != "":
                        scores[mode] = float(score)
                else:
                    if line.strip() != "":
                        scores["easy"] = float(line)

        except:
            pass

        return scores

    def save_scores(self):
        with open("slidingtiles_best_score.txt", "w") as file:
            for mode in ["easy", "medium", "hard"]:
                if self.best_scores[mode] is None:
                    file.write(mode + "=\n")
                else:
                    file.write("%s=%.3f\n" % (mode, self.best_scores[mode]))

    def set_difficulty(self, mode):
        self.difficulty = mode

        if mode == "easy":
            self.oyun_boyutu = 3
        elif mode == "medium":
            self.oyun_boyutu = 4
        elif mode == "hard":
            self.oyun_boyutu = 5

        self.best_score = self.best_scores[self.difficulty]
        self.new()

    def oyun_kur(self):
        grid = []
        number = 1

        for x in range(self.oyun_boyutu):
            grid.append([])
            for y in range(self.oyun_boyutu):
                grid[x].append(number)
                number += 1

        grid[-1][-1] = 0
        return grid

    def karistir(self):
        muhtemel_hareketler = []

        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        muhtemel_hareketler.append("right")
                    if tile.left():
                        muhtemel_hareketler.append("left")
                    if tile.up():
                        muhtemel_hareketler.append("up")
                    if tile.down():
                        muhtemel_hareketler.append("down")
                    break

            if len(muhtemel_hareketler) > 0:
                break

        choice = random.choice(muhtemel_hareketler)

        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

    def draw_tiles(self):
        self.tiles = []

        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])

            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.oyun_kur()
        self.tiles_grid_completed = self.oyun_kur()

        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False

        self.buttons_list = []

        # ÜST: Start / Reset
        self.buttons_list.append(Button(775, 120, 200, 50, "Start", WHITE, BLACK))
        self.buttons_list.append(Button(775, 185, 200, 50, "Reset", WHITE, BLACK))

        # ORTA: Mod ayarlama
        self.buttons_list.append(Button(780, 310, 180, 40, "Kolay", WHITE, BLACK))
        self.buttons_list.append(Button(780, 355, 180, 40, "Orta", WHITE, BLACK))
        self.buttons_list.append(Button(780, 400, 180, 40, "Zor", WHITE, BLACK))

        self.draw_tiles()

    def run(self):
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):

        if self.start_game:

            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False

                if self.best_scores[self.difficulty] is None or self.elapsed_time < self.best_scores[self.difficulty]:
                    self.best_scores[self.difficulty] = self.elapsed_time
                    self.best_score = self.best_scores[self.difficulty]
                    self.save_scores()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False

            self.elapsed_time = time.time() - self.timer

        if self.start_karistir:
            self.karistir()
            self.draw_tiles()

            self.karistir_time += 1

            if self.karistir_time > 120:
                self.start_karistir = False
                self.start_game = True
                self.start_timer = True

        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BGCOLOUR)

        self.all_sprites.draw(self.screen)

        for button in self.buttons_list:
            button.draw(self.screen)

        if self.difficulty == "easy":
            mod_yazisi = "Kolay"
        elif self.difficulty == "medium":
            mod_yazisi = "Orta"
        else:
            mod_yazisi = "Zor"

        if self.best_score is None:
            best_yazisi = "Best Score: Yok"
        else:
            best_yazisi = "Best Score: %.3f" % self.best_score

        Menu(825, 35, "%.2f" % self.elapsed_time).draw(self.screen)

        
        Menu(805, 465, mod_yazisi).draw(self.screen)
        Menu(755, 520, best_yazisi).draw(self.screen)

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):

                        if tile.click(mouse_x, mouse_y):

                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()

                for button in self.buttons_list:

                    if button.click(mouse_x, mouse_y):

                        if button.text == "Kolay":
                            self.set_difficulty("easy")

                        elif button.text == "Orta":
                            self.set_difficulty("medium")

                        elif button.text == "Zor":
                            self.set_difficulty("hard")

                        elif button.text == "Start":
                            self.karistir_time = 0
                            self.start_karistir = True

                        elif button.text == "Reset":
                            self.new()


game = Game()

while True:
    game.new()
    game.run()