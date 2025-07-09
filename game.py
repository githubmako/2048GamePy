import pygame

class Game:
    def __init__(self, window):
        self.window = window
        self.width = 4
        self.height = 4
        self.tile_size = 100
        self.spacing = 10
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.font = pygame.font.SysFont("arial", 32)
        self.large_font = pygame.font.SysFont("arial", 48, bold=True)
        self.game_over = False
        self.won = False
        self.reset_game()

    def reset_game(self):
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        import random
        empty = [(r, c) for r in range(self.height) for c in range(self.width) if self.board[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = 2 if random.random() < 0.9 else 4

    def process_event(self, event):
        if self.game_over or self.won:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left()
            elif event.key == pygame.K_RIGHT:
                self.move_right()
            elif event.key == pygame.K_UP:
                self.move_up()
            elif event.key == pygame.K_DOWN:
                self.move_down()

    def update(self):
        if not self.game_over and not self.won:
            if self.is_won():
                self.won = True
            elif not self.is_move_possible():
                self.game_over = True

    def draw(self):
        self.window.fill((196,195,208))
        for r in range(self.height):
            for c in range(self.width):
                value = self.board[r][c]
                color = (72,61,139) if value == 0 else (238, 228, 218)
                x = c * (self.tile_size + self.spacing) + self.spacing
                y = r * (self.tile_size + self.spacing) + self.spacing + 100
                pygame.draw.rect(self.window, color, (x, y, self.tile_size, self.tile_size), border_radius=8)
                if value:
                    text = self.font.render(str(value), True, (119, 110, 101))
                    text_rect = text.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
                    self.window.blit(text, text_rect)
      
        score_text = self.font.render(f"Score: {self.score}", True, (119, 110, 101))
        self.window.blit(score_text, (10, 30))

       
        if self.game_over:
            self.display_message("Game Over!", "Press R to play again")
        elif self.won:
            self.display_message("You Won!", "Press R to play again")

    def display_message(self, text1, text2):
        overlay = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.window.blit(overlay, (0, 0))
        t1 = self.large_font.render(text1, True, (119, 110, 101))
        t2 = self.font.render(text2, True, (119, 110, 101))
        rect1 = t1.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2 - 30))
        rect2 = t2.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2 + 30))
        self.window.blit(t1, rect1)
        self.window.blit(t2, rect2)

    def move_left(self):
        changed = False
        for r in range(self.height):
            row = [v for v in self.board[r] if v != 0]
            new_row = []
            i = 0
            while i < len(row):
                if i + 1 < len(row) and row[i] == row[i + 1]:
                    new_row.append(row[i] * 2)
                    self.score += row[i] * 2
                    i += 2
                    changed = True
                else:
                    new_row.append(row[i])
                    i += 1
            new_row += [0] * (self.width - len(new_row))
            if new_row != self.board[r]:
                changed = True
            self.board[r] = new_row
        if changed:
            self.add_new_tile()

    def move_right(self):
        self.reverse_board()
        self.move_left()
        self.reverse_board()

    def move_up(self):
        self.transpose_board()
        self.move_left()
        self.transpose_board()

    def move_down(self):
        self.transpose_board()
        self.move_right()
        self.transpose_board()

    def reverse_board(self):
        for r in range(self.height):
            self.board[r] = self.board[r][::-1]

    def transpose_board(self):
        self.board = [list(w) for w in zip(*self.board)]

    def is_won(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] == 2048:
                    return True
        return False

    def is_move_possible(self):
        
        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] == 0:
                    return True
       
        for r in range(self.height):
            for c in range(self.width - 1):
                if self.board[r][c] == self.board[r][c + 1]:
                    return True
        for c in range(self.width):
            for r in range(self.height - 1):
                if self.board[r][c] == self.board[r + 1][c]:
                    return True
        return False