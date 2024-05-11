import pyinputplus as pypi
from random import randint

correctAnswers = 0
incorrectAnswers = 0
number = 100

while number > 0:
    high_num = int(9 + correctAnswers / 10)
    num1 = randint(0, high_num)
    num2 = randint(0, 9 + high_num)

    try:
        pypi.inputStr(f"{num1} * {num2} = ",
                      allowRegexes=['^%s$' % (num1 * num2)],
                      blockRegexes=[('.*', 'Incorrect!')],
                      timeout=10 - correctAnswers / 10,
                      limit=3)

        correctAnswers += 1
        print(f"Correct! You have {correctAnswers} correct answers.")
    except pypi.TimeoutException:
        print("Out of time!")
        incorrectAnswers += 1
        print(f"Incorrect! You have {incorrectAnswers} incorrect answers.")
    except pypi.RetryLimitException:
        print("Out of tries!")
        incorrectAnswers += 1
        print(f"Incorrect! You have {incorrectAnswers} incorrect answers.")

    number -= 1

print(f"Your score is {correctAnswers} correct answers and {incorrectAnswers} incorrect answers!")
