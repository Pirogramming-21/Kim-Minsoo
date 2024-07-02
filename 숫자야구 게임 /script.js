
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

let answer = makeRandomNumbers();
console.log(answer)

// 한 칸에 숫자 하나가 입력되면 다음 칸으로 이동하는 함수
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

// 각 입력칸에 입력된 숫자를 가져와 정답 여부를 확인하고 틀렸을 시 남은 횟수를 차감하는 함수

let attempts = 10;

const checkNumbers = () => {
  let number1 = document.getElementById('number1').value;
  let number2 = document.getElementById('number2').value;
  let number3 = document.getElementById('number3').value;

  let inputs = [number1, number2, number3];
  let strike = 0;
  let ball = 0;

  for(let i = 0; i < inputs.length; i++) {
    if (inputs[i] === answer[i]) {
      strike++;
    } else if (answer.includes(inputs[i])){
      ball++;
    } 
  }

  const resultDiv = document.getElementById('results');
  const resultText = document.createElement('div')
  resultText.classList.add('check-result');
  resultText.innerHTML = `
  <div class="left">${number1} ${number2} ${number3}</div>
    :
    <div class="right">
      ${strike} <div class="strike num-result">S</div>
      ${ball} <div class="ball num-result">B</div>
      <div class="out num-result">O</div>
    </div>
`;
resultDiv.appendChild(resultText);

attempts--;
document.getElementById('attempts').innerText = attempts;

if (strike === 3) {
  document.getElementById('game-result-img').src = './success.png';
} else if (attempts <= 0) {
  document.getElementById('game-result-img').src = './fail.png';
}
// 초기화 
document.getElementById('number1').value = '';
document.getElementById('number2').value = '';
document.getElementById('number3').value = '';
document.getElementById('number1').focus();

}