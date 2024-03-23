import pygame
from random import randint, uniform, choice
import math

vector = pygame.math.Vector2
gravity = vector(0, 0.3)
screen_width = screen_height = 800

trail_colours = [(45, 45, 45), (60, 60, 60), (75, 75, 75), (125, 125, 125), (150, 150, 150)]
dynamic_offset = 1
static_offset = 5


def generate随机颜色():
    return (randint(0, 255), randint(0, 255), randint(0, 255))


class Firework:
    def __init__(self, pos=None, vec=None):
        self.colour = generate随机颜色()
        self.colours = (
            generate随机颜色(), generate随机颜色(), generate随机颜色()
        )
        if not pos:
            self.firework = Firework.create_firework(randint(0, screen_width), screen_height, True, self.colour)
        else:
            self.firework = Firework.create_firework(pos, screen_height, True, self.colour, vec)
        self.exploded = False
        self.particles = []
        self.min_max_particles = vector(100, 225)

    def explode(self):
        amount = randint(self.min_max_particles.x, self.min_max_particles.y)
        for i in range(amount):
            self.particles.append(Firework.create_firework(self.firework.pos.x, self.firework.pos.y, False, self.colours))

    def create_firework(self, x, y, yan_hua, colour, vec=None):
        # 在这里创建Firework类的实例，它会处理烟花的创建和运动
        return Firework


class Firework(YanHua):
    def __init__(self, x, y, yan_hua, colour, vec=None):
        self.yan_hua = yan_hua
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

        if self.yan_hua:
            self.vel = vector(0, -randint(17, 20))
            self.size = 5
            self.colour = colour
            for i in range(5):
                self.trails.append(DrawFirework(i, self.size, True))
        else:
            if not vec:
                self.vel = vector(uniform(-1, 1), uniform(-1, 1))
            else:
                self.vel = vector(vec, vec)

            self.vel.x *= randint(7, self.explosion_radius + 2)
            self.vel.y *= randint(7, self.explosion_radius + 2)
            self.size = randint(2, 4)
            self.colour = choice(colour)
            for i in range(5):
                self.trails.append(DrawFirework(i, self.size, False))

    def apply_force(self, force):
        self.acc += force

    def move(self):
        if not self.yan_hua:
            self.vel.x *= 0.8
            self.vel.y *= 0.8

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        if self.life == 0 and not self.yan_hua:
            distance = math.sqrt((self.pos.x - self.origin.x)**2 + (self.pos.y - self.origin.y)**2)
            if distance > self.explosion_radius:
                self.remove = True

        self.decay()

        self.trail_update()

        self.life += 1

    def show(self, screen):
        pygame.draw.circle(screen, (self.colour[0], self.colour[1], self.colour[2], 0),
                           (int(self.pos.x), int(self.pos.y)), self.size)

    def decay(self):
        if 10 < self.life < 50:
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
                t.get_pos(self.prev_pos_x[n + dynamic_offset], self.prev_pos_y[n + dynamic_offset])
            else:
                t.get_pos(self.prev_pos_x[n + static_offset], self.prev_pos_y[n + static_offset])


class DrawFirework:
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

        def get_pos(x, y):
            self.pos = vector(x, y)

    def show(self, win):
        pygame.draw.circle(win, self.colour, (int(self.pos.x), int(self.pos.y)), self.size)


def update(screen, fireworks):
    for firework in fireworks:
        firework.update(screen)
        if firework.remove():
            fireworks.remove(firework)

    pygame.display.update()


def create_fireworks(screen_width, screen_height):
    # 在这里生成初始烟花列表
    return fireworks


def main():
    # 检查功能是否正常
    main()
    pygame.init()
    icon = pygame.image.load("bin/image/Logo_Mr.X.ico")
    pygame.display.set_caption("烟花盛宴")
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    fireworks = create_fireworks(screen_width, screen_height)  # 创建第一个烟花
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
                    fireworks.append(Firework())
                if event.key == pygame.K_2:
                    for _ in range(10):
                        fireworks.append(Firework())
                if event.key == pygame.K_3:
                    for _ in range(100):
                        fireworks.append(Firework())
                if event.key == pygame.K_SPACE:
                    for _ in range(100):
                        fireworks.append(Firework(100))
                        fireworks.append(Firework(700))
                    # for _ in range(10):
                    #     fireworks.append(Firework(400, 5))
        screen.fill((20, 20, 30))  # 绘制背景
        if randint(0, 20) == 1:  # 有几率(5%)创建新烟花，使程序不单调
            fireworks.append(Firework())

        update(screen, fireworks)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
