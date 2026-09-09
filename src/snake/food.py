"""Đối tượng mồi.

Người phụ trách: Lê Kiều Diễm (26730010)
"""

from __future__ import annotations

import random

from . import config


class Food:
    """Quản lý vị trí miếng mồi trên lưới."""

    def __init__(self) -> None:
        self.position: tuple[int, int] = (0, 0)

    def respawn(self, occupied: list[tuple[int, int]]) -> None:
        """Đặt mồi vào một ô trống ngẫu nhiên.

        Args:
            occupied: danh sách các ô đang bị thân rắn chiếm. Mồi tuyệt đối
                không được sinh trùng lên các ô này.
        """
        # TODO(Diễm): tạo danh sách tất cả các ô hợp lệ trong lưới
        # (0 <= x < config.GRID_WIDTH, 0 <= y < config.GRID_HEIGHT),
        # loại bỏ các ô trong `occupied`, rồi random.choice() một ô.
        # Tạo danh sách tất cả các ô hợp lệ trong lưới
        all_cells = [(x, y) for x in range(config.GRID_WIDTH) for y in range(config.GRID_HEIGHT)]
        
        # Lọc bỏ các ô đang bị thân rắn chiếm dụng
        available_cells = [cell for cell in all_cells if cell not in occupied]
        
        # Chọn ngẫu nhiên một ô trống để đặt mồi mới
        if available_cells:
            self.position = random.choice(available_cells)
