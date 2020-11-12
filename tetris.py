import pygame
import random

# 10x20 square grid
# shapes: S, Z, I, O, J, L, T

pygame.font.init()


# GLOBAL VARIABLES
s_width = 800 #width of screen
s_height = 660 #height of screen
p_width = 300 #play area width
p_height = 600 #play area height
block_size = 30
tlx = (s_width - p_width) // 2
tly = s_height - p_height 


# SHAPE FORMATS
  #lists within lists gives various orientations the shapes can have on rotation
  #periods(.) represent no block while zeroes(0) represent blocks

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....', 
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..', 
      '..0..', 
      '..0..',
      '.....']]

T = [['.....', 
      '..0..', 
      '.000.', 
      '.....', 
      '.....'], 
     ['.....', 
      '..0..', 
      '..00.', 
      '..0..', 
      '.....'], 
     ['.....', 
      '.....', 
      '.000.', 
      '..0..', 
      '.....'], 
     ['.....', 
      '..0..', 
      '.00..', 
      '..0..', 
      '.....']]

shapes = [S, Z, Z, I, I, O, J, L, L, T]
shape_colors = [(255,128,0), (153,255,51), (153,255,51), (0,255,255), (0,255,255), (255,255,0), (102,0,204), (255,51,153), (255,51,153), (0,128,255)]


#DECLARING UTILITY FUNCTIONS AND CLASSES

class Piece(object): #to store information common to all shapes
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)] #color will be the color at index of whatever shape is given from the list of colors
        self.rotation = 0


def create_grid(locked_pos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    #looping to create 10 cols for each of the 20 rows, (0,0,0) for color

    for i in range(len(grid)): #runs till 20 (for rows)
        for j in range(len(grid[i])): #10 times for each (for cols)
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c 
    return grid


def convert_shape_format(shape): #convert shape format to positions
    positions = []
    formats = shape.shape[shape.rotation % len(shape.shape)] #gives the current shape(sublist)

    for i, line in enumerate(formats):
        row = list(line) #a line looks something like '..0..'

        for j, col in enumerate(row): #col will have a '.' or a '0' each time
            if col == '0':
                positions.append((shape.x + j, shape.y + i)) #for every position we need to add the prev x and y pos of the shape to the col and row value of where the block should be

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 3) #to avoid offsetting to the right and down due to trailing periods

    return positions


def valid_space(shape, grid):
    acc_pos = [[ (j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)] #every possible *empty* position for 20x10 grid
    acc_pos = [j for sub_lst in acc_pos for j in sub_lst] #overriding the list to create a 1-D list
    
    formatted_shapes = convert_shape_format(shape)
    
    for pos in formatted_shapes:
        if pos not in acc_pos and pos[1] > -1: #shapes(y pos) starts somewhere above the screen and not shows up on screen
            return False
    return True


def check_lost(positions): #to check if we lost game
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece (5, 0, random.choice(shapes)) #returns a random shape from the shape list as an obj of Piece class


def draw_text_mid(surface, txt, size, color, shift=0):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(txt, 1, color)

    surface.blit(label, (tlx + p_width/2 - (label.get_width()/2), tly + shift + p_height/2 - (label.get_height()/2)))


def draw_grid(surface, grid):
    sx = tlx
    sy = tly
    for i in range(1, len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size - 15), (sx + p_width, sy + i*block_size - 15)) #Horizontal
        for j in range(1, len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*block_size, sy - 15), (sx + j*block_size, sy + p_height - 15))#Vertical


def draw_nextshape(shape, surface): #to show next shape
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape :', 1, (255,255,255))
    sx = tlx + p_width + 50
    sy = tly + p_height/2 - 60
    surface.blit(label, (sx + 9, sy - 20))
    
    formatted = shape.shape[shape.rotation % len(shape.shape)]
    
    for i, line in enumerate(formatted):
        row = list(line)
        for j, col in enumerate(row):
            if col == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy+i*block_size, block_size, block_size), 0)

    
def draw_window(surface, grid, score = 0):
    surface.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 50)
    label = font.render("TETRIS", 1, (255, 255, 255))

    surface.blit(label, (tlx + p_width/2 - (label.get_width()/2), 10))
               #(txt, (x_position, y_position))
    
    # for displaying score
    font = pygame.font.SysFont('comicsans', 36)
    label = font.render('SCORE : ' + str(score), 1, (255,255,255))
    sx = tlx - 180
    sy = tly + p_height/2 - 74
    surface.blit(label, (sx, sy))
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (tlx + j*block_size , tly + i*block_size - 15, block_size, block_size), 0)
            #(surface, grid_pos, (x_pos{start_x_pos + curr_col*block_size}, y_pos{start_y_pos + curr_row*block_size}, block_size as in width, block_size as in height)

    pygame.draw.rect(surface, (255, 255, 255), (tlx, tly-15, p_width, p_height), 4)

    draw_grid(surface, grid)
    #pygame.display.update()


def update_scores(nscore):
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    with open('scores.txt','w') as f:
        if int(nscore) > int(score):
            f.write(str(nscore))
        else:
            f.write(str(score))


def high_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def clear_rows(grid, locked):
    inc = False
    ind = []
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc = True  
            ind.append(i) #used to indexing which row had been removed
            for j in range(len(row)):
                try:
                    del locked[(j, i)] #deleting those keys and values from the grid ie, locked positions list
                except:
                    continue

    if inc:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]: #sorts on basis of y value
            x, y = key
            increment = 0
            for d in ind:
                if y < d: #rows above the current index
                    increment += 1
            if increment > 0: 
                newKey = (x, y + increment) #shifting the above rows down by incrementing y
                locked[newKey] = locked.pop(key)

    return inc


def pause(surface, run, clock):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

        surface.fill((0,0,0))
        draw_text_mid(surface, 'PAUSED', 70, (255,0,0))
        draw_text_mid(surface, 'Press C to continue', 40, (255,255,255), 50)
        pygame.display.update()
        clock.tick(5)

    return run


def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True 
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.6
    fall_level = 0
    score = 0 #increment score by 10 each time we clear a row
    last_score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime() 
        fall_level += clock.get_rawtime()
        clock.tick()

        if fall_level/100 > 5: #to inc speed every 5s in the game
            fall_level = 0
            if fall_speed > 0.22:
                fall_speed -= 0.0015

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1 
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -=1
                change_piece = True #piece either hit bottom of screen or another piece

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x +=1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -=1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -=1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -=1
                if event.key == pygame.K_p:
                    run = pause(win, run, clock)

        shape_pos = convert_shape_format(current_piece)

        #drawing piece into the grid
        for i in range(len(shape_pos)):
            x, y =  shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
                #updating the color of grid acc to locked position of a shape
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            
            score += clear_rows(grid, locked_positions) * 10

        
        draw_window(win, grid, score)
        draw_nextshape(next_piece, win)

        pygame.display.update()

        if check_lost(locked_positions):
            update_scores(score)
            last_score = high_score()
            win.fill((0,0,0))
            draw_text_mid(win, "GAME OVER!!", 140, (255,0,0))
            draw_text_mid(win, "HIGH SCORE : " + str(last_score), 70, (255,255,255), 75)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False


def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_mid(win, 'Press Any Key To Continue', 60, (255,255,255))
        draw_text_mid(win, 'Press P to pause the game at any time', 40, (255,0,0), 50)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")

main_menu(win)