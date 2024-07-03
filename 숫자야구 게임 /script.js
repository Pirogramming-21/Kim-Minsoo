
//0~9 사이의 중복되지 않는 난수를 생성하는 함수
function makeRandomNumbers() {
  let numbers = [];
  while (numbers.length < 3) {
    let randomNumber = Math.floor(Math.random() * 10);
    if (!numbers.includes(randomNumber)) {
      numbers.push(randomNumber);
    }
  }
  return numbers;
}
// answer에 난수 저장
let answer = makeRandomNumbers();

// 답 확인
console.log(answer)

// enter키를 누르면 확인하기 버튼의 온클릭 이벤트 발생하도록 
// getElementsByClassName는 htmlcollection을 반환하므로, 
// 특정 요소에만 접근하려면 인덱스를 사용해야 함
document.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && attempts > 0) {
    document.getElementsByClassName('submit-button')[0].click();
  }
});


// 한 칸에 숫자 하나가 입력되면 자동으로 다음 칸으로 이동하는 함수
const moveFocus = (current, next) => {
  if (current.value.length === 1) {
      next.focus();
  }
};

document.getElementById('number1').addEventListener('input', () => {
  moveFocus(document.getElementById('number1'), document.getElementById('number2'));
});

document.getElementById('number2').addEventListener('input', () => {
  moveFocus(document.getElementById('number2'), document.getElementById('number3'));
});

document.getElementById('number3').addEventListener('input', () => {
  //마지막 칸이므로 함수 필요 x
});

// 남은 횟수 지정
let attempts = 10;
document.getElementById('attempts').textContent = attempts;

// 각 입력칸에 입력된 숫자를 가져와 정답 여부를 확인하고 틀렸을 시 남은 횟수를 차감하는 함수
const check_numbers = () => {
  let number1 = document.getElementById('number1').value;
  let number2 = document.getElementById('number2').value;
  let number3 = document.getElementById('number3').value;

  // 입력창이 다 채워지지 않은 경우 숫자를 확인하지 않고 초기화
  if ((number1 === '' || number2 === '' || number3 === '')) {
    document.getElementById('number1').value = '';
    document.getElementById('number2').value = '';
    document.getElementById('number3').value = '';
    document.getElementById('number1').focus();
    return;
  }

  // 정수형으로 바꿔주어야 answer과 비교 가능했다 
  let inputs = [parseInt(number1), parseInt(number2), parseInt(number3)];
  let strike = 0;
  let ball = 0;

  for(let i = 0; i < inputs.length; i++) {
    if (inputs[i] === answer[i]) {
      strike++;
    } else if (answer.includes(inputs[i])){
      ball++;
    } 
  }
  
  const resultDisplay = document.querySelector('.result-display');
  const resultDiv = document.getElementById('results');
  const resultText = document.createElement('div')
  resultText.classList.add('check-result');
  resultDiv.appendChild(resultText);

  //스크롤이 자동으로 움직이긴 하나 최하단으로 안 움직임
  //setTimeout을 통해 DOM이 업데이트 된 이후에 실행되도록 만들었더니 해결
  setTimeout(() => {
    resultDisplay.scrollTop = resultDisplay.scrollHeight;
  }, 0);


  if (strike === 0 && ball === 0) {
    // 아웃인 경우
    resultText.innerHTML = `
      <div class="left">${number1} ${number2} ${number3}</div>
      :
      <div class="right">
        <div class="out num-result">O</div>
      </div>
    `;
  } else {
    // 스트라이크 또는 볼이 있는 경우
    resultText.innerHTML = `
      <div class="left">${number1} ${number2} ${number3}</div>
      :
      <div class="right">
        ${strike} <div class="strike num-result">S</div>
        ${ball} <div class="ball num-result">B</div>
      </div>
    `;
  }

attempts--;
document.getElementById('attempts').innerText = attempts;

//성공 혹은 실패 시 이미지를 띄우고 확인하기 버튼을 비활성화
if (strike === 3) {
  document.getElementById('game-result-img').src = './success.png';
  document.getElementsByClassName('submit-button')[0].style.display = 'none';
} else if (attempts <= 0) {
  document.getElementById('game-result-img').src = './fail.png';
  document.getElementsByClassName('submit-button')[0].style.display = 'none';
}

// 값 입력 후 초기화
document.getElementById('number1').value = '';
document.getElementById('number2').value = '';
document.getElementById('number3').value = '';
// 포커스도 다시 줘야 함
document.getElementById('number1').focus();

}