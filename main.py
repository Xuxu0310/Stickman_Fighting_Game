import pygame
import random
import sys
import pickle

pygame.init()

WIDTH, HEIGHT = 900, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Fighting Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)


# ===== 居中文本 =====
def draw_center(text, y, f):
    txt = f.render(text, True, (255,255,255))
    rect = txt.get_rect(center=(WIDTH//2, y))
    screen.blit(txt, rect)


# ===== 按钮 =====
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(screen, (70,70,70), self.rect)
        pygame.draw.rect(screen, (200,200,200), self.rect, 2)
        txt = font.render(self.text, True, (255,255,255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


# ===== 角色 =====
class Fighter:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.hp = 100
        self.mp = 100
        self.color = color
        self.attack_timer = 0
        self.crouching = False

    def face(self, other):
        return 1 if other.x > self.x else -1

    def move(self, dx):
        self.x += dx
        self.x = max(50, min(WIDTH-50, self.x))

    def attack(self, other):
        self.attack_timer = 8
        if abs(self.x - other.x) < 60:
            other.hp -= 3

    def skill(self, other, projectiles):
        if self.mp < 20:
            return
        self.mp -= 20
        d = self.face(other)

        projectiles.append({
            "x": self.x + d*25,
            "y": self.y-20,
            "vx": 10*d,
            "owner": self
        })

    def update(self):
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.mp < 100:
            self.mp += 0.2

    def draw(self, opponent):
        d = self.face(opponent)
        body_y = self.y if not self.crouching else self.y + 30

        pygame.draw.circle(screen, self.color, (int(self.x), int(body_y-40)), 10)
        pygame.draw.line(screen, self.color, (self.x, body_y-30), (self.x, body_y), 3)

        arm = 25 + (15 if self.attack_timer > 0 else 0)
        pygame.draw.line(screen, self.color,
                         (self.x, body_y-20),
                         (self.x + d*arm, body_y-10), 3)

        pygame.draw.line(screen, self.color,
                         (self.x, body_y),
                         (self.x-15, body_y+30), 3)

        pygame.draw.line(screen, self.color,
                         (self.x, body_y),
                         (self.x+15, body_y+30), 3)


# ===== AI =====
class EnemyAI:
    def __init__(self, level):
        self.level = level
        self.action_timer = 0

    def act(self, p, e, projectiles):
        self.action_timer += 1

        # 🔥 决策节流（避免疯狂攻击）
        if self.action_timer < 6:
            return None
        self.action_timer = 0

        # 🔥 困难模式：会躲技能
        if self.level == "hard":
            for proj in projectiles:
                if proj["owner"] != e and abs(proj["x"] - e.x) < 80:
                    return 3

        dist = abs(p.x - e.x)

        if dist < 60:
            if random.random() < 0.4:
                return 2

        if 60 < dist < 150 and e.mp >= 20:
            if random.random() < 0.3:
                return 4

        return 0 if e.x > p.x else 1


# ===== UI =====
def draw_bars(p, e):
    pygame.draw.rect(screen,(255,0,0),(50,30,p.hp*2,20))
    pygame.draw.rect(screen,(255,0,0),(WIDTH-250,30,e.hp*2,20))

    pygame.draw.rect(screen,(0,0,255),(50,55,p.mp*2,10))
    pygame.draw.rect(screen,(0,0,255),(WIDTH-250,55,e.mp*2,10))


# ===== 主菜单 =====
def menu():
    easy = Button("Easy",350,260,200,50)
    hard = Button("Hard",350,330,200,50)

    while True:
        screen.fill((20,20,20))

        draw_center("Stickman Fighting Game", 120, big_font)
        draw_center("← → Move | SPACE Attack | SHIFT Skill | ↓ Dodge", 180, font)

        easy.draw()
        hard.draw()

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if easy.clicked(e.pos):
                    return "easy"
                if hard.clicked(e.pos):
                    return "hard"


# ===== 结束界面 =====
def game_over(result):
    restart = Button("Restart",350,220,200,50)
    menu_btn = Button("Menu",350,290,200,50)
    quit_btn = Button("Quit",350,360,200,50)

    while True:
        screen.fill((30,30,30))

        draw_center(result, 130, big_font)

        restart.draw()
        menu_btn.draw()
        quit_btn.draw()

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if restart.clicked(e.pos): return "restart"
                if menu_btn.clicked(e.pos): return "menu"
                if quit_btn.clicked(e.pos): sys.exit()


# ===== 游戏 =====
def game(level):
    player = Fighter(200,320,(0,200,255))
    enemy = Fighter(700,320,(255,80,80))
    ai = EnemyAI(level)

    projectiles=[]

    while True:
        clock.tick(60)
        screen.fill((30,30,30))

        # ===== 单次触发攻击（关键🔥）=====
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    player.attack(enemy)
                if e.key == pygame.K_LSHIFT:
                    player.skill(enemy, projectiles)

        keys = pygame.key.get_pressed()

        player.crouching = keys[pygame.K_DOWN]

        if keys[pygame.K_LEFT]: player.move(-5)
        if keys[pygame.K_RIGHT]: player.move(5)

        # ===== AI =====
        action = ai.act(player,enemy,projectiles)

        if action is not None:
            enemy.crouching=False

            # 🔥 速度差异（优化点）
            if level == "easy":
                speed = 5
            else:
                speed = 6

            if action==0: enemy.move(-speed)
            elif action==1: enemy.move(speed)
            elif action==2: enemy.attack(player)
            elif action==3: enemy.crouching=True
            elif action==4: enemy.skill(player,projectiles)

        # ===== 子弹 =====
        for p in projectiles[:]:
            p["x"] += p["vx"]
            pygame.draw.circle(screen,(255,255,0),(int(p["x"]),int(p["y"])),6)

            if p["owner"]!=player and abs(p["x"]-player.x)<20 and not player.crouching:
                player.hp-=6
                projectiles.remove(p)

            elif p["owner"]!=enemy and abs(p["x"]-enemy.x)<20 and not enemy.crouching:
                enemy.hp-=6
                projectiles.remove(p)

            elif p["x"]<0 or p["x"]>WIDTH:
                projectiles.remove(p)

        player.update()
        enemy.update()

        player.draw(enemy)
        enemy.draw(player)
        draw_bars(player,enemy)

        if player.hp<=0:
            return "YOU LOSE"
        if enemy.hp<=0:
            return "YOU WIN"

        pygame.display.flip()


# ===== 主循环 =====
level = menu()

while True:
    result = game(level)
    choice = game_over(result)

    if choice == "menu":
        level = menu()
    elif choice == "restart":
        continue