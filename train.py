import numpy as np
import random
import pickle

WIDTH = 900


class Fighter:
    def __init__(self, x):
        self.x = x
        self.hp = 100
        self.mp = 100

    def move(self, dx):
        self.x += dx
        self.x = max(50, min(WIDTH-50, self.x))

    def attack(self, other):
        if abs(self.x - other.x) < 60:
            other.hp -= 3

    def skill(self, other):
        if self.mp >= 20:
            self.mp -= 20
            if abs(self.x - other.x) > 80:
                other.hp -= 6

    def update(self):
        if self.mp < 100:
            self.mp += 0.3


class AI:
    def __init__(self, epsilon):
        self.q = {}
        self.epsilon = epsilon
        self.alpha = 0.1
        self.gamma = 0.9

    def get_state(self, p, e):
        return (
            int((p.x - e.x)/30),
            int(p.hp/10),
            int(e.hp/10),
            int(e.mp/20)
        )

    def choose(self, s):
        if random.random() < self.epsilon:
            return random.randint(0,5)
        return np.argmax(self.q.get(s, [0]*6))

    def learn(self, s, a, r, s2):
        self.q.setdefault(s, [0]*6)
        self.q.setdefault(s2, [0]*6)

        self.q[s][a] += self.alpha * (
            r + self.gamma * max(self.q[s2]) - self.q[s][a]
        )


def train(episodes, name, epsilon):
    ai = AI(epsilon)

    for ep in range(episodes):
        p = Fighter(200)
        e = Fighter(700)

        prev_p_hp = p.hp
        prev_e_hp = e.hp

        for step in range(400):

            s = ai.get_state(p, e)
            a = ai.choose(s)

            reward = 0
            dist = abs(p.x - e.x)

            # ===== 行为 =====
            if a == 0:
                e.move(-5)
            elif a == 1:
                e.move(5)
            elif a == 2:
                e.attack(p)
            elif a == 3:
                pass  # crouch（训练简化）
            elif a == 4:
                e.skill(p)
            elif a == 5:
                pass

            # ===== dummy 玩家（更真实🔥）=====
            if dist > 80:
                p.move(3 if p.x < e.x else -3)
            else:
                if random.random() < 0.5:
                    p.attack(e)

            p.update()
            e.update()

            # ===== 奖励函数（核心🔥）=====
            # 攻击奖励
            if p.hp < prev_p_hp:
                reward += 8
            if e.hp < prev_e_hp:
                reward -= 6

            # 距离控制
            if 50 < dist < 120:
                reward += 2
            if dist < 30:
                reward -= 3
            if dist > 200:
                reward -= 2

            # 鼓励移动
            if a in [0,1]:
                reward += 1

            # 防止挂机🔥
            reward -= 0.2

            # 防止卡墙🔥
            if e.x < 60 or e.x > WIDTH-60:
                reward -= 5

            s2 = ai.get_state(p, e)
            ai.learn(s, a, reward, s2)

            prev_p_hp = p.hp
            prev_e_hp = e.hp

            if p.hp <= 0 or e.hp <= 0:
                break

        print(f"Episode {ep}")

    with open(name, "wb") as f:
        pickle.dump(ai.q, f)


print("Training EASY...")
train(500, "model_easy.pkl", 0.6)

print("Training HARD...")
train(3000, "model_hard.pkl", 0.05)