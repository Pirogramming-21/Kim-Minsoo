num = 0

while True:
  try: 
    count_A = int(input('부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : '))
    if count_A in [1, 2, 3]:
      break
    else:
      print("1, 2, 3 중 하나를 입력하세요.")
  except ValueError:
    print("정수를 입력하세요.")

for i in range(1, count_A + 1):
  num += 1
  print(f"player A : {num}")

while True:
  try: 
    count_B = int(input('부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : '))
    if count_B in [1, 2, 3]:
      break
    else:
      print("1, 2, 3 중 하나를 입력하세요.")
  except ValueError:
    print("정수를 입력하세요.")

for i in range(1, count_B + 1):
  num += 1
  print(f"player B : {num}")