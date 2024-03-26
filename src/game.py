import pygame
import copy
from time import sleep

W = 1
B = 2
WW = 3
WB = 4
BW = 5
BB = 6
WK = 7
BK = 8

class Game:
  def __init__(self, board):
    self.board = board
    self.rows = 9
    self.cols = 9
    self.positions = self.get_positions(board)
    self.king = self.positions[2][0]
    self.white_knights = self.positions[0]
    self.black_knights = self.positions[1]

  def set_board(self, board):
    self.board = board

  def set_king(self, x, y):
    self.king = (x, y)
  
  def set_white_knights(self, white_knights):
    self.white_knights = white_knights

  def get_positions(self, board):
    positions = [[], [], []] # white_knights, black_knights, king
    for y in range(self.rows):
      for x in range(self.cols):
        if board[y][x] == WW or board[y][x] == BW:
          positions[0].append([x, y])
        elif board[y][x] == WB or board[y][x] == BB:
          positions[1].append([x, y])
        elif board[y][x] == WK or board[y][x] == BK:
          positions[2].append((x, y))
        else:
          pass
    return positions
  
  def change_white_knight_board(self, new_x, new_y, x, y):
    board = self.board
    if board[new_y][new_x] == WW:
      board[new_y][new_x] = W
      board[y][x] = BW
    elif board[new_y][new_x] == BW:
      board[new_y][new_x] = B
      board[y][x] = WW
    return board
  
  def change_king_board(self, x, y, new_x, new_y):
    board = self.board
    if board[y][x] == WK:
      board[y][x] = W
      board[new_y][new_x] = BK
    elif board[y][x] == BK:
      board[y][x] = B
      board[new_y][new_x] = WK
    return board
  
  def move_white_knight(self, x, y, direction):
    white_knights = self.white_knights
    if [x, y] in white_knights:
      if direction == 'up' and y - 1 >= 0 and self.board[y - 1][x] not in [0, WB, BB, WW, BW]:
        new_x, new_y = x, y - 1
      elif direction == 'left' and x - 1 >= 0 and self.board[y][x - 1] not in [0, WB, BB, WW, BW]:
        new_x, new_y = x - 1, y
      elif direction == 'down' and y + 1 <= 8 and self.board[y + 1][x] not in [0, WB, BB, WW, BW]:
        new_x, new_y = x, y + 1
      elif direction == 'right' and x + 1 <= 8 and self.board[y][x + 1] not in [0, WB, BB, WW, BW]:
        new_x, new_y = x + 1, y
      else:
        return False
      white_knight_index = white_knights.index([x, y])
      white_knights[white_knight_index] = [new_x, new_y]
      self.set_white_knights(white_knights)
      self.set_board(self.change_white_knight_board(x, y, new_x, new_y))
      return True
  
  def move(self, direction):
    x, y = self.king
    board = self.board
    if direction == 'up':
      new_x, new_y = x % 9, (y - 1) % 9
    elif direction == 'left':
      new_x, new_y = (x - 1) % 9, y % 9
    elif direction == 'down':
      new_x, new_y = x % 9, (y + 1) % 9
    elif direction == 'right':
      new_x, new_y = (x + 1) % 9, y % 9
    else:
      return False
    
    if board[new_y][new_x] in [0, WB, BB]:
      return False
    elif board[new_y][new_x] in [WW, BW]:
      if self.move_white_knight(new_x, new_y, direction):
        self.set_board(self.change_king_board(x, y, new_x, new_y))
        self.set_king(new_x, new_y)
        return 2
      return False
    self.set_board(self.change_king_board(x, y, new_x, new_y))
    self.set_king(new_x, new_y)
    return True

  def undo_move(self, move):
    x, y, direction, knight_moved = move
    white_knights = self.white_knights
    if direction == 'up':
      new_x, new_y = x % 9, (y + 1) % 9
      knight_x, knight_y = x % 9, (y - 1) % 9
    elif direction == 'left':
      new_x, new_y = (x + 1) % 9, y % 9
      knight_x, knight_y = (x - 1) % 9, y % 9
    elif direction == 'down':
      new_x, new_y = x % 9, (y - 1) % 9
      knight_x, knight_y = x % 9, (y + 1) % 9
    elif direction == 'right':
      new_x, new_y = (x - 1) % 9, y % 9
      knight_x, knight_y = (x + 1) % 9, y % 9
    if knight_moved:
      white_knight_index = white_knights.index([knight_x, knight_y])
      white_knights[white_knight_index] = [x, y]
      self.set_white_knights(white_knights)
      self.set_board(self.change_white_knight_board(knight_x, knight_y, x, y))
    self.set_board(self.change_king_board(x, y, new_x, new_y))
    self.set_king(new_x, new_y)

  def simulate(self, white_knights, black_knights):
    if all(knight[2] for knight in black_knights):
      return True

    moves = [(1, -2), (1, 2), (-1, -2), (-1, 2), (2, -1), (2, 1), (-2, -1), (-2, 1)]
    for white_knight in white_knights:
      if not white_knight[2]:
        for move in moves:
          for black_knight in black_knights:
            if not black_knight[2] and white_knight[0] + move[0] == black_knight[0] and white_knight[1] + move[1] == black_knight[1]:
              white_knights_copy = [list(knight) for knight in white_knights]
              black_knights_copy = [list(knight) for knight in black_knights]
              white_knights_copy[white_knights.index(white_knight)][2] = True
              black_knights_copy[black_knights.index(black_knight)][2] = True
              if self.simulate(white_knights_copy, black_knights_copy):
                return True

    return False

  def check_win(self):
    while True:
      white_knights = copy.deepcopy(self.white_knights)
      black_knights = copy.deepcopy(self.black_knights)

      for white_knight in white_knights:
        white_knight.append(False)
      
      for black_knight in black_knights:
        black_knight.append(False)

      if self.simulate(white_knights, black_knights):
        return True
      return False
  
  def draw(self, WIN, SQUARE_SIZE, WK_IMAGE_PATH, BK_IMAGE_PATH, K_IMAGE_PATH):
    board = self.board
    for y in range(self.rows):
      for x in range(self.cols):
        if board[y][x] == W:
          pygame.draw.rect(WIN, (255, 255, 255), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        elif board[y][x] == B:
          pygame.draw.rect(WIN, (0, 0, 0), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        elif board[y][x] == 0:
          pygame.draw.rect(WIN, (112, 113, 160), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        elif board[y][x] == WW:
          pygame.draw.rect(WIN, (255, 255, 255), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
          WIN.blit(WK_IMAGE_PATH, (x*SQUARE_SIZE, y*SQUARE_SIZE))
        elif board[y][x] == WB:
          pygame.draw.rect(WIN, (255, 255, 255), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
          WIN.blit(BK_IMAGE_PATH, (x*SQUARE_SIZE, y*SQUARE_SIZE))
        elif board[y][x] == BW:
          pygame.draw.rect(WIN, (0, 0, 0), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
          WIN.blit(WK_IMAGE_PATH, (x*SQUARE_SIZE, y*SQUARE_SIZE))
        elif board[y][x] == BB:
          pygame.draw.rect(WIN, (0, 0, 0), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
          WIN.blit(BK_IMAGE_PATH, (x*SQUARE_SIZE, y*SQUARE_SIZE))
        elif board[y][x] == WK:
          pygame.draw.rect(WIN, (255, 255, 255), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
          WIN.blit(K_IMAGE_PATH, (x*SQUARE_SIZE, y*SQUARE_SIZE))
        elif board[y][x] == 8:
          pygame.draw.rect(WIN, (0, 0, 0), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
          WIN.blit(K_IMAGE_PATH, (x*SQUARE_SIZE, y*SQUARE_SIZE))

  def dfs_king(self, max_depth, depth, path):
    king = self.king
    if depth >= max_depth:
      return []
    moves = [['right', 1, 0], ['left', -1, 0], ['down', 0, 1], ['up', 0, -1]]
    temp_path = path
    for [direction, x, y] in moves:
      new_x, new_y = king[0] + x, king[1] + y
      value = self.move(direction)
      if value or value == 2:
        temp_path.append((new_x, new_y, direction, value == 2))
        if self.check_win():
          return ["WIN", temp_path]
        tail = self.dfs_king(max_depth, depth + 1, temp_path)
        if len(tail) == 0:
          if len(temp_path) != 0:
            self.undo_move(temp_path.pop())
        elif tail[0] == "WIN":
          return tail
        else:
          temp_path = tail
    return []
