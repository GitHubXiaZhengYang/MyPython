from random import sample
from time import sleep

TICKET_RED = [i for i in range(1, 9)]
TICKET_BLUE = [i for i in range(1, 12)]


def opening():
    """
    开奖
    :return: 开奖号码
    """
    red = sample(TICKET_RED, k=5)
    blue = sample(TICKET_BLUE, k=2)
    ticket = red + blue

    return ticket


def into(ticket: list, keys: str):
    """
    获取用户购买的彩票
    :param ticket: 开奖号码
    :param keys: 用户购买的彩票号码
    :return: 中奖结果
    """
    num = 0
    counts = {}
    key = keys.replace(" ", "").split(",")
    len_k = len(key)
    for k in key:
        num += 1
        count = 0
        t = k.replace("[", "").replace("]", "").replace(" ", "").split(",")
        for i in range(6):
            if t[i] == ticket[i]:
                count += 1
        counts[num] = count

    return len_k, counts, key


def main():
    """
    主程序
    :return:
    """
    ticket = opening()
    running = True
    while running:
        f = input("请输入购买的彩票：")
        if f == "test" or f == "":
            print(ticket)
            ticket = opening()
        elif f == "quit":
            running = False
        else:
            l, counts, key = into(ticket, f)
            if l * 5 == int(input(f"共购买{l}张彩票, 需支付{l * 5}元：")):
                money = 0
                print("请等待5秒, 5秒后系统将返回中奖结果。")
                sleep(5)
                print("张数/t/t彩票/t/t中奖结果")
                for i in range(1, l):
                    print(f"{i}/t/t{key[i - 1]}/t/t{counts[i]}")
                    money += 10 ** (counts[i] - 1)
                print(f"共获奖{money}元！")
            else:
                print("格式错误, 请重试！")


if __name__ == '__main__':
    main()
