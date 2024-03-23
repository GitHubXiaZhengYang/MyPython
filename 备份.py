# 作者: Mr.X （夏正洋）
# 创作时间: 2024/1/1


import pygame
from random import randint, uniform, choice
import math

vector = pygame.math.Vector2
gravity = vector(0, 0.3)
screen_width = screen_height = 800

trail_colours = [(45, 45, 45), (60, 60, 60), (75, 75, 75),
                 (125, 125, 125), (150, 150, 150)]
dynamic_offset = 1
static_offset = 5


class YanHua:

    def __init__(self):
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.colours = (
            (randint(0, 255), randint(0, 255), randint(0, 255)
             ), (randint(0, 255), randint(0, 255), randint(0, 255)),
            (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.yan_hua = Particle(randint(0, screen_width), screen_height, True,
                                self.colour)  # 创建烟花
        self.exploded = False
        self.particles = []
        self.min_max_particles = vector(100, 225)

    def update(self, win):  # 加载烟花
        if not self.exploded:
            self.yan_hua.apply_force(gravity)
            self.yan_hua.move()
            for tf in self.yan_hua.trails:
                tf.show(win)

            self.show(win)

            if self.yan_hua.vel.y >= 0:
                self.exploded = True
                self.explode()
        else:
            for particle in self.particles:
                particle.apply_force(
                    vector(gravity.x + uniform(-1, 1) / 20, gravity.y / 2 + (randint(1, 8) / 100)))
                particle.move()
                for t in particle.trails:
                    t.show(win)
                particle.show(win)

    def explode(self):
        amount = randint(self.min_max_particles.x, self.min_max_particles.y)
        for i in range(amount):
            self.particles.append(
                Particle(self.yan_hua.pos.x, self.yan_hua.pos.y, False, self.colours))

    def show(self, win):
        pygame.draw.circle(win, self.colour, (int(self.yan_hua.pos.x), int(
            self.yan_hua.pos.y)), self.yan_hua.size)

    def remove(self):
        if self.exploded:
            for p in self.particles:
                if p.remove is True:
                    self.particles.remove(p)

            if len(self.particles) == 0:
                return True
            else:
                return False


class Particle:

    def __init__(self, x, y, yan_hua, colour):
        self.firework = yan_hua
        self.pos = vector(x, y)
        self.origin = vector(x, y)
        self.radius = 20
        self.remove = False
        self.explosion_radius = randint(5, 18)
        self.life = 0
        self.acc = vector(0, 0)
        self.trails = []  # 存储粒子跟踪对象
        self.prev_pos_x = [-10] * 10  # 存储最后 10 个位置
        self.prev_pos_y = [-10] * 10  # 存储最后 10 个位置

        if self.firework:
            self.vel = vector(0, -randint(17, 20))
            self.size = 5
            self.colour = colour
            for i in range(5):
                self.trails.append(Trail(i, self.size, True))
        else:
            self.vel = vector(uniform(-1, 1), uniform(-1, 1))
            self.vel.x *= randint(7, self.explosion_radius + 2)
            self.vel.y *= randint(7, self.explosion_radius + 2)
            self.size = randint(2, 4)
            self.colour = choice(colour)
            for i in range(5):
                self.trails.append(Trail(i, self.size, False))

    def apply_force(self, force):
        self.acc += force

    def move(self):
        if not self.firework:
            self.vel.x *= 0.8
            self.vel.y *= 0.8

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        if self.life == 0 and not self.firework:  # 检查颗粒是否在爆炸半径之外
            distance = math.sqrt((self.pos.x - self.origin.x)
                                 ** 2 + (self.pos.y - self.origin.y) ** 2)
            if distance > self.explosion_radius:
                self.remove = True

        self.decay()

        self.trail_update()

        self.life += 1

    def show(self, win):
        pygame.draw.circle(win, (self.colour[0], self.colour[1], self.colour[2], 0),
                           (int(self.pos.x), int(self.pos.y)), self.size)

    def decay(self):
        if 50 > self.life > 10:
            ran = randint(0, 30)
            if ran == 0:
                self.remove = True
        elif self.life > 50:
            ran = randint(0, 5)
            if ran == 0:
                self.remove = True

    def trail_update(self):
        self.prev_pos_x.pop()
        self.prev_pos_x.insert(0, int(self.pos.x))
        self.prev_pos_y.pop()
        self.prev_pos_y.insert(0, int(self.pos.y))

        for n, t in enumerate(self.trails):
            if t.dynamic:
                t.get_pos(self.prev_pos_x[n + dynamic_offset],
                          self.prev_pos_y[n + dynamic_offset])
            else:
                t.get_pos(self.prev_pos_x[n + static_offset],
                          self.prev_pos_y[n + static_offset])


class Trail:

    def __init__(self, n, size, dynamic):
        self.pos_in_line = n
        self.pos = vector(-10, -10)
        self.dynamic = dynamic

        if self.dynamic:
            self.colour = trail_colours[n]
            self.size = int(size - n / 2)
        else:
            self.colour = (255, 255, 200)
            self.size = size - 2
            if self.size < 0:
                self.size = 0

    def get_pos(self, x, y):
        self.pos = vector(x, y)

    def show(self, win):
        pygame.draw.circle(win, self.colour, (int(
            self.pos.x), int(self.pos.y)), self.size)


def update(screen, yan_hua_list):
    for yan_hua in yan_hua_list:
        yan_hua.update(screen)
        if yan_hua.remove():
            yan_hua_list.remove(yan_hua)

    pygame.display.update()


def printf():
    print("""作者: Mr.X (夏正洋)
创建日期：2024/1/1
按1键，额外释放1个烟花
按2键，额外释放10个烟花
按3键，额外释放100个烟花（不建议尝试）
按◁﹣（Backspace）键退出（或直接关闭窗口）""")


def main():
    printf()
    pygame.init()
    icon = pygame.image.load("bin/image/Logo_Mr.X.ico")
    pygame.display.set_caption("烟花盛宴")
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    yan_hua_list = [YanHua() for _ in range(2)]  # 创建第一个烟花
    running = True

    while running:
        clock.tick(60)
        # info = pygame.display.Info()
        # print(info)

        for event in pygame.event.get():  # 侦测事件
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    running = False
                if event.key == pygame.K_1:
                    yan_hua_list.append(YanHua())
                if event.key == pygame.K_2:
                    for _ in range(10):
                        yan_hua_list.append(YanHua())
                if event.key == pygame.K_3:
                    for _ in range(100):
                        yan_hua_list.append(YanHua())
        screen.fill((20, 20, 30))  # 绘制背景

        if randint(0, 20) == 1:  # 有几率(5%)创建新烟花，使程序不单调
            yan_hua_list.append(YanHua())

        # info = pygame.display.Info()  # 显示帧数
        # font = pygame.font.Font(None, 20)
        # text = f"当前屏幕帧数：{info}"
        # image = font.render(text, True, (255, 255, 255))
        # image_x = 0
        # image_y = 50
        # screen.blit(image, (image_x, image_y))

        update(screen, yan_hua_list)

    pygame.quit()
    quit()


# 执行程序
if __name__ == '__main__':
    main()
