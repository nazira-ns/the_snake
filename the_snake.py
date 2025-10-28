from __future__ import annotations
import random
from typing import List, Tuple
import pygame

# Размеры окна и клетки
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20

# Количество клеток по ширине и высоте
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


def draw_rect(surface, color, pos):
    x, y = pos
    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect)


class GameObject:
    # Базовый объект (позиция и цвет)
    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        draw_rect(surface, self.body_color, self.position)


class Apple(GameObject):
    # Яблоко появляется случайно
    def __init__(self):
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )


class Snake(GameObject):
    # Змейка из нескольких клеток
    def __init__(self):
        start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        super().__init__(start_pos, SNAKE_COLOR)
        self.positions: List[Tuple[int, int]] = [start_pos]
        self.direction = RIGHT

    def get_head_position(self):
        return self.positions[0]

    # Меняем направление (не даёт повернуть назад)
    def update_direction(self, new_direction):
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    # Движение вперёд
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        self.positions.insert(0, new)
        self.position = new
        self.positions = self.positions[:len(self.positions)]

    # Начать сначала
    def reset(self):
        self.__init__()

    # Отрисовка всех сегментов
    def draw(self, surface):
        for pos in self.positions:
            draw_rect(surface, self.body_color, pos)


# Обработка клавиш игрока
def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                return True
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)
    return False


def main():
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(8)  # чтобы не слишком быстро

        if handle_keys(snake):
            break

        snake.move()

        # если змейка съела яблоко → растём
        if snake.get_head_position() == apple.position:
            snake.positions.append(snake.positions[-1])
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
