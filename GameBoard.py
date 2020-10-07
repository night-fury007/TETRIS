import pygame

from Piece import Piece

class GameBoard :
    def __init__(self, window_width, window_height, game_width, game_height, block_size):
        self.window_width = window_width
        self.window_height = window_height
        self.game_width = game_width
        self.game_height = game_height
        self.block_size = block_size
        self.top_left_x = (window_width - game_width) // 2
        self.top_left_y = (window_height - game_height) // 2

    def getShape(self):
        return Piece(5, 0)
    

    def convertShapeFormat(self, shape):
        positions = list()
        get_pattern = shape.pattern[shape.rotation % len(shape.pattern)]

        for i, line in enumerate(get_pattern):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def validSpace(self, shape, grid):
        accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        formatted = self.convertShapeFormat(shape)

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def createGrid(self, locked_pos=dict()):
        grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_pos:
                    c = locked_pos[(j,i)]
                    grid[i][j] = c
        return grid

    def drawNextShape(self, shape, Board):
        font = pygame.font.SysFont('Ink Free', 30)
        label = font.render('Next Pattern', 1, (255,255,255))

        temp_x = self.window_width - (self.top_left_x + self.game_width)
        sx = (self.top_left_x + self.game_width + temp_x/2) - (label.get_width()/2) 
        sy = self.top_left_y + self.game_height/2
        get_pattern = shape.pattern[shape.rotation % len(shape.pattern)]

        for i, line in enumerate(get_pattern):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(Board, shape.color, (sx + j*self.block_size, sy + i*self.block_size, self.block_size, self.block_size), 0)

        Board.blit(label, (sx, sy - 50))
        

    def drawBoard(self, Board, grid, score):
        Board.fill((0, 0, 0))
        pygame.font.init()
        font = pygame.font.SysFont('Ink Free', 30)
        label = font.render('Tetris', 1, (255, 255, 255))
        Board.blit(label, (self.top_left_x + self.game_width/2 - (label.get_width()/2), 10))

        font = pygame.font.SysFont('Ink Free', 30)
        label = font.render('Score: ' + str(score), 1, (255,255,255))
        temp_x = self.window_width - (self.top_left_x + self.game_width)
        sx = (self.top_left_x + self.game_width + temp_x/2) - (label.get_width()/2) 
        sy = self.top_left_y + self.game_height/2
        Board.blit(label, (sx, sy - 200))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(Board, grid[i][j], (self.top_left_x + j*self.block_size, self.top_left_y + i*self.block_size, self.block_size, self.block_size), 0)
        
        pygame.draw.rect(Board, (204, 0, 0), (self.top_left_x, self.top_left_y, self.game_width, self.game_height), 5)

    def clearRows(self, grid, locked):
        no_of_rows = 0
        for i in range(len(grid)-1, -1, -1):
            row = grid[i]
            if (0,0,0) not in row:
                no_of_rows += 1
                index = i
                for j in range(len(row)):
                    try:
                        del locked[(j,i)]
                    except:
                        continue

        if no_of_rows > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < index:
                    newKey = (x, y + no_of_rows)
                    locked[newKey] = locked.pop(key)

        return no_of_rows

    def checkLost(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

    def displayScore(self, win, text, score, size, color):
        font = pygame.font.SysFont("Ink Free", size, bold=True)
        label = font.render(text + str(score), 1, color)
        sx = self.top_left_x + self.game_width /2 - (label.get_width()/2)   
        sy = self.top_left_y + self.game_height/2 - (label.get_height()/2)
        win.blit(label, (sx, sy))
    
