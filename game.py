import pygame
import math
from pygame.locals import *
pygame.init()
## TODO ###
# 
# - Change square size to be determined when level created
# - Flash screen message on final level 
# - Menu
# - High score
#




# GLOBALS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

TOTAL_X = 700
TOTAL_Y = 500

SIZE = (TOTAL_X, TOTAL_Y)
CAPTION = "This game"




def load_level(filename):
	with open(filename) as f:
		level = []
		for line in f:
			line = line.strip()
			level_row = []
			for char in line:
				level_row.append(char)
			level.append(level_row)
	return level
level0 = load_level('level0.txt')
level1 = load_level('level1.txt')
level2 = load_level('level2.txt')
level3 = load_level('level3.txt')
level4 = load_level('level4.txt')
level5 = load_level('level5.txt')
level6 = load_level('level6.txt')
level7 = load_level('level7.txt')

levels = [level0, level1, level2, level3, level4, level5, level6, level7]
loc_x = 5
loc_y = 10

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(CAPTION)
done = False
clock = pygame.time.Clock()

square_width = 45
square_height = 45

class Board:
	def __init__(self, levels):
		self.levels = levels
		self.square_list = []
		self.color_map = {'W':BLUE, 'G':GREEN, 'X':RED}
		self.loc_x = 5
		self.loc_y = 10
		self.level_over = False
		self.current_level = 0
		self.square_width = round((TOTAL_X - 75) / len(self.levels[self.current_level][0]), 0)
		self.square_height = round((TOTAL_Y - 75) / len(self.levels[self.current_level]), 0)

		print 'Board Created'
		# for row in self.levels:
		# 	print row
	def make_level(self, levelnum):
		#print 'length of self.levels : ' + str(len(self.levels[0]))
		print 'Length of width: %s' % len(self.levels[levelnum][0])
		print 'Square Width: %s' % str(TOTAL_X - 50)
		print 'Square Count: %s' % len(self.levels[levelnum][0])
		square_width = round((TOTAL_X - 75) / len(self.levels[levelnum][0]), 0)
		square_height = round((TOTAL_Y - 75) / len(self.levels[levelnum]), 0)
		self.square_list = []
		for y in range(len(self.levels[levelnum])):
			#print 'length of self.levels[y] : ' + str(len(self.levels[levelnum][y]))
			for x in range(len(self.levels[levelnum][y])):
				self.color = self.color_map[self.levels[levelnum][y][x]]
				self.square_list.append(Square(self, self.loc_x, self.loc_y, x, y, self.square_width, self.square_height, self.color))
				self.loc_x += square_width + 5
			self.loc_x = 5
			self.loc_y += square_height + 5
		self.loc_y = 10
		

	def update(self):
		if not self.level_over:
			for square in self.square_list:
				square.update()
			p.update()
		else:
			self.level_over = False
			self.current_level += 1
			try:
				self.make_level(self.current_level)
				self.square_width = round((TOTAL_X - 75) / len(self.levels[self.current_level][0]), 0)
				self.square_height = round((TOTAL_Y - 75) / len(self.levels[self.current_level]), 0)
				p.move_to(0, 0)
				print 'Player Width from %s to %s' % (p.width, square_width)
				# square_width = round((TOTAL_X - 75) / len(self.levels[levelnum][0]), 0)
				# square_height = round((TOTAL_Y - 75) / len(self.levels[levelnum]), 0)
				p.width = self.square_width
				p.height = self.square_height
			except:
				print 'Winner!!'
				print 'Total Time: %s seconds.' % display_time
				self.make_level(self.current_level - 1)
				p.move_to(0,0)

class Square:
	def __init__(self, board, x, y, x_count, y_count, width, height, color):
		self.x = x
		self.y = y
		self.x_count = x_count
		self.y_count = y_count
		self.width = width
		self.height = height
		self.color = color
		self.board = board
	def valid_move(self, square):
		return square.color <> 'BLUE'
	def update(self):
		pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])

class Player(Square):
	def __init__(self, board, x, y, x_count, y_count, width, height, color):
		self.x = x
		self.y = y
		self.x_count = x_count
		self.y_count = y_count
		self.move(x_count, y_count)
		self.width = width
		self.height = height
		
		self.color = color
		#print 'Square at (x, y): (' + str(self.x) + ', ' + str(self.y) + ')'
		self.move_to(0, 0)
	def move(self, move_x, move_y):
		# print 'Player is at square x: %s, y: %s and ' %(self.x_count, self.y_count)
		# print 'is moving to square x: %s, y: %s' % (self.x_count + move_x, self.y_count + move_y)
		if self.valid_move(self.x_count + move_x, self.y_count + move_y):	
			self.x_count = self.x_count + move_x
			self.y_count = self.y_count + move_y
			dest = self.find_square(self.x_count, self.y_count)
			if dest:
				self.x = dest.x
				self.y = dest.y
	def move_to(self, x, y):
		dest = self.find_square(x, y)
		if dest:
			self.x = dest.x
			self.y = dest.y
			self.x_count = x
			self.y_count = y
	def valid_move(self, move_x, move_y):
		dest_square = self.find_square(move_x, move_y)
		if dest_square:
			if dest_square.color <> BLUE and dest_square.x_count >= 0:# and dest_square.x_count < len(dest_square.board.levels[0]):
				return True
			else:
				return False
		else:
			return False
	def find_square(self, x, y):
		for square in board.square_list:
			if square.x_count == x and square.y_count == y:
				return square
	def update(self):
		current = self.find_square(self.x_count, self.y_count)
		if current:
			if current.color == RED:
				print 'Level Complete!'
				print 
				print
				board.level_over = True
		
		pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
		

board = Board(levels)
pygame.display.flip()
board.make_level(0)
square_width = round((TOTAL_X - 75) / len(board.levels[board.current_level][0]), 0)
square_height = round((TOTAL_Y - 75) / len(board.levels[board.current_level]), 0)
p = Player(board, 5, 5, 0, 0, square_width, square_height, WHITE)

total_time = 0

# MAIN GAME LOOP
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		# if event.type == KEYDOWN and event.key == K_DOWN:
		# 	debug()
		if event.type == KEYDOWN and event.key == K_DOWN:
			p.move(0, 1)
		if event.type == KEYDOWN and event.key == K_UP:
			p.move(0, -1)
		if event.type == KEYDOWN and event.key == K_LEFT:
			p.move(-1, 0)
		if event.type == KEYDOWN and event.key == K_RIGHT:
			p.move(1, 0)
		if event.type == KEYDOWN and event.key == K_l:
			board.level_over = True

	# Reset the screen
	screen.fill(BLACK)

	total_time += clock.get_time()

	display_time = int(total_time / 1000)-1767859
	msg = 'Total Time: %s' % display_time

	fontObj = pygame.font.Font(None, 32)
	msgSurfaceObj = fontObj.render(msg, True, WHITE)
	msgRectObj = msgSurfaceObj.get_rect()
	msgRectObj.topleft = (10, TOTAL_Y - 30)
	screen.blit(msgSurfaceObj, msgRectObj)


	board.update()

	pygame.display.flip()


	clock.tick(60)
	
pygame.quit()