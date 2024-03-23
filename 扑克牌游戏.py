fu = int(input("请输入您要玩的牌的副数(1/2)"))
cards = []
for i in range(fu):
    cards.extend(["小王", "大王"])
    for flower_color in ["梅花♣", "方片♦", "红桃♥", "黑桃♠"]:
        for number in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]:
            cards.append(f"{flower_color}{number}")
print(cards)
