from random import choice, choices
from time import sleep


def title():
    print("""这是一个三国杀小游戏
作者：夏正洋
祝你玩得愉快！！！
中途如想退出，请输入“Quit”或“Exit”。""")


class InitGame:
    def __init__(self):
        self.SGS_Cards = ['桃', '闪', '闪', '杀', '杀', '杀', '杀']
        self.computer_Cards = None
        self.player_Cards = None
        self.computer_Hp = 4
        self.player_Hp = 4
        self.init_game()

    def init_game(self):
        self.player_Cards = choices(self.SGS_Cards, k=4)
        self.computer_Cards = choices(self.SGS_Cards, k=4)


class PlayGame:
    def __init__(self):
        self.init = InitGame()
        self.player_shu_ru = None
        self.com_card = None

    def cards_random(self, num):
        return choices(self.init.SGS_Cards, k=num)

    def player_game(self):
        self.init.player_Cards.extend(self.cards_random(2))
        while True:
            sleep(0.5)
            self.player_shu_ru = input(f'你现在有{self.init.player_Cards}\n请出牌：')
            if self.player_shu_ru == "Quit" or self.player_shu_ru == "Exit":
                exit()
            elif self.player_shu_ru in self.init.player_Cards:
                self.init.player_Cards.remove(self.player_shu_ru)
                print('你已出牌：', end='')
                print(self.player_shu_ru)
                if self.player_shu_ru == '桃':
                    self.init.player_Hp += 1
                self.computer_look()
                break
            else:
                print('输入错误！请重新输入！')
                sleep(0.5)

        while True:
            if len(self.init.player_Cards) > self.init.player_Hp:
                card = input(f'你现在有{self.init.player_Cards}\n请扔牌：')
                self.init.player_Cards.remove(card)
            if len(self.init.player_Cards) <= self.init.player_Hp:
                break

    def computer_game(self):
        self.init.computer_Cards.extend(self.cards_random(2))
        self.com_card = None
        if '桃' in self.init.computer_Cards and self.init.computer_Hp < 3:
            self.com_card = '桃'
            self.init.computer_Hp += 1
            self.init.computer_Cards.remove(self.com_card)
            print('电脑出牌：', end='')
            print(self.com_card)
        else:
            if '杀' in self.init.computer_Cards:
                self.com_card = '杀'
                self.init.computer_Cards.remove(self.com_card)
                print('电脑出牌：', end='')
                print(self.com_card)
                self.player_look()
            else:
                self.com_card = None
                print('电脑无牌出！')
        if len(self.init.computer_Cards) > self.init.computer_Hp:
            num = len(self.init.computer_Cards) - self.init.computer_Hp
            cards = []
            for _ in range(num):
                card = choice(self.init.computer_Cards)
                self.init.computer_Cards.remove(card)
                cards.append(card)
            print(f'电脑已扔牌：{cards}')

    def player_look(self):
        if '闪' in self.init.player_Cards:
            sleep(0.5)
            print('你已出闪。')
            self.init.player_Cards.remove('闪')
        else:
            sleep(0.5)
            print('你没闪，扣一血！')
            self.init.player_Hp -= 1

    def computer_look(self):
        if self.player_shu_ru == '杀':
            sleep(0.5)
            if '闪' in self.init.computer_Cards:
                self.init.computer_Cards.remove('闪')
                print('电脑已出：“闪”')
            else:
                self.init.computer_Hp -= 1


class RunGame:
    def __init__(self):
        """
        初始化函数，用于创建一个游戏对象。
        """
        self.play = PlayGame()  # 创建一个PlayGame对象并赋值给self.play
        self.hui_he = 0  # 初始化self.hui_he为0


    def run(self):
        """
        运行函数，执行程序主逻辑
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
        然后暂停5秒，最后退出游戏。
        """
        if self.play.init.player_Hp == 0 or self.play.init.computer_Hp == 0:
            print('Game Over!!!')
            if self.play.init.player_Hp == 0:
                print('你输了！！！')
            else:
                print('你赢了！！！')
            sleep(5)
            exit()


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
