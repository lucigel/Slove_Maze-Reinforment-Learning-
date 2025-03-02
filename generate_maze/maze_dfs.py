import numpy as np 
import matplotlib.pyplot as plt 
import random 

WIDTH = 21 
HEIGHT = 21 

DIRECTIONS = [(-2, 0), (2, 0), (0, 2), (0, -2)] # LEFT, RIGHT, DOWN, UP

def create_maze_dfs(width, height):
    # initial maze fill all of wall(1)
    maze = np.ones((height, width), dtype=int) 
    # pos start
    start_x, start_y = random.randrange(1, width, 2), random.randrange(1, height, 2)

    maze[start_y, start_x] = 0 
    stack = [(start_x, start_y)]

    while stack:
        x, y = stack[-1]
        random.shuffle(DIRECTIONS)
        
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            wx, wy = x + dx//2, y + dy//2

            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny, nx] == 1:
                maze[wy, wx] = 0
                maze[ny, nx] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()

    return maze, (start_x, start_y)

def find_end_point(maze):
    """ Tìm điểm kết thúc ở rìa dưới hoặc bên phải của mê cung """
    height, width = maze.shape
    possible_ends = [(x, y) for x in range(width) for y in range(height) 
                     if maze[y, x] == 0 and (x == width - 2 or y == height - 2)]
    return random.choice(possible_ends)  # choose end point

def display_maze(maze, start, end):
    plt.figure(figsize=(10, 10))
    plt.imshow(maze, cmap="gray_r", interpolation="nearest")

    # mark start point is green
    plt.scatter(start[0], start[1], color="green", s=200, label="Start", edgecolors="black")

    # mark end point is red
    plt.scatter(end[0], end[1], color="red", s=200, label="End", edgecolors="black")

    plt.legend()
    plt.xticks([]), plt.yticks([])  
    plt.title("Maze Generated using DFS Algorithm")
    plt.show()


if __name__ == "__main__":
    maze, start = create_maze_dfs(WIDTH, HEIGHT)
    end = find_end_point(maze)
    display_maze(maze, start, end)





