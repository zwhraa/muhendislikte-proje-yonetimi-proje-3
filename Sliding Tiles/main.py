import pygame
import time
import random
from sprite import *
from ayarlar import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen =pygame.display.set_mode((WIDTH, HEIGHT)) 
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.karistir_time = 0
        self.start_karistir = False
        self.old_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        scores = self.get_best_scores()
        self.best_score= float(scores[0]) if scores else 9999
        

    def get_best_scores(self):
        with open("slidingtiles_best_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores
    
    def save_scores(self):
        with open("slidingtiles_best_score.txt", "w")as file:
            file.write(str("%.3\n" % self.best_score_kolay))
            file.write(str("%.3\n" % self.best_score_orta))
            file.write(str("%.3\n" % self.best_score_zor))


    def oyun_kur(self):
        grid = []
        number = 1

        for x in range(OYUN_BOYUTU):
            grid.append([])
            for y in range(OYUN_BOYUTU):
                grid[x].append(number)
                number += 1   #
        grid[-1][-1] = 0
        print(grid) 
        return grid
   
    #grid[[(x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1))] for y in range(GAME_SIZE)]
    #    grid[-1][-1]
    #    return grid

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

        if self.old_choice == "right":
            muhtemel_hareketler.remove("left") if "left" in muhtemel_hareketler else muhtemel_hareketler
        if self.old_choice == "left":
            muhtemel_hareketler.remove("right") if "right" in muhtemel_hareketler else muhtemel_hareketler
        if self.old_choice == "up":
            muhtemel_hareketler.remove("down") if "down" in muhtemel_hareketler else muhtemel_hareketler
        if self.old_choice == "down":
            muhtemel_hareketler.remove("up") if "up" in muhtemel_hareketler else muhtemel_hareketler

        choice = random.choice(muhtemel_hareketler)
        self.old_choice = choice
        if choice == "right" and col + 1 < OYUN_BOYUTU:
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
        elif choice == "left" and col - 1 >= 0:
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
        elif choice == "up" and row - 1 >= 0:
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
        elif choice == "down" and row + 1 < OYUN_BOYUTU:
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
        self.buttons_list.append(Button(775, 100, 200, 50, "Karıştır", WHITE, BLACK))
        self.buttons_list.append(Button(775, 170, 200, 50, "Reset", WHITE, BLACK))
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
                if self.best_score > 0:
                    self.best_score = self.elapsed_time if self.elapsed_time < self.best_score else self.best_score
                else: 
                    self.best_score = self.elapsed_time
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

    def draw_grid(self):
        for row in range(-1, OYUN_BOYUTU * KARE, KARE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, OYUN_BOYUTU * KARE))
        for col in range(-1, OYUN_BOYUTU * KARE, KARE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (OYUN_BOYUTU*KARE, col))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        
        for button in self.buttons_list:
            button.draw(self.screen)
        
        Menu(710,380,"Best Score: %.3f " % self.elapsed_time).draw(self.screen)
        Menu(825, 35, "%.2f" % self.elapsed_time).draw(self.screen)
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
                            print(tile.text)
                            
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
                                #x, y = y, x
                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
                                #x, y = y, x
                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
                                #x, y = y, x
                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
                                #x, y = y, x
                            self.draw_tiles() 
               
                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        print(button.text) 
                        if button.text == "Karıştır":
                            self.karistir_time = 0
                            self.start_karistir = True
                            
                        if button.text == "Reset":   
                            self.new()  
            
game = Game()
while True:
    game.new()
    game.run()