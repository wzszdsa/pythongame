class BlockType:
    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    CYAN = 4
    BLUE = 5
    PURPLE = 6
    BLOCKMAX = 7


class BlockGroupType:
    FIXED = 0
    DROP = 1


BLOCK_RES = {
    BlockType.RED: "../img/red.png",
    BlockType.ORANGE: "../img/orange.png",
    BlockType.YELLOW: "../img/yellow.png",
    BlockType.GREEN: "../img/green.png",
    BlockType.CYAN: "../img/cyan.png",
    BlockType.BLUE: "../img/blue.png",
    BlockType.PURPLE: "../img/purple.png",
}

GAME_ROW = 17
GAME_COL = 10
GAME_WIDTH_SIZE = 800
GAME_HEIGHT_SIZE = 600
BLOCK_SIZE_W = 32
BLOCK_SIZE_H = 32

BLOCK_SHAPE = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],  # 方形
    [((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 0), (1, 0), (2, 0), (3, 0))],  # 长条
    [((0, 0), (0, 1), (1, 1), (1, 2)), ((0, 1), (1, 0), (1, 1), (2, 0))],  # z字形
    [((0, 1), (1, 0), (1, 1), (1, 2)), ((0, 1), (1, 1), (1, 2), (2, 1)), ((1, 0), (1, 1), (1, 2), (2, 1)),
     ((0, 1), (1, 0), (1, 1), (2, 1))],  # 飞机型

]
