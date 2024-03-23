from wxauto import WeChat


def hong_zha(who, xin_xi):
    wx = WeChat()
    wx.GetSessionList()
    wx.ChatWith(who)

    wx.SendMsg(xin_xi)


if __name__ == "__main__":
    shu_liang = int(input('请输入信息数量：'))
    who = input('请输入信息接收人的名称：')
    xin_xi = input('请输入发送的信息：')
    for _ in range(shu_liang):
        hong_zha(who, xin_xi)
