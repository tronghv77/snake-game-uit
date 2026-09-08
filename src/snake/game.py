"""Vòng lặp chính, trạng thái game, xử lý va chạm và tính điểm.

Người phụ trách: Hồ Văn Trọng (26730077)

Tình trạng hiện tại:
    Đã xong  T1 quản lý trạng thái, T2 nhận phím, T3 nhịp đi, T5 điểm cao nhất.
    Còn chờ  T4 ăn mồi và va chạm — cần lớp Snake và Food của Diễm.

Mọi chỗ còn thiếu đều được đánh dấu ``TODO(T4)``. Tìm theo từ khoá đó là ra
đủ các điểm cần nối vào khi phần của Diễm xong.
"""

from __future__ import annotations

import json
from collections import deque
from enum import Enum, auto

import pygame

from . import config, ui
from .snake import DOWN, LEFT, RIGHT, UP

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

        # TODO(T4): self.snake = Snake(...) và self.food = Food()

    # --- Bắt đầu và kết thúc một ván --------------------------------------

    def reset_round(self) -> None:
        """Dọn sạch mọi thứ để bắt đầu một ván mới."""
        self.score = 0
        self.new_record = False
        self.move_timer = 0.0
        self.direction_queue.clear()
        self.state = GameState.PLAYING

        # TODO(T4): tạo lại self.snake ở giữa lưới và gọi self.food.respawn()

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
        """Cho rắn đi đúng một bước."""
        if self.direction_queue:
            _next_direction = self.direction_queue.popleft()
            # TODO(T4): self.snake.change_direction(_next_direction)

        # TODO(T4): tính ô đầu rắn sắp tới, so với self.food.position để biết
        # có ăn được không, gọi self.snake.move(grow), cộng điểm và sinh mồi
        # mới, rồi kiểm tra va chạm tường và self.snake.hits_self() —
        # trúng thì gọi self.end_round().

    # --- Vẽ ----------------------------------------------------------------

    def draw(self) -> None:
        """Vẽ khung hình tương ứng với trạng thái hiện tại."""
        ui.draw_grid(self.screen)

        if self.state is GameState.MENU:
            self.draw_menu_tam()
        elif self.state is GameState.GAME_OVER:
            self.draw_game_over_tam()
        else:
            self.draw_playing_tam()

        pygame.display.flip()

    # Ba hàm dưới đây chỉ là màn hình tạm để chạy thử phần trạng thái. Khi Tín
    # làm xong N3, N4, N5 thì xoá cả ba và gọi thẳng ui.draw_menu(),
    # ui.draw_game_over(), ui.draw_snake(), ui.draw_food(), ui.draw_score().
    #
    # Chữ ở đây cố tình viết không dấu vì font mặc định của pygame không có
    # glyph tiếng Việt, để nguyên dấu sẽ ra ô vuông. Tín nạp font riêng ở N6
    # xong thì viết lại có dấu được.

    def draw_menu_tam(self) -> None:
        cx = config.WINDOW_WIDTH // 2
        ui.draw_text(self.screen, "SNAKE GAME", 64, (cx, 90))
        ui.draw_text(
            self.screen, "Nhom 3 - UIT", 26, (cx, 130), config.COLOR_TEXT_DIM
        )
        ui.draw_text(
            self.screen, f"Do kho: {self.difficulty_name}", 34, (cx, 200)
        )
        ui.draw_text(
            self.screen,
            "1 - De     2 - Thuong     3 - Kho",
            24,
            (cx, 235),
            config.COLOR_TEXT_DIM,
        )
        ui.draw_text(self.screen, "SPACE de bat dau", 30, (cx, 300))
        ui.draw_text(
            self.screen,
            "Mui ten hoac WASD de dieu khien - P tam dung - ESC thoat",
            20,
            (cx, 335),
            config.COLOR_TEXT_DIM,
        )
        ui.draw_text(
            self.screen,
            f"Ky luc: {self.highscore}",
            24,
            (cx, 385),
            config.COLOR_TEXT_DIM,
        )
        ui.draw_text(
            self.screen,
            "Ho Van Trong - Le Kieu Diem - Dang Duc Tin",
            20,
            (cx, config.WINDOW_HEIGHT - 25),
            config.COLOR_TEXT_DIM,
        )

    def draw_playing_tam(self) -> None:
        cx = config.WINDOW_WIDTH // 2
        ui.draw_text(
            self.screen,
            f"Diem: {self.score}    Ky luc: {self.highscore}",
            26,
            (cx, 24),
        )
        ui.draw_text(
            self.screen,
            "Cho lop Snake va Food cua Diem (issue #2, #3)",
            24,
            (cx, config.WINDOW_HEIGHT // 2),
            config.COLOR_TEXT_DIM,
        )
        if self.state is GameState.PAUSED:
            ui.draw_text(
                self.screen, "TAM DUNG", 56, (cx, config.WINDOW_HEIGHT // 2 - 60)
            )
            ui.draw_text(
                self.screen,
                "P de choi tiep",
                24,
                (cx, config.WINDOW_HEIGHT // 2 - 20),
                config.COLOR_TEXT_DIM,
            )

    def draw_game_over_tam(self) -> None:
        cx = config.WINDOW_WIDTH // 2
        cy = config.WINDOW_HEIGHT // 2
        ui.draw_text(self.screen, "GAME OVER", 64, (cx, cy - 70))
        ui.draw_text(self.screen, f"Diem: {self.score}", 34, (cx, cy - 10))
        if self.new_record:
            ui.draw_text(self.screen, "KY LUC MOI!", 30, (cx, cy + 30))
        else:
            ui.draw_text(
                self.screen,
                f"Ky luc: {self.highscore}",
                26,
                (cx, cy + 30),
                config.COLOR_TEXT_DIM,
            )
        ui.draw_text(
            self.screen,
            "SPACE de choi lai - ESC de thoat",
            24,
            (cx, cy + 85),
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
