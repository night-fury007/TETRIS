import pygame

from GameBoard import GameBoard
from Utilities import BUTTON

pygame.font.init()

window_width = 800
window_height = 700
game_width = 300  
game_height = 600  
block_size = 30

top_left_x = (window_width - game_width) // 2
top_left_y = (window_height - game_height)

def playGame(win):
    pygame.display.set_caption("TETRIS")

    game_board = GameBoard(window_width, window_height, game_width, game_height, block_size)
    locked_positions = dict()
    grid = game_board.createGrid(locked_positions)
    change_piece = False
    current_piece = game_board.getShape()
    next_piece = game_board.getShape()
    clock = pygame.time.Clock()
    score = 0
    fall_time = 0
    fall_speed = 0.7
    level_time = 0
    running = True
    while running :
        grid = game_board.createGrid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 10:
            level_time = 0
            if fall_speed > 0.11:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(game_board.validSpace(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        for event in pygame.event.get() :
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT :
                running = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(game_board.validSpace(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(game_board.validSpace(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(game_board.validSpace(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(game_board.validSpace(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = game_board.convertShapeFormat(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = game_board.getShape()
            change_piece = False
            matched_rows = game_board.clearRows(grid, locked_positions)
            if matched_rows == 1 :
                score +=  matched_rows * 10
            elif matched_rows == 2 :
                score +=  matched_rows * 20
            elif matched_rows > 2 :
                score +=  matched_rows * 30        

        game_board.drawBoard(win, grid, score)   
        game_board.drawNextShape(next_piece, win)    
        pygame.display.update() 

        if game_board.checkLost(locked_positions):
            game_board.displayScore(win, " YOUR SCORE ", score, 50, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            running = False

def main(win):
    pygame.display.set_caption("TETRIS")
    
    running = True
    play_button = BUTTON((172, 57, 57), 350, 600, 100, 50, "PLAY")
    while running :
        for event in pygame.event.get() :
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT :
                running = False
                pygame.display.quit()
                quit()

            if event.type == pygame.MOUSEMOTION :
                if play_button.isOver(pos) :
                    play_button.color = (51, 153, 102)
                else :
                    play_button.color = (172, 57, 57)
            if event.type == pygame.MOUSEBUTTONDOWN :
                if play_button.isOver(pos) : 
                    playGame(win)

        win.fill((0, 0, 0))
        play_button.draw(win)            
        pygame.display.update()                    

if __name__== "__main__" : 
    win = pygame.display.set_mode((window_width, window_height))
    main(win) 