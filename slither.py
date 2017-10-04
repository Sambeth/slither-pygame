# make necessary imports
# pygame will be used to create the game
# sys will be used to exit the game
# time will be used to create a delay
# random will be used to create random cordinates
import pygame, random, sys, time

# initailize pygame
starter = pygame.init()

# check errors on init
if starter[1] > 0:
    print('Game has {} errors, exiting.....'.format(starter[1]))
    sys.exit(-1)
else:
    print('Game run succesfully!')

# create resoultion and caption
resolution = (800, 600)
game_board = pygame.display.set_mode(resolution)
pygame.display.set_caption('Slither')

# create colors needed
white = pygame.Color(255, 255, 255)  # background
green = pygame.Color(0, 255, 0)  # snake
brown = pygame.Color(165, 42, 42)  # food
black = pygame.Color(0, 0, 0)  # score
red = pygame.Color(255, 0, 0)  # game over

# frames per seconds
FPS = pygame.time.Clock()

# create snake body(head, body, size)
snakeHead = [150, 50]
snakeBody = [[150, 50], [140, 50], [130, 50]]
snakeSize = 10

# snake food(random postion as a multiple of 10)
snakeFood = [random.randrange(1, 80)*10, random.randrange(1, 60)*10]
foodSpawn = True

# direction of snake
direction = 'RIGHT'
turn_to = direction

score = 0


# game over function
def game_over():
    go_font = pygame.font.SysFont('monaco', 72)
    go_surface = go_font.render('Game Over!', True, red)
    go_rect = go_surface.get_rect()
    go_rect.midtop = (400, 15)
    game_board.blit(go_surface, go_rect)
    show_score(0)
    pygame.display.update()
    time.sleep(4)
    pygame.quit()
    sys.exit()


# score function
def show_score(choice=1):
    s_font = pygame.font.SysFont('monaco', 23)
    s_surface = s_font.render('Score: {0}'.format(score), True, black)
    s_rect = s_surface.get_rect()
    if choice == 1:
        s_rect.midtop = (80, 10)
    else:
        s_rect.midtop = (400, 90)
    game_board.blit(s_surface, s_rect)


while True:
    # create game movement events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                turn_to = 'RIGHT'
            elif event.key == pygame.K_LEFT:
                turn_to = 'LEFT'
            elif event.key == pygame.K_UP:
                turn_to = 'UP'
            elif event.key == pygame.K_DOWN:
                turn_to = 'DOWN'

    # validate direction so you cant move in opposite directions
    if turn_to == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    elif turn_to == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    elif turn_to == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    elif turn_to == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    # locomotion of snake
    if direction == 'RIGHT':
        snakeHead[0] += 10
    elif direction == 'LEFT':
        snakeHead[0] -= 10
    elif direction == 'UP':
        snakeHead[1] -= 10
    elif direction == 'DOWN':
        snakeHead[1] += 10

    # snake body mechanism
    snakeBody.insert(0, list(snakeHead))
    if snakeHead[0] == snakeFood[0] and snakeHead[1] == snakeFood[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()

    # spawn food after eaten
    if foodSpawn is False:
        snakeFood = [random.randrange(1, 80) * 10, random.randrange(1, 60) * 10]
        foodSpawn = True

    # draw white background
    game_board.fill(white)

    # draw snake
    for pos in snakeBody:
        pygame.draw.rect(game_board, green, pygame.Rect(pos[0], pos[1], snakeSize, snakeSize))

    # draw snake food
    pygame.draw.rect(game_board, brown, pygame.Rect(snakeFood[0], snakeFood[1], snakeSize, snakeSize))

    # board boundaries
    if snakeHead[0] < 0 or snakeHead[0] > 790:
        game_over()
    elif snakeHead[1] < 0 or snakeHead[1] > 590:
        game_over()

    # suicide hits
    for block in snakeBody[1:]:
        if snakeHead[0] == block[0] and snakeHead[1] == block[1]:
            game_over()

    show_score()
    pygame.display.update()
    FPS.tick(15)
