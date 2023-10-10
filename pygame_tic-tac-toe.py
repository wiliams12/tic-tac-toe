import pygame
from pygame.locals import *
from random import randint
import copy


pygame.init()
pygame.mixer.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
SIZE = 600


class App():
    def __init__(self):
        """
        Setting up pygame. Creating tiles.
        """
        self.running = True
        self.size = SIZE
        self.screen = pygame.display.set_mode((self.size,self.size))
        self.grid = [[0,0,0],
                     [0,0,0],
                     [0,0,0]]
        pygame.display.set_caption("Tic-Tac-Toe")
        pygame.display.set_icon(pygame.image.load("static\imgs\icon.png"))
        self.mixer = pygame.mixer.Sound("static\sound\sound.mp3")
        self.tiles = []
        for i in range(3):
            for q in range(3):
                self.tiles.append(Tile(q,i,600)) 
        self.turn = 0 
        self.current_on = [None, None]     
   

    def game_loop(self):
        """
        The game loop. Doesn't need to be broken out of because end_check() starts a nested App() when the quiting condition is fulfilled
        """
        self.set_up()
        while self.running:       
            if self.two_players:
                self.turn_player(1)
                self.end_check()
                self.turn_player(2)
                self.end_check()
            else:
                self.turn_player(1)
                self.end_check()
                self.turn_comp()
                self.end_check()


    def end_check(self):
        """
        Evaluates the result of check()
        """
        win = self.check(self.grid)
        if win == 1:
            symbol = "X"
            self.end_screen(f"'{symbol}' have won")
        elif win == 2:
            symbol = "O"
            self.end_screen(f"'{symbol}' have won")     
        self.turn +=1
        if self.turn == 9:
            self.end_screen("It is a draw")



    def end_screen(self,text):
            """
            An end screen giving player an option to play again. The play again option runs another App(). The current App() terminates once the nested App() ends.
            """
            pygame.time.delay(500)
            text = Text(text,300,100,70,WHITE)
            btn = Button(600,"play again",(300,300))
            while self.running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                    if event.type == MOUSEBUTTONDOWN:
                        if btn.rect.collidepoint(event.pos):
                            app = App()
                            app.settings()
                            app.game_loop()
                            self.running = False
                            pygame.quit()
                self.screen.fill(BLACK)
                self.screen.blit(text.txt,text.rect)
                pygame.draw.rect(self.screen,btn.color,btn.rect)
                self.screen.blit(btn.txt.txt,btn.rect)
                pygame.display.flip()
    

    def settings(self):
        """
        Setting the game mode. Either 2 players or playing against a computer is possible
        """
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
            self.screen.fill(BLACK)

            pygame.draw.rect(self.screen,btn_2players.color,btn_2players.rect)
            pygame.draw.rect(self.screen,btn_comp.color,btn_comp.rect)

            heading = Text("Choose: ",300,100,60,WHITE)

            self.screen.blit(btn_2players.txt.txt,btn_2players.rect)
            self.screen.blit(btn_comp.txt.txt,btn_comp.rect)
            self.screen.blit(heading.txt,heading.rect)
            
            pygame.display.flip()
        
        self.running = True


    def valid_move(self,index):
        """
        Checks whether the given move is valid (The tile is yet to be occupied)
        """
        if self.grid[index[0]][index[1]] == 0:
            return True
        else:
            return False


    def turn_player(self,player):
        """
        Player's turn. Gets a move from the user and displays it on screen.
        """
        while True: 
            x,y = self.get_move(600)
            if self.valid_move((int(x),int(y))):
                break
            else:
                print("invalid move")
        self.grid[int(x)][int(y)] = player
        rect = pygame.rect.Rect(self.current_on[0]*self.size//3,self.current_on[1]*self.size//3,self.size//3,self.size//3)
        pygame.draw.rect(self.screen,(200,200,200),rect)
        pygame.draw.rect(self.screen,(100,100,100),rect,5,1)                          
        if player == 1:
            Image("static\imgs\cross2.png",600,x,y,self.screen,self.mixer)
        else:
            Image("static\imgs\circle2.png",600,x,y,self.screen,self.mixer)
    

    def check(self,grid):
        """
        Checks whether any of the winning/losing conditions has beee met.
        """
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


    def comp_move(self, global_grid):
            """
            Firstly it checks the board for an option to win. If none is found, it tries to prevent the oponent from winning. Returns false if no important move can be made.
            """
            for i in range(3):
                for q in range(3):
                    local_grid = copy.deepcopy(global_grid)
                    local_grid[i][q] = 2
                    if self.check(local_grid) != 0 and self.valid_move((i,q)):
                        return i,q
            for i in range(3):
                for q in range(3):
                    local_grid = copy.deepcopy(global_grid)
                    local_grid[i][q] = 1
                    if self.check(local_grid) != 0 and self.valid_move((i,q)):
                        return i,q
            return False
    

    def turn_comp(self):
        """
        Calls comp_move(). If it return false, it generates random placement. Finally, displays it on the screen.
        """
        tile = self.comp_move(copy.deepcopy(self.grid))
        if tile:
            x,y = tile
        else:  
            while True:
                x = randint(0,2)
                y = randint(0,2)
                if self.valid_move((x,y)):
                    break       
        self.grid[x][y] = 2
        rect = pygame.rect.Rect(x*self.size//3,y*self.size//3,self.size//3,self.size//3)
        pygame.draw.rect(self.screen,(200,200,200),rect)
        pygame.draw.rect(self.screen,(100,100,100),rect,5,1)                  
        Image("static\imgs\circle2.png",600,x,y,self.screen,self.mixer)


    def set_up(self):
        """
        Displays the initial grid which will be later filled.
        """
        self.screen.fill((200,200,200))
        for tile in self.tiles:   
            pygame.draw.rect(self.screen,(100,100,100),tile.rect,5,1)
        pygame.display.flip()
    

    def get_move(self,size):
        """
        A loop waiting for an user input.
        """
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
        """
        Highlights the tile, mouse is currently on. The try block then gives the tile it's original colour.
        """
        x = tile.rect.left//(self.size//3)
        y = tile.rect.top//(self.size//3)
        if self.grid[x][y] == 0:
            pygame.draw.rect(self.screen,(170,170,170),tile.rect)
            pygame.draw.rect(self.screen,(70,70,70),tile.rect,5,1)
            pygame.display.flip()
        try:    
            if (self.current_on[0] != x or self.current_on[1] != y) and self.grid[self.current_on[0]][self.current_on[1]] == 0:    
                rect = pygame.rect.Rect(self.current_on[0]*self.size//3,self.current_on[1]*self.size//3,self.size//3,self.size//3)
                pygame.draw.rect(self.screen,(200,200,200),rect)
                pygame.draw.rect(self.screen,(100,100,100),rect,5,1)            
                pygame.display.flip()
        except TypeError:
            pass
        self.current_on[0] = x
        self.current_on[1] = y


         
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
        self.txt = Text(text,*self.pos,size//16,BLACK)
        self.rect = pygame.rect.Rect(0,0,*self.size)
        self.rect.center = self.pos
        self.color = WHITE



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
        screen.blit(self.img,self.rect)
        mixer.play(0)
        pygame.time.wait(100)
        pygame.display.flip()           


if __name__ == "__main__":  
    app = App()
    app.settings()
    app.game_loop()
    pygame.quit()