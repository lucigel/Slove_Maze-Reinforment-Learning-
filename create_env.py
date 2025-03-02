import numpy as np 
import gym 
from gym import spaces

# import my module
from generate_maze import create_maze

WIDTH = 9 
HEIGHT = 9 

DIRECTIONS = [(-2, 0), (2, 0), (0, 2), (0, -2)] # LEFT, RIGHT, DOWN, UP

class MazeEnv(gym.Env):
    """Môi trường Gym tùy chỉnh cho mê cung"""
    def __init__(self, width=9, height=9):
        super(MazeEnv, self).__init__()
        self.width = width
        self.height = height
        self.maze, _ = create_maze_dfs(width, height)
        self.start_pos = (1, 1)
        self.goal_pos = (height - 2, width - 2)
        self.agent_pos = self.start_pos
        
        # Xác định các hành động: 0=Up, 1=Down, 2=Left, 3=Right
        self.action_space = spaces.Discrete(4)
        
        # Trạng thái: ma trận kích thước (height, width)
        self.observation_space = spaces.Box(low=0, high=2, shape=(height, width), dtype=np.int8)

    def step(self, action):
        """Di chuyển AI theo hành động đã chọn"""
        x, y = self.agent_pos
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # (Up, Down, Left, Right)
        dx, dy = moves[action]
        nx, ny = x + dx, y + dy
        
        # Chỉ di chuyển nếu không phải tường
        if 0 <= ny < self.height and 0 <= nx < self.width and self.maze[ny, nx] != 1:
            self.agent_pos = (nx, ny)
        
        # Kiểm tra nếu đến đích
        done = self.agent_pos == self.goal_pos
        reward = 10 if done else -1  # Phạt mỗi bước, thưởng khi đến đích
        
        return self.get_observation(), reward, done, {}

    def reset(self):
        """Đặt lại trạng thái về ban đầu"""
        self.maze, _ = create_maze_dfs(self.width, self.height)
        self.agent_pos = self.start_pos
        return self.get_observation()
    
    def get_observation(self):
        """Trả về trạng thái mê cung"""
        obs = np.copy(self.maze)
        x, y = self.agent_pos
        obs[y, x] = 3  # Đánh dấu vị trí AI
        gx, gy = self.goal_pos
        obs[gy, gx] = 2  # Đánh dấu điểm đến
        return obs

    def render(self):
        """Hiển thị mê cung"""
        symbols = {0: ' ', 1: '#', 2: 'G', 3: 'A'}
        for row in self.get_observation():
            print("".join(symbols[cell] for cell in row))
        print("\n")