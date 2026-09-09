"""Các hằng số cấu hình của game.

Người phụ trách: Đặng Đức Tín (26730073)

Mọi con số "ma thuật" (magic number) đều nên đặt tên ở đây thay vì viết
thẳng trong code, để cả nhóm chỉnh một chỗ là toàn bộ game đổi theo.
"""

from pathlib import Path

# --- Kích thước cửa sổ và lưới -------------------------------------------
CELL_SIZE = 20          # Kích thước một ô vuông (pixel)
GRID_WIDTH = 30         # Số ô theo chiều ngang
GRID_HEIGHT = 22        # Số ô theo chiều dọc

WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

WINDOW_TITLE = "Snake Game - Nhom 3 - UIT"

# --- Giao diện ------------------------------------------------------------
UI_MARGIN = 2
UI_OVERLAY_ALPHA = 130
UI_SCORE_BAR_HEIGHT = 34
UI_SCORE_BAR_PADDING = 10
COLOR_PANEL = (12, 17, 24)
COLOR_PANEL_BORDER = (70, 88, 104)
COLOR_ACCENT = (255, 205, 92)
COLOR_FOOD_HIGHLIGHT = (255, 146, 146)

# --- Tốc độ ---------------------------------------------------------------
FPS = 60                # Số khung hình mỗi giây

# Số bước rắn đi được trong 1 giây, ứng với từng mức độ khó
SPEED_EASY = 8
SPEED_NORMAL = 12
SPEED_HARD = 18

# --- Màu sắc (R, G, B) ----------------------------------------------------
COLOR_BACKGROUND = (18, 24, 32)
COLOR_GRID = (28, 36, 46)
COLOR_SNAKE_HEAD = (86, 214, 122)
COLOR_SNAKE_BODY = (58, 168, 96)
COLOR_FOOD = (232, 84, 84)
COLOR_TEXT = (236, 240, 244)
COLOR_TEXT_DIM = (140, 152, 166)

# --- Điểm số --------------------------------------------------------------
SCORE_PER_FOOD = 10
HIGHSCORE_FILE = "highscore.json"

# --- Tài nguyên -----------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"
SOUNDS_DIR = ASSETS_DIR / "sounds"
FONTS_DIR = ASSETS_DIR / "fonts"
FONT_CANDIDATES = [
    FONTS_DIR / "SegoeUI.ttf",
    FONTS_DIR / "NotoSansVN-Regular.ttf",
    FONTS_DIR / "NotoSans-Regular.ttf",
    Path("C:/Windows/Fonts/SegoeUI.ttf"),
    Path("C:/Windows/Fonts/segoeui.ttf"),
    Path("C:/Windows/Fonts/arial.ttf"),
]
FONT_PATH = next((path for path in FONT_CANDIDATES if path.exists()), None)
SOUND_EAT_PATH = SOUNDS_DIR / "eat.wav"
SOUND_GAME_OVER_PATH = SOUNDS_DIR / "game_over.wav"
SOUND_ENABLED = True
