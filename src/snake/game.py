"""Vòng lặp chính, trạng thái game, xử lý va chạm và tính điểm.

Người phụ trách: Hồ Văn Trọng (26730077)

Đã xong toàn bộ T1 quản lý trạng thái, T2 nhận phím, T3 nhịp đi, T4 ăn mồi và
va chạm, T5 điểm cao nhất. Phần vẽ gọi sang module ``ui`` của Tín, phần rắn và
mồi dùng lớp ``Snake`` và ``Food`` của Diễm.
"""

from __future__ import annotations

import json
from collections import deque
from enum import Enum, auto

import pygame

from . import config, ui
from .food import Food
from .snake import DOWN, LEFT, RIGHT, UP, Snake

# --- Bảng tra phím ---------------------------------------------------------
# Dùng dict thay cho một dãy if để dễ thêm phím mới và dễ đọc.
KEY_TO_DIRECTION = {
    pygame.K_UP: UP,
    pygame.K_w: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_d: RIGHT,
}

# Phím chọn mức độ khó ở màn hình menu, kèm tên hiển thị.
KEY_TO_DIFFICULTY = {
    pygame.K_1: ("DE", config.SPEED_EASY),
    pygame.K_2: ("THUONG", config.SPEED_NORMAL),
    pygame.K_3: ("KHO", config.SPEED_HARD),
}

# Số hướng được xếp hàng chờ. Xem giải thích ở Game.handle_keydown.
DIRECTION_QUEUE_SIZE = 2

# Ô mà đầu rắn xuất phát: giữa lưới, chừa chỗ bên trái cho thân rắn.
START_CELL = (config.GRID_WIDTH // 2, config.GRID_HEIGHT // 2)

# Sai số cho phép khi so sánh thời gian. Số thực trong máy tính không chính xác
# tuyệt đối: 0.05 + 0.04 + 0.01 ra 0.09999999999999999 chứ không phải 0.1. Thiếu
# hằng số này thì thỉnh thoảng rắn bị trễ mất một khung hình.
EPSILON = 1e-9


class GameState(Enum):
    """Bốn trạng thái người chơi có thể đang ở.

    MENU --[Space]--> PLAYING --[P]--> PAUSED --[P]--> PLAYING
                         |
                      [va chạm]
                         v
                     GAME_OVER --[Space]--> PLAYING
    """

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


def load_highscore(path: str = config.HIGHSCORE_FILE) -> int:
    """Đọc điểm cao nhất từ file.

    Trả về 0 nếu file chưa tồn tại, không đọc được, hoặc nội dung hỏng.
    Game tuyệt đối không được crash chỉ vì thiếu file điểm.
    """
    try:
        with open(path, encoding="utf-8") as f:
            value = int(json.load(f)["highscore"])
    except (OSError, ValueError, TypeError, KeyError, IndexError):
        return 0
    return max(value, 0)


def save_highscore(score: int, path: str = config.HIGHSCORE_FILE) -> bool:
    """Ghi điểm cao nhất ra file. Trả về True nếu ghi thành công."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"highscore": int(score)}, f)
    except (OSError, ValueError, TypeError):
        return False
    return True


class Game:
    """Điều phối toàn bộ game."""

    def __init__(self, highscore_path: str = config.HIGHSCORE_FILE) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(config.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Điểm cao nhất đọc một lần lúc mở game, ghi lại mỗi khi phá kỷ lục.
        self.highscore_path = highscore_path
        self.highscore = load_highscore(highscore_path)

        # Mức độ khó mặc định, người chơi đổi được ở menu bằng phím 1/2/3.
        self.difficulty_name, self.speed = KEY_TO_DIFFICULTY[pygame.K_2]

        self.state = GameState.MENU
        self.score = 0
        self.new_record = False

        # Thời gian tích luỹ chờ tới bước đi kế tiếp của rắn.
        self.move_timer = 0.0

        # Hàng chờ các hướng người chơi vừa bấm. Xem Game.handle_keydown.
        self.direction_queue: deque[tuple[int, int]] = deque(
            maxlen=DIRECTION_QUEUE_SIZE
        )

        # Tạo sẵn rắn và mồi ngay từ đầu để mọi hàm khác luôn có cái mà dùng,
        # kể cả khi người chơi còn đang ở màn hình menu.
        self.snake = Snake(*START_CELL)
        self.food = Food()
        self.food.respawn(self.snake.body)

    # --- Bắt đầu và kết thúc một ván --------------------------------------

    def reset_round(self) -> None:
        """Dọn sạch mọi thứ để bắt đầu một ván mới."""
        self.score = 0
        self.new_record = False
        self.move_timer = 0.0
        self.direction_queue.clear()
        self.snake = Snake(*START_CELL)
        self.food.respawn(self.snake.body)
        self.state = GameState.PLAYING

    def end_round(self) -> None:
        """Kết thúc ván: chuyển sang GAME_OVER và lưu kỷ lục nếu có."""
        self.state = GameState.GAME_OVER
        self.new_record = self.score > self.highscore
        if self.new_record:
            self.highscore = self.score
            save_highscore(self.highscore, self.highscore_path)

    # --- Nhận phím ---------------------------------------------------------

    def handle_events(self) -> None:
        """Đọc bàn phím và sự kiện đóng cửa sổ."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """Xử lý một phím vừa được bấm, tuỳ theo trạng thái hiện tại.

        Về hàng chờ hướng đi: nếu người chơi bấm rất nhanh LÊN rồi TRÁI trong
        cùng một bước đi, mà ta áp dụng cả hai ngay lập tức, thì rắn đang đi
        PHẢI sẽ nhận LÊN (hợp lệ) rồi nhận luôn TRÁI (lúc này cũng hợp lệ vì
        rắn chưa kịp nhúc nhích) — kết quả là rắn quay ngược 180 độ và tự cắn
        mình. Vì vậy phím được xếp vào hàng chờ, mỗi bước đi chỉ lấy ra đúng
        một hướng. Hàng chờ giới hạn 2 phần tử để rắn không đi theo những phím
        bấm từ lâu lắc.
        """
        if key == pygame.K_ESCAPE:
            self.running = False

        elif self.state is GameState.MENU:
            if key in KEY_TO_DIFFICULTY:
                self.difficulty_name, self.speed = KEY_TO_DIFFICULTY[key]
            elif key == pygame.K_SPACE:
                self.reset_round()

        elif self.state is GameState.PLAYING:
            if key == pygame.K_p:
                self.state = GameState.PAUSED
            elif key in KEY_TO_DIRECTION:
                self.direction_queue.append(KEY_TO_DIRECTION[key])

        elif self.state is GameState.PAUSED:
            if key == pygame.K_p:
                self.state = GameState.PLAYING

        elif self.state is GameState.GAME_OVER:
            if key == pygame.K_SPACE:
                self.reset_round()

    # --- Cập nhật ----------------------------------------------------------

    def update(self, dt: float) -> None:
        """Cập nhật trạng thái game.

        Args:
            dt: số giây đã trôi qua kể từ khung hình trước.

        Màn hình vẽ 60 khung hình mỗi giây nhưng rắn chỉ đi ``self.speed`` bước
        mỗi giây, nên không phải khung hình nào rắn cũng nhúc nhích. Ta cộng
        dồn thời gian vào ``move_timer``, đủ một nhịp thì mới cho rắn đi và trừ
        ngược lại đúng một nhịp — phần dư giữ nguyên nên nhịp đi không bị lệch
        dần theo thời gian.
        """
        if self.state is not GameState.PLAYING:
            return

        self.move_timer += dt
        seconds_per_step = 1 / self.speed
        if self.move_timer + EPSILON >= seconds_per_step:
            self.move_timer -= seconds_per_step
            self.step()

    def step(self) -> None:
        """Cho rắn đi đúng một bước.

        Thứ tự ở đây quan trọng. Phải biết trước ô sắp tới có phải miếng mồi
        không rồi mới cho rắn đi, vì lúc đi mới quyết định được là bỏ đuôi hay
        giữ lại. Và phải sinh mồi mới *sau khi* rắn đã dài ra, nếu không mồi
        có thể rơi trúng ngay dưới bụng rắn.
        """
        # Mỗi bước chỉ lấy ra một hướng, xem giải thích ở Game.handle_keydown.
        if self.direction_queue:
            self.snake.change_direction(self.direction_queue.popleft())

        next_cell = self.next_head_cell()
        an_duoc_moi = next_cell == self.food.position

        self.snake.move(grow=an_duoc_moi)

        if an_duoc_moi:
            self.score += config.SCORE_PER_FOOD
            self.food.respawn(self.snake.body)

        if self.hits_wall() or self.snake.hits_self():
            self.end_round()

    def next_head_cell(self) -> tuple[int, int]:
        """Ô mà đầu rắn sẽ tới ở bước kế tiếp."""
        head_x, head_y = self.snake.head
        dx, dy = self.snake.direction
        return head_x + dx, head_y + dy

    def hits_wall(self) -> bool:
        """Trả về True nếu đầu rắn đã ra khỏi lưới."""
        x, y = self.snake.head
        return not (0 <= x < config.GRID_WIDTH and 0 <= y < config.GRID_HEIGHT)

    # --- Vẽ ----------------------------------------------------------------

    def draw(self) -> None:
        """Vẽ khung hình tương ứng với trạng thái hiện tại."""
        ui.draw_grid(self.screen)

        if self.state is GameState.MENU:
            ui.draw_menu(self.screen, self.difficulty_name)
            pygame.display.flip()
            return

        # Ba trạng thái còn lại đều vẽ sân chơi trước, chỉ khác lớp phủ ở trên.
        ui.draw_snake(self.screen, self.snake.body)
        ui.draw_food(self.screen, self.food.position)
        ui.draw_score(self.screen, self.score, self.highscore)

        if self.state is GameState.PAUSED:
            self.draw_paused_overlay()
        elif self.state is GameState.GAME_OVER:
            ui.draw_game_over(
                self.screen, self.score, self.highscore, self.new_record
            )

        pygame.display.flip()

    def draw_paused_overlay(self) -> None:
        """Lớp phủ mờ kèm chữ TAM DUNG khi người chơi bấm P.

        Chữ viết không dấu vì font mặc định của pygame không có glyph tiếng
        Việt. Khi Tín nạp font riêng vào assets/fonts/ thì viết lại có dấu được.
        """
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((*config.COLOR_BACKGROUND, config.UI_OVERLAY_ALPHA))
        self.screen.blit(overlay, (0, 0))

        center_x = config.WINDOW_WIDTH // 2
        center_y = config.WINDOW_HEIGHT // 2
        ui.draw_text(self.screen, "TAM DUNG", 56, (center_x, center_y - 20))
        ui.draw_text(
            self.screen,
            "Nhan P de choi tiep",
            24,
            (center_x, center_y + 25),
            config.COLOR_TEXT_DIM,
        )

    # --- Vòng lặp ----------------------------------------------------------

    def run(self) -> None:
        """Vòng lặp game."""
        while self.running:
            # tick() trả về số mili-giây kể từ lần gọi trước, đổi sang giây.
            dt = self.clock.tick(config.FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
