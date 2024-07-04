def brGame():
    while True:
        try:
            count = int(input('부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : '))
            if count in [1, 2, 3]:
                return count
            else:
                print("1, 2, 3 중 하나를 입력하세요.")
        except ValueError:
            print("정수를 입력하세요.")

num = 0

while num <= 31:
    count_A = brGame()
    for i in range(1, count_A + 1):
        num += 1
        print(f"playerA : {num}")
    if num >= 31:
        print("PlayerB win!")
        break

    count_B = brGame()
    for i in range(1, count_B + 1):
        num += 1
        print(f"playerB : {num}")
    if num >= 31:
        print("PlayerA win!")
        break
