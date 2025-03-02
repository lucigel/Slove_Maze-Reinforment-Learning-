import numpy as np
import matplotlib.pyplot as plt
import random

# Kích thước mê cung (phải là số lẻ)
WIDTH, HEIGHT = 21, 21  

# Hướng di chuyển
DIRECTIONS = {
    (0, -1): "U", (0, 1): "D",
    (-1, 0): "L", (1, 0): "R"
}
MOVES = list(DIRECTIONS.keys())

def create_maze_wilson(width, height):
    """ Tạo mê cung bằng Wilson’s Algorithm (Fixed) """
    maze = np.ones((height, width), dtype=int)  # Tất cả là tường (1)

    # Chọn ô đầu tiên làm cây
    tree = set()
    start_x, start_y = random.randrange(1, width, 2), random.randrange(1, height, 2)
    tree.add((start_x, start_y))
    maze[start_y, start_x] = 0  

    # Tạo danh sách ô còn lại
    unvisited = {(x, y) for x in range(1, width, 2) for y in range(1, height, 2)}
    unvisited.remove((start_x, start_y))

    while unvisited:
        # Chọn một ô chưa thăm
        current = random.choice(list(unvisited))
        path = [current]  # Lưu đường đi

        # Walk ngẫu nhiên đến khi gặp cây
        while path[-1] not in tree:
            move = random.choice(MOVES)
            next_x, next_y = path[-1][0] + move[0] * 2, path[-1][1] + move[1] * 2

            # Kiểm tra hợp lệ
            if (1 <= next_x < width - 1 and 1 <= next_y < height - 1):
                if (next_x, next_y) in path:  # Nếu có vòng lặp, cắt bỏ phần lặp
                    loop_start = path.index((next_x, next_y))
                    path = path[:loop_start + 1]
                else:
                    path.append((next_x, next_y))

        # Thêm đường đi vào cây
        for i in range(len(path) - 1):
            pos, next_pos = path[i], path[i + 1]
            tree.add(pos)
            tree.add(next_pos)
            maze[pos[1], pos[0]] = 0
            maze[next_pos[1], next_pos[0]] = 0

            # Mở tường giữa 2 ô
            wall_x, wall_y = (pos[0] + next_pos[0]) // 2, (pos[1] + next_pos[1]) // 2
            maze[wall_y, wall_x] = 0

        unvisited -= tree  # Cập nhật ô chưa thăm

    return maze, (start_x, start_y)

def find_end_point(maze, start):
    """ Tìm điểm kết thúc ở rìa dưới hoặc bên phải của mê cung """
    height, width = maze.shape
    possible_ends = [(x, y) for x in range(width) for y in range(height) 
                     if maze[y, x] == 0 and (x == width - 2 or y == height - 2)]
    return random.choice(possible_ends)

def display_maze(maze, start, end):
    plt.figure(figsize=(10, 10))
    plt.imshow(maze, cmap="gray_r", interpolation="nearest")

    # Đánh dấu điểm bắt đầu (màu xanh)
    plt.scatter(start[0], start[1], color="green", s=200, label="Start", edgecolors="black")

    # Đánh dấu điểm kết thúc (màu đỏ)
    plt.scatter(end[0], end[1], color="red", s=200, label="End", edgecolors="black")

    plt.legend()
    plt.xticks([]), plt.yticks([])  
    plt.title("Maze Generated using Wilson's Algorithm (Fixed)")
    plt.show()

# Tạo mê cung và đặt điểm bắt đầu/kết thúc
maze, start = create_maze_wilson(WIDTH, HEIGHT)
end = find_end_point(maze, start)

# Hiển thị mê cung
display_maze(maze, start, end)
