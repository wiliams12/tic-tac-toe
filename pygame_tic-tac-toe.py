import pygame
from pygame.locals import *
from random import randint
import copy

pygame.init()
pygame.mixer.init()

class App():
    def __init__(self):
        self.running = True
        self.size = 600
        self.screen = pygame.display.set_mode((self.size,self.size))
        self.grid = [[0,0,0],
                     [0,0,0],
                     [0,0,0]]
        pygame.display.set_caption("Tic-Tac-Toe")
        pygame.display.set_icon(pygame.image.load("static\imgs\icon.png"))
        self.heading = Text("Choose: ",300,100,60,(255,255,255))
        self.mixer = pygame.mixer.Sound("static\sound\sound.mp3")
        self.tiles = []
        for i in range(3):
            for q in range(3):
                self.tiles.append(Tile(q,i,600)) 
        self.turn = -1 
        self.current_on = {"x":None,"y":None}      
        
        
        self.settings()
        self.game_loop()
   
    def game_loop(self):
        self.update()
        while self.running:       
            self.change()
            if self.two_players:
                self.turn_player(1)
                self.change()
                self.turn_player(2)
            else:
                self.turn_player(1)
                self.change()
                self.turn_comp()
    
    def change(self):
        win = self.check(self.grid)
        if win == 1:
            symbol = "X"
            self.end_screen(f"' {symbol} ' have won")
        elif win == 2:
            symbol = "O"
            self.end_screen(f"' {symbol} ' have won")     
        self.turn +=1
        if self.turn == 9:
            self.end_screen("It is a draw")
            
    def end_screen(self,text):
            text = Text(text,300,100,70,(255,255,255))
            btn = Button(600,"play again",(300,300))
            while self.running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                    if event.type == MOUSEBUTTONDOWN:
                        if btn.rect.collidepoint(event.pos):
                            App()
                            self.running = False
                            pygame.quit()
                self.screen.fill((0,0,0))
                self.screen.blit(text.txt,text.rect)
                pygame.draw.rect(self.screen,btn.color,btn.rect)
                self.screen.blit(btn.txt.txt,btn.rect)
                pygame.display.flip()
    
    def settings(self):
        btn_2players = Button(600, "2 players", (150,300))
        btn_comp = Button(600,"computer",(450,300))
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()    
                if event.type == MOUSEBUTTONDOWN:
                    if btn_2players.rect.collidepoint(event.pos):
                        self.two_players = True
                        self.running = False
                    elif btn_comp.rect.collidepoint(event.pos):
                        self.two_players = False
                        self.running = False
            self.screen.fill((0,0,0))

            pygame.draw.rect(self.screen,btn_2players.color,btn_2players.rect)
            pygame.draw.rect(self.screen,btn_comp.color,btn_comp.rect)

            self.screen.blit(btn_2players.txt.txt,btn_2players.rect)
            self.screen.blit(btn_comp.txt.txt,btn_comp.rect)
            self.screen.blit(self.heading.txt,self.heading.rect)
            
            pygame.display.flip()
        
        self.running = True

    def valid_move(self,index):
        if self.grid[index[0]][index[1]] == 0:
            return True
        else:
            return False
        
    def turn_player(self,player):
        while True: 
            x,y = self.get_move(600)
            if self.valid_move((int(x),int(y))):
                break
            else:
                print("invalid move")
        self.grid[int(x)][int(y)] = player
        rect = pygame.rect.Rect(self.current_on["x"]*self.size//3,self.current_on["y"]*self.size//3,self.size//3,self.size//3)
        pygame.draw.rect(self.screen,(200,200,200),rect)
        pygame.draw.rect(self.screen,(100,100,100),rect,5,1)                          
        if player == 1:
            Image("static\imgs\cross2.png",600,x,y,self.screen,self.mixer)
        else:
            Image("static\imgs\circle2.png",600,x,y,self.screen,self.mixer)
    


    def check(self,grid):
        for i in range(3):
            if grid[i][0] == grid[i][1] == grid[i][2] != 0:
                return grid[i][i]
            elif grid[0][i] == grid[1][i] == grid[2][i] != 0:
                return grid[i][i]
            elif grid[0][0] == grid[1][1] == grid[2][2] != 0:
                return grid[1][1]
            elif grid[2][0] == grid[1][1] == grid[0][2] != 0:
                return grid[1][1]
        return 0

    def turn_comp(self):
        def funct(global_grid):
            for i in range(3):
                for q in range(3):
                    local_grid = copy.deepcopy(global_grid)
                    local_grid[i][q] = 2
                    if self.check(local_grid) != 0 and self.valid_move((i,q)):
                        return i,q
                    local_grid[i][q] = 1
                    if self.check(local_grid) != 0 and self.valid_move((i,q)):
                        return i,q
            return 0
        
        tile = funct(copy.deepcopy(self.grid))
        if tile:
            x,y = tile
        else:  
            while True:
                x = randint(0,2)
                y = randint(0,2)
                if self.valid_move((x,y)):
                    break
                
        
        
        
        
        
        
        #Already has a move
        self.grid[x][y] = 2
        rect = pygame.rect.Rect(x*self.size//3,y*self.size//3,self.size//3,self.size//3)
        pygame.draw.rect(self.screen,(200,200,200),rect)
        pygame.draw.rect(self.screen,(100,100,100),rect,5,1)                  
        Image("static\imgs\circle2.png",600,x,y,self.screen,self.mixer)

    def update(self):
        self.screen.fill((200,200,200))
        for tile in self.tiles:   
            pygame.draw.rect(self.screen,(100,100,100),tile.rect,5,1)
        pygame.display.flip()
    
    def get_move(self,size):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()                              
                elif event.type == MOUSEMOTION:
                    for tile in self.tiles:
                        if tile.rect.collidepoint(event.pos):
                            self.current_tile(tile)    
                elif event.type == MOUSEBUTTONDOWN: 
                    for tile in self.tiles:
                         if tile.rect.collidepoint(event.pos):
                             rect = tile
                             self.running = False
        x,y = rect.rect.center
        x = x//(size//3)
        y = y//(size//3)
        self.running = True
        return x,y
    
    def current_tile(self,tile):
        x = tile.rect.left//(self.size//3)
        y = tile.rect.top//(self.size//3)
        if self.grid[x][y] == 0:
            pygame.draw.rect(self.screen,(170,170,170),tile.rect)
            pygame.draw.rect(self.screen,(70,70,70),tile.rect,5,1)
            pygame.display.flip()
        try:    
            if (self.current_on["x"] != x or self.current_on["y"] != y) and self.grid[self.current_on["x"]][self.current_on["y"]] == 0:    
                rect = pygame.rect.Rect(self.current_on["x"]*self.size//3,self.current_on["y"]*self.size//3,self.size//3,self.size//3)
                pygame.draw.rect(self.screen,(200,200,200),rect)
                pygame.draw.rect(self.screen,(100,100,100),rect,5,1)            
                pygame.display.flip()
        except TypeError:
            pass
        self.current_on["x"] = x
        self.current_on["y"] = y


         


class Text():
    def __init__(self,text,x,y,size,color):
        pygame.font.init()
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.font = pygame.font.SysFont('swis721wgl4',self.size)
        self.txt = self.font.render(self.text,True,self.color)
        self.rect = self.txt.get_rect()
        self.rect.center = (self.x,self.y) 

class Button():
    def __init__(self,size,text,pos):
        self.size = (3*size//8,size//8)
        self.pos = pos
        self.text = text
        self.txt = Text(text,*self.pos,size//16,(0,0,0))
        self.rect = pygame.rect.Rect(0,0,*self.size)
        self.rect.center = self.pos
        self.color = (255,255,255)


class Tile():
    def __init__(self,x,y,size_screen):
        self.size = size_screen//3
        self.rect = pygame.rect.Rect(0,0,self.size,self.size)
        self.rect.left = x*self.size
        self.rect.top = y*self.size

class Image():
    def __init__(self,path,size,x,y,screen,mixer):
        self.img = pygame.image.load(path)
        self.rect = self.img.get_rect()
        self.rect.left = x*size//3
        self.rect.top = y*size//3
        self.draw_self(screen,mixer)
    
    def draw_self(self,screen,mixer):   
        screen.blit(self.img,self.rect)
        mixer.play(0)
        pygame.time.wait(100)
        pygame.display.flip()           


App()
pygame.quit()