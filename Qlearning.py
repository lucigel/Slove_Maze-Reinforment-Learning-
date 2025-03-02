class QLearningAgent:
    def __init__(self, maze, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.maze = maze
        self.height, self.width = maze.shape
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

        # Khởi tạo Q-table: Mỗi ô sẽ có 4 giá trị ứng với 4 hướng đi (Up, Down, Left, Right)
        self.q_table = np.zeros((self.height, self.width, 4))

    def get_valid_actions(self, x, y):
        """Lấy các hành động hợp lệ (không đi vào tường)"""
        actions = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for i, (dx, dy) in enumerate(moves):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.height and 0 <= ny < self.width and self.maze[nx, ny] == 0:
                actions.append(i)

        return actions

    def choose_action(self, x, y):
        """Chọn hành động theo Q-Learning (Exploration vs Exploitation)"""
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.get_valid_actions(x, y))  # Chọn ngẫu nhiên
        else:
            return np.argmax(self.q_table[x, y])  # Chọn hành động có giá trị Q cao nhất

    def update_q_table(self, x, y, action, reward, next_x, next_y):
        """Cập nhật giá trị Q-table dựa trên trải nghiệm"""
        best_next_q = np.max(self.q_table[next_x, next_y])  # Giá trị Q tốt nhất của trạng thái tiếp theo
        current_q = self.q_table[x, y, action]

        # Công thức cập nhật Q-Learning
        self.q_table[x, y, action] = (1 - self.alpha) * current_q + self.alpha * (reward + self.gamma * best_next_q)

    def train(self, start, goal, episodes=1000, max_steps=100):
        """Huấn luyện AI tìm đường thoát khỏi mê cung"""
        for episode in range(episodes):
            x, y = start
            for _ in range(max_steps):
                action = self.choose_action(x, y)

                # Thực hiện di chuyển
                moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                dx, dy = moves[action]
                nx, ny = x + dx, y + dy

                # Kiểm tra điều kiện dừng
                if (nx, ny) == goal:
                    reward = 100  # Thưởng lớn nếu AI tìm thấy lối ra
                    self.update_q_table(x, y, action, reward, nx, ny)
                    break
                elif self.maze[nx, ny] == 1:
                    reward = -10  # Phạt nếu đâm vào tường
                else:
                    reward = -1  # Phạt nhẹ để khuyến khích đi nhanh

                # Cập nhật Q-table
                self.update_q_table(x, y, action, reward, nx, ny)
                x, y = nx, ny

            if (episode + 1) % 100 == 0:
                print(f"Episode {episode + 1}/{episodes} - AI đang học...")

    def solve(self, start, goal):
        """Chạy AI sau khi học xong"""
        x, y = start
        path = [(x, y)]

        for _ in range(100):  # Giới hạn số bước
            action = np.argmax(self.q_table[x, y])  # Chọn hướng tốt nhất theo Q-table
            dx, dy = [(-1, 0), (1, 0), (0, -1), (0, 1)][action]
            nx, ny = x + dx, y + dy

            if (nx, ny) == goal:
                path.append((nx, ny))
                return path  # Tìm thấy lối ra

            if self.maze[nx, ny] == 1:  # Nếu AI đi vào tường, dừng lại
                break

            x, y = nx, ny
            path.append((x, y))

        return None  # Không tìm thấy lối ra
    

import numpy as np
import random


# Tạo mê cung
maze, start = create_maze_dfs(WIDTH, HEIGHT)
goal = (WIDTH - 2, HEIGHT - 2)

# Huấn luyện AI
agent = QLearningAgent(maze)
print("🔄 Đang huấn luyện AI...")
agent.train(start, goal)

# Chạy AI sau khi huấn luyện
print("✅ AI đang giải mê cung...")
path = agent.solve(start, goal)

# Hiển thị kết quả
if path:
    for x, y in path:
        maze[x, y] = 3  # Đánh dấu đường đi
    display_maze(maze, start, goal)
    print(f"🎉 AI tìm thấy lối thoát trong {len(path)} bước!")
else:
    print("❌ AI vẫn chưa tìm được lối ra.")
