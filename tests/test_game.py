"""Kiểm thử phần lõi điều khiển game — T1, T2, T3, T5.

Người phụ trách: Hồ Văn Trọng (26730077)

Chạy:  python -m pytest tests/test_game.py -v
"""

import os
import sys
from pathlib import Path

# Chạy pygame ở chế độ không cần màn hình để test chạy được cả trên máy chủ CI.
# Phải đặt trước khi import pygame.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pygame  # noqa: E402
import pytest  # noqa: E402

from snake import config  # noqa: E402
from snake.game import (  # noqa: E402
    KEY_TO_DIFFICULTY,
    KEY_TO_DIRECTION,
    Game,
    GameState,
    load_highscore,
    save_highscore,
)
from snake.snake import DOWN, LEFT, RIGHT, UP  # noqa: E402


@pytest.fixture
def game(tmp_path):
    """Một game mới tinh, điểm cao nhất ghi vào thư mục tạm của test."""
    g = Game(highscore_path=str(tmp_path / "highscore.json"))
    yield g
    pygame.quit()


# --- T1: quản lý trạng thái ------------------------------------------------


def test_mo_game_len_thay_menu_truoc(game):
    assert game.state is GameState.MENU


def test_space_o_menu_thi_vao_choi(game):
    game.handle_keydown(pygame.K_SPACE)
    assert game.state is GameState.PLAYING


def test_phim_p_tam_dung_roi_choi_tiep(game):
    game.handle_keydown(pygame.K_SPACE)
    game.handle_keydown(pygame.K_p)
    assert game.state is GameState.PAUSED
    game.handle_keydown(pygame.K_p)
    assert game.state is GameState.PLAYING


def test_phim_p_khong_lam_gi_o_menu(game):
    game.handle_keydown(pygame.K_p)
    assert game.state is GameState.MENU


def test_dang_tam_dung_thi_ran_khong_di(game):
    game.handle_keydown(pygame.K_SPACE)
    game.handle_keydown(pygame.K_p)
    da_di = []
    game.step = lambda: da_di.append(1)
    game.update(10.0)  # thời gian rất dài, đủ cho hàng chục bước
    assert da_di == []


def test_escape_thoat_game_o_moi_trang_thai(game):
    for state in GameState:
        game.state = state
        game.running = True
        game.handle_keydown(pygame.K_ESCAPE)
        assert game.running is False, f"ESC khong thoat duoc o {state}"


def test_thua_roi_bam_space_thi_choi_lai(game):
    game.handle_keydown(pygame.K_SPACE)
    game.score = 70
    game.end_round()
    assert game.state is GameState.GAME_OVER

    game.handle_keydown(pygame.K_SPACE)
    assert game.state is GameState.PLAYING
    assert game.score == 0
    assert game.move_timer == 0
    assert len(game.direction_queue) == 0


# --- T2: nhận phím ---------------------------------------------------------


def test_du_8_phim_deu_map_dung_huong():
    assert KEY_TO_DIRECTION[pygame.K_UP] == UP
    assert KEY_TO_DIRECTION[pygame.K_w] == UP
    assert KEY_TO_DIRECTION[pygame.K_DOWN] == DOWN
    assert KEY_TO_DIRECTION[pygame.K_s] == DOWN
    assert KEY_TO_DIRECTION[pygame.K_LEFT] == LEFT
    assert KEY_TO_DIRECTION[pygame.K_a] == LEFT
    assert KEY_TO_DIRECTION[pygame.K_RIGHT] == RIGHT
    assert KEY_TO_DIRECTION[pygame.K_d] == RIGHT


def test_bam_phim_luc_dang_choi_thi_vao_hang_cho(game):
    game.handle_keydown(pygame.K_SPACE)
    game.handle_keydown(pygame.K_UP)
    assert list(game.direction_queue) == [UP]


def test_bam_hai_phim_that_nhanh_thi_giu_ca_hai(game):
    """Đây là ca chống lỗi rắn quay ngược 180 độ rồi tự cắn mình."""
    game.handle_keydown(pygame.K_SPACE)
    game.handle_keydown(pygame.K_UP)
    game.handle_keydown(pygame.K_LEFT)
    assert list(game.direction_queue) == [UP, LEFT]


def test_hang_cho_chi_giu_toi_da_hai_huong(game):
    game.handle_keydown(pygame.K_SPACE)
    for key in (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT):
        game.handle_keydown(key)
    assert list(game.direction_queue) == [DOWN, RIGHT]


def test_bam_huong_o_menu_thi_khong_vao_hang_cho(game):
    game.handle_keydown(pygame.K_UP)
    assert len(game.direction_queue) == 0


def test_moi_buoc_di_lay_ra_dung_mot_huong(game):
    game.handle_keydown(pygame.K_SPACE)
    game.handle_keydown(pygame.K_UP)
    game.handle_keydown(pygame.K_LEFT)

    game.step()
    assert list(game.direction_queue) == [LEFT]
    game.step()
    assert list(game.direction_queue) == []


def test_handle_events_doc_duoc_phim_tu_hang_doi(game):
    """Chứng minh handle_events nối đúng vào hàng đợi sự kiện của pygame."""
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    game.handle_events()
    assert game.state is GameState.PLAYING


def test_dong_cua_so_thi_thoat_game(game):
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.handle_events()
    assert game.running is False


# --- T3: nhịp đi của rắn ---------------------------------------------------


def test_chon_do_kho_bang_phim_1_2_3(game):
    game.handle_keydown(pygame.K_1)
    assert game.speed == config.SPEED_EASY
    game.handle_keydown(pygame.K_3)
    assert game.speed == config.SPEED_HARD
    game.handle_keydown(pygame.K_2)
    assert game.speed == config.SPEED_NORMAL


def test_ba_muc_do_kho_deu_co_ten_hien_thi():
    for key, (ten, toc_do) in KEY_TO_DIFFICULTY.items():
        assert ten, f"muc do kho cua phim {key} chua co ten"
        assert toc_do > 0


def test_chua_du_mot_nhip_thi_ran_chua_di(game):
    game.handle_keydown(pygame.K_SPACE)
    game.speed = 10  # mỗi bước cách nhau 0.1 giây
    da_di = []
    game.step = lambda: da_di.append(1)

    game.update(0.05)
    assert da_di == []
    game.update(0.04)
    assert da_di == []
    game.update(0.01)  # tổng đúng 0.1 giây
    assert len(da_di) == 1


def test_phan_du_thoi_gian_khong_bi_mat(game):
    """Nhịp đi không được lệch dần theo thời gian."""
    game.handle_keydown(pygame.K_SPACE)
    game.speed = 10
    da_di = []
    game.step = lambda: da_di.append(1)

    game.update(0.15)  # đi 1 bước, còn dư 0.05 giây
    assert len(da_di) == 1
    assert game.move_timer == pytest.approx(0.05)

    game.update(0.05)  # 0.05 dư cộng 0.05 mới là đủ nhịp
    assert len(da_di) == 2


def test_ran_di_dung_so_buoc_trong_mot_giay(game):
    """Chạy giả lập 1 giây ở 60 khung hình, đếm số bước rắn đi được."""
    game.handle_keydown(pygame.K_SPACE)
    game.speed = config.SPEED_NORMAL
    da_di = []
    game.step = lambda: da_di.append(1)

    for _ in range(60):
        game.update(1 / 60)

    assert len(da_di) == config.SPEED_NORMAL


# --- T5: điểm cao nhất -----------------------------------------------------


def test_luu_roi_doc_lai_duoc(tmp_path):
    p = str(tmp_path / "hs.json")
    assert save_highscore(120, p) is True
    assert load_highscore(p) == 120


def test_file_chua_ton_tai_thi_tra_ve_0(tmp_path):
    assert load_highscore(str(tmp_path / "chua-co.json")) == 0


def test_file_hong_thi_tra_ve_0_chu_khong_crash(tmp_path):
    p = tmp_path / "hs.json"
    p.write_text("day khong phai json", encoding="utf-8")
    assert load_highscore(str(p)) == 0


def test_file_thieu_khoa_highscore_thi_tra_ve_0(tmp_path):
    p = tmp_path / "hs.json"
    p.write_text('{"diem": 50}', encoding="utf-8")
    assert load_highscore(str(p)) == 0


def test_diem_am_trong_file_thi_tra_ve_0(tmp_path):
    p = tmp_path / "hs.json"
    p.write_text('{"highscore": -99}', encoding="utf-8")
    assert load_highscore(str(p)) == 0


def test_pha_ky_luc_thi_luu_lai(game):
    game.highscore = 50
    game.score = 80
    game.end_round()

    assert game.new_record is True
    assert game.highscore == 80
    assert load_highscore(game.highscore_path) == 80


def test_khong_pha_ky_luc_thi_giu_nguyen(game):
    game.highscore = 50
    game.score = 30
    game.end_round()

    assert game.new_record is False
    assert game.highscore == 50


def test_bang_diem_ky_luc_khong_tinh_la_pha_ky_luc(game):
    game.highscore = 50
    game.score = 50
    game.end_round()
    assert game.new_record is False


def test_choi_van_moi_thi_xoa_co_ky_luc(game):
    game.score = 90
    game.end_round()
    assert game.new_record is True
    game.reset_round()
    assert game.new_record is False


def test_mo_game_doc_lai_duoc_ky_luc_cu(tmp_path):
    p = str(tmp_path / "hs.json")
    save_highscore(250, p)
    g = Game(highscore_path=p)
    assert g.highscore == 250
    pygame.quit()
