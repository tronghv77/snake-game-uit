"""Vẽ giao diện: lưới, chữ, menu, màn hình game over.

Người phụ trách: Đặng Đức Tín (26730073)
"""

from __future__ import annotations

import math
import struct

import pygame
from pathlib import Path

from . import config


def draw_grid(surface: pygame.Surface) -> None:
    """Vẽ nền và các đường kẻ lưới."""
    surface.fill(config.COLOR_BACKGROUND)
    for x in range(0, config.WINDOW_WIDTH, config.CELL_SIZE):
        pygame.draw.line(
            surface, config.COLOR_GRID, (x, 0), (x, config.WINDOW_HEIGHT)
        )
    for y in range(0, config.WINDOW_HEIGHT, config.CELL_SIZE):
        pygame.draw.line(
            surface, config.COLOR_GRID, (0, y), (config.WINDOW_WIDTH, y)
        )


def draw_text(
    surface: pygame.Surface,
    text: str,
    size: int,
    center: tuple[int, int],
    color: tuple[int, int, int] = config.COLOR_TEXT,
) -> None:
    """Vẽ một dòng chữ căn giữa tại toạ độ `center`."""
    font = pygame.font.Font(None, size)
    rendered = font.render(text, True, color)
    surface.blit(rendered, rendered.get_rect(center=center))


def draw_snake(surface: pygame.Surface, body: list[tuple[int, int]]) -> None:
    """Vẽ thân rắn lên màn hình."""
    for index, (grid_x, grid_y) in enumerate(body):
        rect = pygame.Rect(
            grid_x * config.CELL_SIZE + config.UI_MARGIN,
            grid_y * config.CELL_SIZE + config.UI_MARGIN,
            config.CELL_SIZE - config.UI_MARGIN * 2,
            config.CELL_SIZE - config.UI_MARGIN * 2,
        )
        color = config.COLOR_SNAKE_HEAD if index == 0 else config.COLOR_SNAKE_BODY
        pygame.draw.rect(surface, color, rect, border_radius=4)

    if body:
        head_x, head_y = body[0]
        eye_y = head_y * config.CELL_SIZE + config.UI_MARGIN + config.CELL_SIZE // 3
        left_eye_x = head_x * config.CELL_SIZE + config.UI_MARGIN + config.CELL_SIZE // 3
        right_eye_x = head_x * config.CELL_SIZE + config.UI_MARGIN + config.CELL_SIZE * 2 // 3
        pygame.draw.circle(surface, config.COLOR_BACKGROUND, (left_eye_x, eye_y), 2)
        pygame.draw.circle(surface, config.COLOR_BACKGROUND, (right_eye_x, eye_y), 2)


def draw_food(surface: pygame.Surface, position: tuple[int, int]) -> None:
    """Vẽ miếng mồi lên màn hình."""
    center = (
        position[0] * config.CELL_SIZE + config.CELL_SIZE // 2,
        position[1] * config.CELL_SIZE + config.CELL_SIZE // 2,
    )
    radius = max(4, config.CELL_SIZE // 2 - 3)
    pygame.draw.circle(surface, config.COLOR_FOOD, center, radius)
    pygame.draw.circle(
        surface,
        config.COLOR_FOOD_HIGHLIGHT,
        (center[0] - radius // 3, center[1] - radius // 3),
        max(2, radius // 4),
    )


def draw_score(surface: pygame.Surface, score: int, highscore: int) -> None:
    """Hiển thị điểm hiện tại và điểm cao nhất ở góc màn hình."""
    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Diem: {score}", True, config.COLOR_TEXT)
    highscore_text = font.render(
        f"Cao nhat: {highscore}", True, config.COLOR_TEXT_DIM
    )
    surface.blit(score_text, (10, 7))
    surface.blit(
        highscore_text,
        (config.WINDOW_WIDTH - highscore_text.get_width() - 10, 7),
    )


def draw_menu(surface: pygame.Surface, difficulty_name: str) -> None:
    """Màn hình menu: tên game, hướng dẫn chọn độ khó, phím bắt đầu."""
    _draw_panel(surface, 110, 55, config.WINDOW_WIDTH - 220, config.WINDOW_HEIGHT - 110)
    center_x = config.WINDOW_WIDTH // 2
    draw_text(surface, "SNAKE GAME", 58, (center_x, 125), config.COLOR_ACCENT)
    draw_text(surface, "NHOM 3 - UIT", 25, (center_x, 165), config.COLOR_TEXT_DIM)
    draw_text(surface, "Chon do kho: 1 - De   2 - Thuong   3 - Kho", 24,
              (center_x, 235), config.COLOR_TEXT)
    draw_text(surface, f"Do kho: {difficulty_name}", 24,
              (center_x, 265), config.COLOR_ACCENT)
    draw_text(surface, "Mui ten / WASD de di chuyen", 22,
              (center_x, 295), config.COLOR_TEXT_DIM)
    draw_text(surface, "Nhan SPACE de bat dau", 26,
              (center_x, 335), config.COLOR_SNAKE_HEAD)
    draw_text(surface, "ESC de thoat", 20, (center_x, 355), config.COLOR_TEXT_DIM)
    draw_text(surface, "Ho Van Trong - Le Kieu Diem - Dang Duc Tin", 16,
              (center_x, 415), config.COLOR_TEXT_DIM)


def draw_game_over(
    surface: pygame.Surface, score: int, highscore: int, new_record: bool
) -> None:
    """Màn hình kết thúc: điểm đạt được, phím chơi lại, phím thoát."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((*config.COLOR_BACKGROUND, config.UI_OVERLAY_ALPHA))
    surface.blit(overlay, (0, 0))
    panel_width = config.WINDOW_WIDTH - 240
    panel_height = 290
    panel_x = (config.WINDOW_WIDTH - panel_width) // 2
    panel_y = (config.WINDOW_HEIGHT - panel_height) // 2
    _draw_panel(surface, panel_x, panel_y, panel_width, panel_height)
    center_x = config.WINDOW_WIDTH // 2
    draw_text(surface, "GAME OVER", 52, (center_x, panel_y + 55), config.COLOR_FOOD)
    draw_text(surface, f"Diem cua ban: {score}", 28,
              (center_x, panel_y + 110), config.COLOR_TEXT)
    draw_text(surface, f"Ky luc: {highscore}", 24,
              (center_x, panel_y + 145), config.COLOR_TEXT_DIM)
    if new_record:
        draw_text(surface, "KY LUC MOI!", 24,
                  (center_x, panel_y + 178), config.COLOR_ACCENT)
    draw_text(surface, "SPACE de choi lai", 24,
              (center_x, panel_y + 215), config.COLOR_SNAKE_HEAD)
    draw_text(surface, "ESC de thoat", 20, (center_x, panel_y + 255), config.COLOR_TEXT_DIM)


def _draw_panel(surface: pygame.Surface, x: int, y: int, width: int, height: int) -> None:
    """Vẽ khung nền dùng chung cho menu và game over."""
    panel = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, config.COLOR_PANEL, panel, border_radius=8)
    pygame.draw.rect(surface, config.COLOR_PANEL_BORDER, panel, width=2, border_radius=8)


def load_sound(path: Path) -> pygame.mixer.Sound | None:
    """Tải âm thanh tùy chọn; trả về None nếu mixer/file chưa sẵn sàng."""
    if not config.SOUND_ENABLED:
        return None
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if not path.is_file():
            return _create_fallback_sound(path)
        return pygame.mixer.Sound(str(path))
    except pygame.error:
        return None


def _create_fallback_sound(path: Path) -> pygame.mixer.Sound:
    """Tạo tiếng beep ngắn khi assets chưa có file âm thanh."""
    frequency = 660 if "eat" in path.stem.lower() else 220
    mixer_settings = pygame.mixer.get_init()
    sample_rate = mixer_settings[0] if mixer_settings else 44_100
    channels = mixer_settings[2] if mixer_settings else 2
    duration = 0.12 if frequency > 300 else 0.25
    frame_count = int(sample_rate * duration)
    samples = bytearray()
    for frame in range(frame_count):
        envelope = 1.0 - frame / frame_count
        value = int(8_000 * envelope * math.sin(
            2 * math.pi * frequency * frame / sample_rate
        ))
        samples.extend(struct.pack("<h", value) * channels)
    return pygame.mixer.Sound(buffer=bytes(samples))


def play_sound(sound: pygame.mixer.Sound | None) -> None:
    """Phát âm thanh nếu đã tải thành công."""
    if sound is not None:
        channel = pygame.mixer.find_channel(force=True)
        if channel is not None:
            channel.play(sound)
