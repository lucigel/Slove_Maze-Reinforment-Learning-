import numpy as np
import matplotlib.pyplot as plt
import random

# Kích thước mê cung
WIDTH, HEIGHT = 21, 21  

# Hướng di chuyển (theo bước nhảy 2 ô)
DIRECTIONS = [(0, -2), (0, 2), (-2, 0), (2, 0)]

def create_maze_prim(width, height):
    """ Tạo mê cung sử dụng thuật toán Prim """
    maze = np.ones((height, width), dtype=int)  # Toàn bộ là tường (1)

    # Chọn điểm bắt đầu ngẫu nhiên (phải là số lẻ)
    start_x, start_y = random.randrange(1, width, 2), random.randrange(1, height, 2)
    maze[start_y, start_x] = 0  
    walls = [(start_x + dx, start_y + dy, start_x, start_y) for dx, dy in DIRECTIONS if 1 <= start_x + dx < width-1 and 1 <= start_y + dy < height-1]

    while walls:
        wx, wy, px, py = random.choice(walls)
        walls.remove((wx, wy, px, py))

        if maze[wy, wx] == 1:  
            maze[wy, wx] = 0
            maze[(wy + py) // 2, (wx + px) // 2] = 0  

            # Thêm các cạnh mới vào danh sách
            for dx, dy in DIRECTIONS:
                nx, ny = wx + dx, wy + dy
                if 1 <= nx < width-1 and 1 <= ny < height-1 and maze[ny, nx] == 1:
                    walls.append((nx, ny, wx, wy))

    return maze, (start_x, start_y)

def find_end_point(maze, start):
    """ Tìm điểm kết thúc ở rìa dưới hoặc bên phải của mê cung """
    height, width = maze.shape
    possible_ends = [(x, y) for x in range(width) for y in range(height) 
                     if maze[y, x] == 0 and (x == width - 2 or y == height - 2)]
    return random.choice(possible_ends)  # Chọn ngẫu nhiên điểm kết thúc

def display_maze(maze, start, end):
    plt.figure(figsize=(10, 10))
    plt.imshow(maze, cmap="gray_r", interpolation="nearest")

    # Đánh dấu điểm bắt đầu (màu xanh)
    plt.scatter(start[0], start[1], color="green", s=200, label="Start", edgecolors="black")

    # Đánh dấu điểm kết thúc (màu đỏ)
    plt.scatter(end[0], end[1], color="red", s=200, label="End", edgecolors="black")

    plt.legend()
    plt.xticks([]), plt.yticks([])  
    plt.title("Maze Generated using Prim's Algorithm")
    plt.show()

# Tạo mê cung và đặt điểm bắt đầu/kết thúc
maze, start = create_maze_prim(WIDTH, HEIGHT)
end = find_end_point(maze, start)

# Hiển thị mê cung
display_maze(maze, start, end)
