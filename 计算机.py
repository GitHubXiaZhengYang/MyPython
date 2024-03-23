# name: 计算机
# service: 1.0
# man_name: Mr.X
# time: 2022/12/17

def main(func):
    num = eval(func)
    print(num)


if __name__ == '__main__':
    func = input('请输入算式：')
    main(func)
