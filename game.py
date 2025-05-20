from grid import Grid
from blocks import *
import random
import pygame

class Game:
	def __init__(self):
		# Inicializa a grade de jogo e os blocos disponíveis
		self.grid = Grid()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()  # Bloco atual em jogo
		self.next_block = self.get_random_block()     # Próximo bloco a ser exibido
		self.game_over = False
		self.score = 0

		# Sons para rotação e remoção de linha
		self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
		self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

		# Música de fundo do jogo
		pygame.mixer.music.load("Sounds/original_music.ogg")
		pygame.mixer.music.set_volume(0.2)
		pygame.mixer.music.play(-1)

	# Atualiza a pontuação com base nas linhas limpas e nos pontos por movimentação para baixo
	def update_score(self, lines_cleared, move_down_points):
		if lines_cleared == 1:
			self.score += 100
		elif lines_cleared == 2:
			self.score += 300
		elif lines_cleared == 3:
			self.score += 500
		self.score += move_down_points

	# Retorna um bloco aleatório, garantindo variedade (sem repetição imediata)
	def get_random_block(self):
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = random.choice(self.blocks)
		self.blocks.remove(block)
		return block

	# Movimenta o bloco atual para a esquerda (caso possível)
	def move_left(self):
		self.current_block.move(0, -1)
		if not self.block_inside() or not self.block_fits():
			self.current_block.move(0, 1)

	# Movimenta o bloco atual para a direita (caso possível)
	def move_right(self):
		self.current_block.move(0, 1)
		if not self.block_inside() or not self.block_fits():
			self.current_block.move(0, -1)

	# Move o bloco para baixo; se não puder descer mais, fixa-o na grade
	def move_down(self):
		self.current_block.move(1, 0)
		if not self.block_inside() or not self.block_fits():
			self.current_block.move(-1, 0)
			self.lock_block()

	# Fixa o bloco atual na grade e prepara o próximo
	def lock_block(self):
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		self.current_block = self.next_block
		self.next_block = self.get_random_block()

		# Limpa linhas completas e atualiza pontuação
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.clear_sound.play()
			self.update_score(rows_cleared, 0)

		# Verifica se o novo bloco colide — fim de jogo
		if not self.block_fits():
			self.game_over = True

	# Reinicia o jogo
	def reset(self):
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.score = 0

	# Verifica se o bloco atual cabe nas posições da grade
	def block_fits(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if not self.grid.is_empty(tile.row, tile.column):
				return False
		return True

	# Tenta rotacionar o bloco atual; se não couber, desfaz
	def rotate(self):
		self.current_block.rotate()
		if not self.block_inside() or not self.block_fits():
			self.current_block.undo_rotation()
		else:
			self.rotate_sound.play()

	# Verifica se todas as posições do bloco estão dentro da grade
	def block_inside(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if not self.grid.is_inside(tile.row, tile.column):
				return False
		return True

	# Desenha a grade, o bloco atual e o próximo bloco na tela
	def draw(self, screen):
		self.grid.draw(screen)
		self.current_block.draw(screen, 11, 11)

		# Ajusta a posição do próximo bloco com base no seu tipo
		if self.next_block.id == 3:
			self.next_block.draw(screen, 255, 290)  # Bloco O
		elif self.next_block.id == 4:
			self.next_block.draw(screen, 255, 280)  # Bloco S
		else:
			self.next_block.draw(screen, 270, 270)
