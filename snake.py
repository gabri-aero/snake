import pygame
import random
import time
pygame.font.init()

class Box:

    def __init__(self, posX, posY, width, height):
        self.x = posX
        self.y = posY
        self.width = width
        self.height = height
        self.status = 'EMPTY'
        self.color = (0, 0, 0)
        self.time = 0

    def display(self, win, length):
        if self.status == 'SNAKE': 
            self.color = (0, 255, 0)
            self.mode = 0
            self.time -= 1
            if self.time < 0: self.status = 'EMPTY'
            if self.time == length - 1: self.color = (0, 100, 0)
        if self.status == 'EMPTY': 
            self.color, self.mode = (100, 100, 100), 1
            pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), 0)
        if self.status == 'FOOD': self.color, self.mode = (255, 0, 0), 0
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), self.mode)

    def snake_place(self, snake, board):
        if self.status == 'FOOD': 
            snake.length += 1
            board.boxes[random.randint(0, board.rows - 1)][random.randint(0, board.cols -1)].status = 'FOOD'
        self.time = snake.length
        self.status = 'SNAKE'



class Board:

    def __init__(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.box_width = self.width / self.cols
        self.box_height = self.height / self.rows
        self.boxes = [[Box(self.box_width * j, self.box_height * i, self.box_width, self.box_height) for j in range(self.cols)] for i in range(self.rows)]

    def display(self, win, length):
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].display(win, length)

class Snake:
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.x = random.randint(0, self.rows-1)
        self.y = random.randint(0, self.cols-1)
        self.dir = ['UP', 'RIGHT', 'DOWN', 'LEFT'][random.randint(0,3)]
        self.width = width
        self.height = height
        self.length = 1

    def move(self, board):
        if self.dir == 'UP': self.y -= 1
        if self.dir == 'DOWN': self.y += 1
        if self.dir == 'RIGHT': self.x += 1
        if self.dir == 'LEFT': self.x -=1
        #adjust coordinates
        if self.x < 0: self.x += self.cols
        if self.x >= self.cols: self.x -= self.cols
        if self.y < 0: self.y += self.rows
        if self.y >= self.rows: self.y -= self.rows

        board.boxes[self.y][self.x].snake_place(self, board)

def checkCrash(board, snake):
    return True if board.boxes[snake.y][snake.x].color == (0, 255, 0) else False

def finished(win):
    fnt = pygame.font.SysFont("comicsans", width // 5)
    text = fnt.render('GAME OVER', 1, (255, 255, 255))
    win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
    run = False
 
width = 150
height = 150
rows = 10
cols = 10

def main():
    win = pygame.display.set_mode((width, height))
    board = Board(width, height, rows, cols)
    snake = Snake(rows, cols, width, height)
    win.fill((0, 0, 0))

    prevtime = 0
    delay = 0.15

    run = True

    board.boxes[8][4].status = 'FOOD'

    while run:
        print(run)
        if(round(time.time(), 1) >= prevtime + delay):
            prevtime = round(time.time(), 1)
            board.display(win, snake.length)
            snake.move(board)
            pygame.display.update()
            if checkCrash(board, snake): finished(win); run = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and snake.dir != 'UP': snake.dir = 'DOWN'
                if event.key == pygame.K_UP and snake.dir != 'DOWN': snake.dir = 'UP'
                if event.key == pygame.K_LEFT and snake.dir != 'RIGHT': snake.dir = 'LEFT'
                if event.key == pygame.K_RIGHT and snake.dir != 'LEFT': snake.dir = 'RIGHT'
        
main()

        


