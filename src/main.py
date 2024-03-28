import pygame
from time import sleep
from board import Board
from game import Game
from macros import *

def draw_levels_menu(win):
  win.fill((112, 113, 160))
  
  win.blit(TITLE_IMAGE_PATH, (105, 100))
  win.blit(LEVEL_ONE_IMAGE_PATH, (68, 400))
  win.blit(LEVEL_TWO_IMAGE_PATH, (216, 400))
  win.blit(LEVEL_THREE_IMAGE_PATH, (364, 400))
  win.blit(LEVEL_FOUR_IMAGE_PATH, (512, 400))
  win.blit(LEVEL_FIVE_IMAGE_PATH, (660, 400))
  win.blit(LEVEL_SIX_IMAGE_PATH, (68, 600))
  win.blit(LEVEL_SEVEN_IMAGE_PATH, (216, 600))
  win.blit(LEVEL_EIGHT_IMAGE_PATH, (364, 600))
  win.blit(LEVEL_NINE_IMAGE_PATH, (512, 600))
  win.blit(LEVEL_TEN_IMAGE_PATH, (660, 600))
  pygame.display.update()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        return 0
      if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        if 68 <= x <= 148 and 400 <= y <= 480:
          return 0
        elif 216 <= x <= 296 and 400 <= y <= 480:
          return 1
        elif 364 <= x <= 444 and 400 <= y <= 480:
          return 2
        elif 512 <= x <= 592 and 400 <= y <= 480:
          return 3
        elif 660 <= x <= 740 and 400 <= y <= 480:
          return 4
        elif 68 <= x <= 148 and 600 <= y <= 680:
          return 5
        elif 216 <= x <= 296 and 600 <= y <= 680:
          return 6
        elif 364 <= x <= 444 and 600 <= y <= 680:
          return 7
        elif 512 <= x <= 592 and 600 <= y <= 680:
          return 8
        elif 660 <= x <= 740 and 600 <= y <= 680:
          return 9

def draw_start_menu(win):
  win.fill((112, 113, 160))
  
  win.blit(TITLE_IMAGE_PATH, (105, 100))
  win.blit(HUMAN_IMAGE_PATH, (50, 500))
  win.blit(DFS_IMAGE_PATH, (460, 500))
  win.blit(BFS_IMAGE_PATH, (50, 600))
  win.blit(A_STAR_IMAGE_PATH, (460, 600))
  pygame.display.update()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        return '', ''
      if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        if 50 <= x <= 350 and 500 <= y <= 580:
          return 'Human', ''
        elif 460 <= x <= 760 and 500 <= y <= 580:
          return 'AI', 'DFS'
        elif 50 <= x <= 350 and 600 <= y <= 680:
          return 'AI', 'BFS'
        elif 460 <= x <= 760 and 600 <= y <= 680:
          return 'AI', 'A*'

def draw_menu(win):
  win.fill((112, 113, 160))

  win.blit(TITLE_IMAGE_PATH, (105, 100))
  win.blit(START_IMAGE_PATH, (50, 500))
  win.blit(EXIT_IMAGE_PATH, (460, 500))
  win.blit(LEVELS_IMAGE_PATH, (50, 600))
  win.blit(CONFIG_IMAGE_PATH, (460, 600))
  pygame.display.update()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        return 2
      if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        if 50 <= x <= 350 and 500 <= y <= 580:
          return 1
        elif 460 <= x <= 760 and 500 <= y <= 580:
          return 2
        elif 50 <= x <= 350 and 600 <= y <= 680:
          return 3
        elif 460 <= x <= 760 and 600 <= y <= 680:
          return 4
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          return 2

def main():
  # PYGAME INITIALIZATION
  pygame.init()
  pygame.display.set_caption("Chesskoban")
  pygame.display.set_icon(pygame.image.load("../img/pieces/white_king.png"))

  win = pygame.display.set_mode((WIDTH, HEIGHT))

  FONT = pygame.font.Font(None, 40)

  SPACE_TEXT = FONT.render("Press SPACE to finish", True, (255, 255, 255))
  WIN_TEXT = FONT.render("You win!", True, (0, 255, 0))
  LOSE_TEXT = FONT.render("You lose!", True, (255, 0, 0))
  AI_TEXT = FONT.render("Press N to continue", True, (255, 255, 255))

  SPACE_TEXT_RECT = SPACE_TEXT.get_rect()
  WIN_TEXT_RECT = WIN_TEXT.get_rect()
  LOSE_TEXT_RECT = LOSE_TEXT.get_rect()
  AI_TEXT_RECT = AI_TEXT.get_rect()
  
  SPACE_TEXT_RECT.center = (WIDTH // 2, 20)
  WIN_TEXT_RECT.center = (WIDTH // 2, 20)
  LOSE_TEXT_RECT.center = (WIDTH // 2, 20)
  AI_TEXT_RECT.center = (WIDTH // 2, 20)

  # GAME INITIALIZATION
  level = 0
  GAME_PLAYER = Game(Board(level).board)

  menu_option = draw_menu(win)
  
  if menu_option == 1:
    player, algorithm = draw_start_menu(win)
    if player == '':
      level = 5
  elif menu_option == 2:
    level = 5
  elif menu_option == 3:
    level_option = draw_levels_menu(win)
    player, algorithm = draw_start_menu(win)
    level = level_option
  elif menu_option == 4:
    # TODO show how to play, change what is below
    player, algorithm = 'Human', ''

  while level < 5:
    GAME_PLAYER.set_board(Board(level).board)

    if player == 'AI':
      display_text = AI_TEXT
      display_textRect = AI_TEXT_RECT
    else:
      display_text = SPACE_TEXT
      display_textRect = SPACE_TEXT_RECT
    
    run = True
    dfs = 'DFS' == algorithm
    bfs = 'BFS' == algorithm

    move_count = 0
    moves = []

    while run:
      if dfs:
        moves = GAME_PLAYER.dfs_king(MAX_DEPTH[level], 0, [])
        GAME_PLAYER.set_board(Board(level).board)
        dfs = False
      
      if bfs:
        moves = GAME_PLAYER.bfs_king()
        GAME_PLAYER.set_board(Board(level).board)
        bfs = False
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
        elif event.type == pygame.KEYDOWN:
          direction = ''
          if player == 'Human':
            if event.key == pygame.K_w:
              direction = 'up'
            elif event.key == pygame.K_a:
              direction = 'left'
            elif event.key == pygame.K_s:
              direction = 'down'
            elif event.key == pygame.K_d:
              direction = 'right'
            elif event.key == pygame.K_SPACE:
              run = False
              if GAME_PLAYER.check_win():
                display_text = WIN_TEXT
                display_textRect = WIN_TEXT_RECT
              else:
                display_text = LOSE_TEXT
                display_textRect = LOSE_TEXT_RECT
                level -= 1
            elif event.key == pygame.K_q:
              run = False
              level = 4
              break
            if direction != '':
              GAME_PLAYER.move(direction)
          else:
            if event.key == pygame.K_n and move_count < MAX_DEPTH[level]:
              GAME_PLAYER.move(moves[1][move_count][2])
              move_count += 1
              if move_count == MAX_DEPTH[level]:
                display_text = WIN_TEXT
                display_textRect = WIN_TEXT_RECT
                run = False
                break
            elif event.key == pygame.K_q:
              run = False
              level = 4
              break
            
      GAME_PLAYER.draw(win)
      
      pygame.draw.rect(win, (0, 0, 0), display_textRect)
      win.blit(display_text, display_textRect)

      pygame.display.update()

      if display_text in [WIN_TEXT, LOSE_TEXT]:
        sleep(0.5)

    level += 1

  sleep(0.5)

  pygame.quit()

if __name__ == "__main__":
  main()
