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


def draw_rect(surface: pygame.Surface, color: Tuple[int, int, int], pos: Tuple[int, int]) -> None:
    """Draw a single grid cell (rectangle) on the given surface."""
    x, y = pos
    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect)


class GameObject:
    """Base game object with position and color."""

    def __init__(self, position: Tuple[int, int] = (0, 0), body_color: Tuple[int, int, int] = (255, 255, 255)):
        """Initialize the game object with position and body color."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the object on the given surface."""
        draw_rect(surface, self.body_color, self.position)


class Apple(GameObject):
    """Apple that appears at a random position on the board."""

    def __init__(self) -> None:
        """Create an apple and place it randomly."""
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Move the apple to a new random cell."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )


class Snake(GameObject):
    """Snake consisting of multiple grid cells."""

    def __init__(self) -> None:
        """Initialize the snake in the center of the board."""
        start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        super().__init__(start_pos, SNAKE_COLOR)
        self.positions: List[Tuple[int, int]] = [start_pos]
        self.direction = RIGHT

    def get_head_position(self) -> Tuple[int, int]:
        """Return the current position of the snake's head."""
        return self.positions[0]

    def update_direction(self, new_direction: Tuple[int, int]) -> None:
        """Update movement direction, preventing a 180-degree turn."""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def move(self) -> None:
        """Move the snake one step forward (with wrap-around)."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)

        self.positions.insert(0, new_head)
        self.position = new_head

        # Remove tail segment to keep the length constant (growth handled elsewhere).
        self.positions.pop()

    def reset(self) -> None:
        """Reset the snake to the initial state."""
        self.__init__()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all snake segments on the given surface."""
        for pos in self.positions:
            draw_rect(surface, self.body_color, pos)


def handle_keys(snake: Snake) -> bool:
    """Handle player input. Return True if the game should exit."""
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


def main() -> None:
    """Run the Snake game loop."""
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(8)

        if handle_keys(snake):
            break

        snake.move()

        # If the snake eats the apple, grow by adding one more segment.
        if snake.get_head_position() == apple.position:
            snake.positions.append(snake.positions[-1])
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
