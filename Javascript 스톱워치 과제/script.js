let timer;
let milliseconds = 0;

const startTimer = () => {
  clearInterval(timer);
  timer = setInterval(updateTimer, 10); // 10밀리초마다 업데이트
}

const stopTimer = () => {
  clearInterval(timer);
  recordLaptime();
}

const resetTimer = () => {
  clearInterval(timer);
  milliseconds = 0;
  updateDisplay();
}

const updateTimer = () => {
  milliseconds += 10; // 10밀리초마다 증가
  updateDisplay();
}

const updateDisplay = () => {
  const display = getFormattedTime();
  document.querySelector('.stopwatch-screen').textContent = display;
}

// 시간 정보를 받아오는 함수
const getFormattedTime = () => {
  const seconds = Math.floor(milliseconds / 1000);
  const remainingMilliseconds = milliseconds % 1000;
  const displaySeconds = seconds.toString().padStart(2, '0');
  const displayMilliseconds = remainingMilliseconds.toString().padStart(3, '0').slice(0, 2);

  return `${displaySeconds}:${displayMilliseconds}`;
}

// display에 표시된 시간을 기록하는 함수
const recordLaptime = () => {
  const lapTime = getFormattedTime();
  addLapTime(lapTime);
}

const addLapTime = (lapTime) => {
  const lapTimeRecord = document.querySelector('.lap-time-records');

  // lap-time-item 요소 생성
  const lapTimeItem = document.createElement('div');
  lapTimeItem.classList.add('lap-time-item');

  // lap-time 요소 생성 및 설정
  const lapTimeElement = document.createElement('div');
  lapTimeElement.textContent = lapTime;
  lapTimeElement.classList.add('lap-time');

  // checkIcon 요소 생성 및 설정
  const checkIcon = document.createElement('div');
  checkIcon.classList.add('checkbox', 'fa-regular', 'fa-circle');

  // lap-time-item에 lapTimeElement와 checkIcon을 추가
  lapTimeItem.appendChild(checkIcon);
  lapTimeItem.appendChild(lapTimeElement);

  // lap-time-records에 lapTimeItem 추가
  lapTimeRecord.appendChild(lapTimeItem);
}

// 체크박스 토글 함수
const toggleCheck = (checkIcon) => {
  checkIcon.classList.toggle('fa-circle');
  checkIcon.classList.toggle('fa-circle-check');
  updateCheckboxKing();
}

// fa-circle-check 상태의 item을 지우는 함수
const removeCheckedLapTimes = () => {
  const lapTimeItems = document.querySelectorAll('.lap-time-item');
  lapTimeItems.forEach(item => {
    const checkIcon = item.querySelector('.fa-circle-check');
    if (checkIcon) {
      item.remove();
    }
  });
}

// 상단의 체크박스를 클릭하면 모든 체크박스가 토글되는 함수
const toggleAllCheckboxes = () => {
  const checkboxKing = document.querySelector('.checkbox-king');
  const isChecked = checkboxKing.classList.contains('fa-circle-check');
  
  const checkboxes = document.querySelectorAll('.lap-time-item .checkbox');
  checkboxes.forEach(checkbox => {
    if (isChecked) {
      checkbox.classList.remove('fa-circle-check');
      checkbox.classList.add('fa-circle');
    } else {
      checkbox.classList.remove('fa-circle');
      checkbox.classList.add('fa-circle-check');
    }
  });
  
  checkboxKing.classList.toggle('fa-circle');
  checkboxKing.classList.toggle('fa-circle-check');
}

// 추가: 하위 체크박스의 체크가 하나라도 해제되면 상위 체크박스가 언체크 되는 기능
const updateCheckboxKing = () => {
  const checkboxKing = document.querySelector('.checkbox-king');
  const checkboxes = document.querySelectorAll('.lap-time-item .checkbox');
  const allChecked = Array.from(checkboxes).every(checkbox => 
    checkbox.classList.contains('fa-circle-check')
  );

  if (allChecked) {
    checkboxKing.classList.remove('fa-circle');
    checkboxKing.classList.add('fa-circle-check');
  } else {
    checkboxKing.classList.remove('fa-circle-check');
    checkboxKing.classList.add('fa-circle');
  }
}

// 이벤트 리스너 설정
document.querySelector('.start').addEventListener("click", startTimer);
document.querySelector('.stop').addEventListener("click", stopTimer);
document.querySelector('.reset').addEventListener("click", resetTimer);
document.querySelector('.trashcan').addEventListener("click", removeCheckedLapTimes);
document.querySelector('.checkbox-king').addEventListener('click', toggleAllCheckboxes);

// 랩타임 기록에 대한 이벤트 위임
document.querySelector('.lap-time-records').addEventListener('click', (event) => {
  if (event.target.classList.contains('checkbox')) {
    toggleCheck(event.target);
  }
});