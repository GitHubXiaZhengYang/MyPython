from random import choice, choices
from time import sleep


def title():
    print("""这是一个三国杀小游戏
作者：夏正洋
祝你玩得愉快！！！
中途如想退出，请输入“Quit”或“Exit”。""")


def player_help():
    print("""
【玩家操作】
【1】出牌：出牌后，玩家需要选择一张手牌进行出牌（输入卡牌名称并按下回车即可），然后等待电脑出牌。
【2】使用【桃】：使用桃牌后，玩家回复一点体力。
【3】使用【闪】：使用闪牌后，玩家抵挡住电脑出的杀牌。
【4】使用【杀】：使用杀牌后，玩家需要等待电脑出牌。
【5】出牌阶段或弃牌阶段时，不输入并按下回车即可跳过此阶段。
""")


class InitGame:
    """
    初始化游戏类，负责游戏的初始化操作。
    """

    def __init__(self):
        """
        类的构造函数，用于初始化游戏状态。

        :param:
        :return:
        """
        # 初始化游戏卡牌池
        self.SGS_Cards = ['桃', '闪', '闪', '杀', '杀', '杀', '杀']
        # 初始化玩家和电脑的卡牌手牌，初始为None
        self.computer_Cards = None
        self.player_Cards = None
        # 初始化玩家和电脑的血量为4
        self.computer_Hp = 4
        self.player_Hp = 4
        # 调用初始化游戏流程的方法
        self.init_game()

    def init_game(self):
        """
        初始化游戏流程的方法，包括玩家和电脑的初始手牌分配。
        :param:
        :return:
        """
        # 分配玩家手牌
        self.player_Cards = choices(self.SGS_Cards, k=4)
        # 分配电脑手牌
        self.computer_Cards = choices(self.SGS_Cards, k=4)


class PlayGame:
    """
    游戏玩法类，负责游戏的进行。
    """

    def __init__(self):
        """
        初始化游戏，创建初始游戏对象，初始化玩家输入、电脑卡片为空。
        :param:
        :return:
        """
        self.init = InitGame()  # 初始化游戏设置
        self.player_input = None  # 玩家输入
        self.com_card = None  # 电脑的卡片

    def cards_random(self, num):
        """
        生成随机卡片序列。

        :param: num
        :return:
        """
        return choices(self.init.SGS_Cards, k=num)  # 使用随机选择函数选择num个卡片

    def player_game(self):
        """
        玩家游戏流程，包括发牌、玩家出牌和扔牌阶段。
        :param:
        :return:
        """
        # 发给玩家两张卡片
        self.init.player_Cards.extend(self.cards_random(2))
        # 初始化杀牌数量
        sha = 0
        while True:
            # 每轮等待玩家输入
            sleep(0.5)
            self.player_input = input(f'你现在有{self.init.player_Cards}\n请出牌：')
            # 提供给玩家退出游戏的选项
            if self.player_input == "Quit" or self.player_input == "Exit":
                exit()
            if self.player_input == 'Help':
                player_help()
            # 玩家出牌逻辑，包括移除出的牌和可能的加血操作
            elif self.player_input == '':
                break
            elif self.player_input in self.init.player_Cards:
                if not sha:
                    pass
                else:
                    if self.player_input == '杀':
                        print("你已出杀，不能再出杀！")
                        continue
                self.init.player_Cards.remove(self.player_input)
                print('你已出牌：', end='')
                print(self.player_input)
                if self.player_input == '桃':
                    self.init.player_Hp += 1
                # 电脑回合
                self.computer_look()
                if self.player_input == '杀':
                    sha += 1
            else:
                # 输入错误处理
                print('输入错误！请重新输入！')
                sleep(0.5)

        # 玩家处理剩余卡片，扔牌阶段
        while True:
            if len(self.init.player_Cards) > self.init.player_Hp:
                card = input(f'你现在有{self.init.player_Cards}\n请扔牌：')
                cards = []
                if card == "":
                    for _ in range(len(self.init.player_Cards) - self.init.player_Hp):
                        card = choice(self.init.player_Cards)
                        self.init.player_Cards.remove(card)
                        cards.append(card)
                else:
                    self.init.player_Cards.remove(card)
                    cards.append(card)
                print(f"你扔掉了{cards}")
            if len(self.init.player_Cards) <= self.init.player_Hp:
                break

    def computer_game(self):
        """
        计算机玩家进行游戏的逻辑处理。

        从初始手牌中随机选择两张牌加入计算机玩家的手中。然后根据手牌情况，电脑会优先使用桃子恢复生命值，
        若没有桃子则尝试使用杀牌，如果没有杀牌则判定为无牌可出。若计算机玩家手牌数量超过其生命值，
        则会丢弃多余的牌。
        :param:
        :return:
        """
        # 初始化，给计算机玩家发两张随机牌
        self.init.computer_Cards.extend(self.cards_random(2))
        self.com_card = None
        # 如果有桃子且生命值小于3，则使用桃子恢复生命值
        if '桃' in self.init.computer_Cards and self.init.computer_Hp < 3:
            self.com_card = '桃'
            self.init.computer_Hp += 1
            self.init.computer_Cards.remove(self.com_card)
            print('电脑出牌：', end='')
            print(self.com_card)
        # 如果有杀牌，则出杀牌，并调用player_look方法
        if '杀' in self.init.computer_Cards:
            self.com_card = '杀'
            self.init.computer_Cards.remove(self.com_card)
            print('电脑出牌：', end='')
            print(self.com_card)
            self.player_look()
        else:
            # 如果没有可以出的牌，则显示无牌可出
            self.com_card = None
            print('电脑无牌出！')
        # 如果手牌数量超过生命值，丢弃多余的牌
        if len(self.init.computer_Cards) > self.init.computer_Hp:
            num = len(self.init.computer_Cards) - self.init.computer_Hp
            cards = []
            for _ in range(num):
                card = choice(self.init.computer_Cards)
                self.init.computer_Cards.remove(card)
                cards.append(card)
            print(f'电脑已扔牌：{cards}')

    def player_look(self):
        """
        玩家出牌逻辑处理，如果玩家有闪，则出闪，否则扣除一点生命值。

        :param:
        :return:
        """
        sleep(0.5)
        # 检查玩家是否有闪，若有则出闪，否则扣血
        if '闪' in self.init.player_Cards:
            sleep(0.5)
            print('你已出闪。')
            self.init.player_Cards.remove('闪')
        else:
            sleep(0.5)
            print('你没闪，扣一血！')
            self.init.player_Hp -= 1

    def computer_look(self):
        """
        电脑自动出牌逻辑。
        根据玩家输入的‘杀’，电脑判断是否出‘闪’来挡杀，如果没有‘闪’则扣血。

        :param:
        :return:
        """
        if self.player_input == '杀':  # 玩家出‘杀’
            sleep(0.5)  # 增加游戏趣味性，电脑思考0.5秒
            if '闪' in self.init.computer_Cards:  # 电脑判断是否拥有‘闪’
                self.init.computer_Cards.remove('闪')  # 电脑出‘闪’，移除‘闪’这张牌
                print('电脑已出：“闪”')
            else:  # 电脑没有‘闪’，则扣血
                self.init.computer_Hp -= 1


class RunGame:
    def __init__(self):
        """
        初始化函数，用于创建一个游戏对象。

        :param:
        :return:
        """
        self.play = PlayGame()  # 创建一个PlayGame对象并赋值给self.play
        self.hui_he = 0  # 初始化self.hui_he为0

    def run(self):
        """
        运行函数，执行程序主逻辑.

        :param:
        :return:
        """
        title()  # 调用title函数
        while True:
            self.hui_he += 1  # 自增循环计数器
            self.indoor()  # 调用indoor函数
            self.play.player_game()  # 调用play对象的player_game方法
            self.look()  # 调用look函数
            self.play.computer_game()  # 调用play对象的computer_game方法
            self.look()  # 调用look函数

    def look(self):
        """
        查看游戏结果

        如果玩家或电脑的血量为0，则打印"Game Over!!!"，并根据玩家和电脑的血量判断输赢。
        如果玩家血量为0，则打印"你输了！！！"。
        如果电脑血量为0，则打印"你赢了！！！"。
        然后暂停5秒，最后进行询问。

        :param:
        :return:
        """
        if self.play.init.player_Hp == 0 or self.play.init.computer_Hp == 0:
            sleep(0.5)
            print('Game Over!!!')
            if self.play.init.player_Hp == 0:
                print('你输了！！！')
            else:
                print('你赢了！！！')
            sleep(5)
            exit(0)

    def indoor(self):
        """
        在室内进行游戏的函数。
        该函数用于在室内进行游戏，会打印出当前回合、玩家的血量、玩家的卡牌和电脑的血量。

        :param:
        :return:
        """
        sleep(0.5)
        print(f"""\n当前回合：{self.hui_he}
你的血量: {self.play.init.player_Hp}
你的卡牌: {self.play.init.player_Cards}
电脑的血量: {self.play.init.computer_Hp}\n""")


if __name__ == '__main__':
    run = RunGame()
    run.run()
