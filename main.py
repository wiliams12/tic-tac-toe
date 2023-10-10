from random import randint

class App():
    def __init__(self):
        self.running = True
        self.settings()
        self.grid = [[0,0,0],
                     [0,0,0],
                     [0,0,0]]
        self.game_loop()
   
    def game_loop(self):
        while self.running:
            if self.two_players:
                self.turn_player(1)
                self.change()
                self.turn_player(2)
            else:
                self.turn_player(1)
                self.change()
                self.turn_comp_random()
            self.change()
    
    def change(self):
        win = self.check()
        if win:
            print(f"player {win} won.")
            self.running = False
        self.update()

    def settings(self):
        while self.running:    
            str_input = input("Two players? Y/N: ")
            if  str_input == "Y":
                self.two_players = True
                self.running = False
            elif str_input == "N":
                self.two_players = False
                self.running = False
            else:
                print("invalid input")
        self.running = True

    def valid_move(self,index):
        if self.grid[index[0]][index[1]] == 0:
            return True
        else:
            return False
        
    def turn_player(self,player):
        while True:
            x,y = input("Please provide an input of cordinates in the grid seperated by comma. ").split(",")
            if self.valid_move((int(x),int(y))):
                break
            else:
                print("invalid move")
        self.grid[int(x)][int(y)] = player

    def check(self):
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != 0:
                return self.grid[i][i]
            elif self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != 0:
                return self.grid[i][i]
            elif self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != 0:
                return self.grid[1][1]
            elif self.grid[2][0] == self.grid[1][1] == self.grid[0][2] != 0:
                return self.grid[1][1]
        return 0

    def turn_comp_random(self):
        while True:
            x = randint(0,2)
            y = randint(0,2)
            if self.valid_move((x,y)):
                break
        self.grid[x][y] = 2
        

    def update(self):
        for i in range(3):
            for q in range(3):
                print(self.grid[i][q],end=None)
            print("\n")


App()