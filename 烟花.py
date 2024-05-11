from time import sleep

import pygame
from random import randint, uniform, choice
import math_game
from ast import literal_eval

vector = pygame.math.Vector2
options = {}
with open("bin/options.txt", "r") as f:
    lines = f.readlines()
    for i in lines:
        list_ = i.replace("\n", "").split(": ")
        if list_[0] == "gravity":
            options["gravity"] = vector(0, float(list_[1]))
        elif list_[0] == "trail_colours":
            options["trail_colours"] = literal_eval(list_[1])
        elif list_[0] == "font" or list_[0] == "greetings" or list_[0] == "bold":
            options[list_[0]] = list_[1]
        else:
            options[list_[0]] = int(list_[1])


class InitFirework:

    def __init__(self, pos=None, vec=None):
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.colours = (
            (randint(0, 255), randint(0, 255), randint(0, 255)
             ), (randint(0, 255), randint(0, 255), randint(0, 255)),
            (randint(0, 255), randint(0, 255), randint(0, 255)))
        if not pos:
            self.yan_hua = CreateFirework(randint(0, options["screen_width"]),
                                          options["screen_height"], True, self.colour)
            # 创建烟花
        else:
            self.yan_hua = CreateFirework(pos, options["screen_height"], True, self.colour, vec)
        self.exploded = False
        self.particles = []
        self.min_max_particles = vector(100, 225)

    def update(self, screen):  # 加载烟花
        if not self.exploded:
            self.yan_hua.apply_force(options["gravity"])
            self.yan_hua.move()
            for tf in self.yan_hua.trails:
                tf.show(screen)

            self.show(screen)

            if self.yan_hua.vel.y >= 0:
                self.exploded = True
                self.explode()
        else:
            for particle in self.particles:
                particle.apply_force(
                    vector(options["gravity"].x + uniform(-1, 1) / 20, options["gravity"].y / 2 + (randint(1, 8) / 100))
                )
                particle.move()
                for t in particle.trails:
                    t.show(screen)
                particle.show(screen)

    def explode(self):
        amount = randint(int(self.min_max_particles.x), int(self.min_max_particles.y))
        for _ in range(amount):
            self.particles.append(
                CreateFirework(self.yan_hua.pos.x, self.yan_hua.pos.y, False, self.colours))

    def show(self, win):
        pygame.draw.circle(win, self.colour, (int(self.yan_hua.pos.x), int(
            self.yan_hua.pos.y)), self.yan_hua.size)

    def remove(self):
        if self.exploded:
            for p in self.particles:
                if p.remove:
                    self.particles.remove(p)

            if len(self.particles) == 0:
                return True
            else:
                return False


class CreateFirework:

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
            for n in range(5):
                self.trails.append(DrawFirework(n, self.size, True))
        else:
            if not vec:
                self.vel = vector(uniform(-1, 1), uniform(-1, 1))
            else:
                self.vel = vector(vec, vec)

            self.vel.x *= randint(7, self.explosion_radius + 2)
            self.vel.y *= randint(7, self.explosion_radius + 2)
            self.size = randint(2, 4)
            self.colour = choice(colour)
            for n in range(5):
                self.trails.append(DrawFirework(n, self.size, False))

    def apply_force(self, force):
        self.acc += force

    def move(self):
        if not self.yan_hua:
            self.vel.x *= 0.8
            self.vel.y *= 0.8

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        if self.life == 0 and not self.yan_hua:  # 检查颗粒是否在爆炸半径之外
            distance = math.sqrt((self.pos.x - self.origin.x)
                                 ** 2 + (self.pos.y - self.origin.y) ** 2)
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
                t.get_pos(self.prev_pos_x[n + options["dynamic_offset"]],
                          self.prev_pos_y[n + options["dynamic_offset"]])
            else:
                t.get_pos(self.prev_pos_x[n + options["static_offset"]],
                          self.prev_pos_y[n + options["static_offset"]])


class DrawFirework:

    def __init__(self, n, size, dynamic):
        self.pos_in_line = n
        self.pos = vector(-10, -10)
        self.dynamic = dynamic

        if self.dynamic:
            self.colour = options["trail_colours"][n]
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
按0键，进入配置模式
按空格键，额外在两侧释放10个烟花（不建议尝试）
按◁﹣（Backspace）/Q/Esc键退出（或直接关闭窗口）
""")


def options_setting():
    print(f"""欢迎来到配置模式。输入quit退出.
可更改参数如下：
screen_width(屏宽 单位: px)(w) 当前值为{options["screen_width"]})
screen_height(屏高 单位: px)(h) 当前值为{options["screen_height"]})
dynamic_offset(动态偏移(粒子与拖尾的距离偏移) 参数 0-5)(d) 当前值为{options["dynamic_offset"]})
static_offset(静态偏移(粒子与拖尾的时间偏移) 参数 0-5)(s) 当前值为{options["static_offset"]})
gravity(重力 参数: 小数)(g) 当前值为{options["gravity"]})
trail_colours(粒子颜色 参数: RGB 格式: [(R, G, B), ...])(t) 当前值为{options["trail_colours"]})
font(字体 参数: 字体名(宋体/微软雅黑/楷体) 格式: SongTi(宋体))(f) 当前值为{options["font"]})
glyph(字形大小)(l) 当前值为{options["glyph"]})
greetings(背景文字/祝福语)(e) 当前值为{options["greetings"]})
bold(文字加粗 参数: True/False)(b) 当前值为{options["bold"]})

若要更改, 请输入对应参数编码。
Tips: 修改需谨慎！修改的格式错误将导致程序崩溃！
""")
    old_options = {
        "w": "screen_width",
        "h": "screen_height",
        "d": "dynamic_offset",
        "s": "static_offset",
        "g": "gravity",
        "t": "trail_colours",
        "f": "font",
        "l": "glyph",
        "e": "greetings",
        "b": "bold"
    }
    while True:
        setting = input("请输入: ").replace("\n", "")
        if setting == "quit":
            return
        else:
            if setting in old_options:
                value_g = 0.3
                value_t = [(45, 45, 45), (60, 60, 60), (75, 75, 75), (125, 125, 125), (150, 150, 150)]
                if setting == "l" or setting == "w" or setting == "h" or setting == "d" or setting == "s":
                    options[(old_options[setting])] = int(
                        input(f"请输入{old_options[setting]}的值: ").replace("\n", ""))
                elif setting == "g":
                    value_g = float(input(f"请输入{old_options[setting]}的值: ").replace("\n", ""))
                    options[old_options[setting]] = vector(0, value_g)
                elif setting == "t":
                    value_t = literal_eval(input(f"请输入{old_options[setting]}的值: ").replace("\n", ""))
                    value_new = literal_eval(value_t)
                    options[old_options[setting]] = value_new
                else:
                    options[old_options[setting]] = input(f"请输入{old_options[setting]}的值: ").replace("\n", "")

                with open("bin/options.txt", "w") as file:
                    file.write(f"""screen_width: {options["screen_width"]}
screen_height: {options["screen_height"]}
dynamic_offset: {options["dynamic_offset"]}
static_offset: {options["static_offset"]}
gravity: {value_g}
trail_colours: {value_t}
font: {options["font"]}
glyph: {options["glyph"]}
greetings: {options["greetings"]}
bold: {options["bold"]}
""")
            else:
                print("参数错误!")
                sleep(0.1)


def main():
    printf()
    pygame.init()
    icon = pygame.image.load("bin/image/Logo_Mr.X.ico")
    pygame.display.set_caption("烟花盛宴")
    pygame.display.set_icon(icon)
    pygame.mixer.music.load("bin/music/bgm.mp3")
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((options["screen_width"], options["screen_height"]))
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()

    yan_hua_list = [InitFirework() for _ in range(2)]  # 创建第一个烟花
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():  # 侦测事件
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_1:
                    yan_hua_list.append(InitFirework())
                if event.key == pygame.K_2:
                    for _ in range(10):
                        yan_hua_list.append(InitFirework())
                if event.key == pygame.K_3:
                    for _ in range(100):
                        yan_hua_list.append(InitFirework())
                if event.key == pygame.K_SPACE:
                    for _ in range(10):
                        yan_hua_list.append(InitFirework(100))
                        yan_hua_list.append(InitFirework(700))
                if event.key == pygame.K_0:
                    pygame.mixer.music.pause()
                    sleep(1)
                    options_setting()
                    sleep(1)
                    pygame.mixer.music.unpause()

        if options["font"] == "WeiRuanYaHei":
            font = pygame.font.Font("bin/font/WeiRuanYaHei.ttc", options["glyph"])
        else:
            font = pygame.font.Font(f"bin/font/{options['font']}.ttf", options["glyph"])
        if options["bold"] == "True":
            font.set_bold(True)
        text = f"{options['greetings']}"
        image = font.render(text, True, "red")
        rect = image.get_rect()
        rect.center = screen_rect.center

        screen.fill((20, 20, 30))  # 绘制背景
        if randint(0, 20) == 1:  # 有几率(5%)创建新烟花，使程序不单调
            yan_hua_list.append(InitFirework())

        screen.blit(image, (rect.x, rect.y))
        update(screen, yan_hua_list)

    pygame.quit()


# 执行程序
if __name__ == '__main__':
    main()
