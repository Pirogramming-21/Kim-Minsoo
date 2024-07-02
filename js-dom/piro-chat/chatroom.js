const chatInput = document.getElementById('chat-input');
const hashtagBtn = document.getElementById('hashtag');
const sendBtn = document.getElementById('btn-send');

// 새로고침 했을 때 딱 1번 실행 되면서 자동 포커스
chatInput.focus();

// input이 들어왔을 때 전송 버튼 보이고 안 보이고
chatInput.addEventListener('input', (event) => {
  if(event.target.value !== '') {
    sendBtn.style.display = 'block';
    hashtagBtn.style.display = 'none';
  } else {
    sendBtn.style.display = 'none';
    hashtagBtn.style.display = 'block';
  }
})

chatInput.addEventListener('keypress', (event) => {
  if(event.code === 'Enter') {
    sendBtn.click();
  }
})

let flag = true; // true -> 나 false -> 교육팀장님
const chatBubbleContainer = document.getElementById('chat-bubble');

// 전송 클릭 이벤트
sendBtn.addEventListener('click', () => {
  if(chatInput.value === '') return;
  const contentDiv = document.createElement('div');
  if(flag) {
    flag = false;
    // 내 말풍선 띄우기
    /*
      <div class="my-bubble-content">
        <div class="my-bubble">
          안녕하세요
        </div>
      </div>
    */
    contentDiv.className = 'my-bubble-content';
    const bubble = document.createElement('div');
    bubble.className = 'my-bubble';
    bubble.innerText = chatInput.value;
    contentDiv.appendChild(bubble);
  } else {
    flag = true;
    // 교육팀장님 말풍선 띄우기
    /**
      <div class="your-bubble">
        <div class="profile">
          <img src="./profile.png" alt="">
        </div>
        <div class="bubble-content">
          <div class="name">교육팀장님</div>
          <div class="bubble">
            반가워요
          </div>
        </div>
      </div>
    */
    contentDiv.className = 'your-bubble';
    const profileDiv = document.createElement('div');
    profileDiv.className = 'profile';
    const profileImg = document.createElement('img');
    profileImg.src = './profile.png';
    profileDiv.appendChild(profileImg);
    contentDiv.appendChild(profileDiv);
    const bubbleContent = document.createElement('div');
    bubbleContent.className = 'bubble-content';
    const name = document.createElement('div');
    name.className = 'name';
    name.innerText = '교육팀장님';
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.innerText = chatInput.value;
    bubbleContent.appendChild(name);
    bubbleContent.appendChild(bubble);
    contentDiv.appendChild(bubbleContent);
  }
  chatBubbleContainer.appendChild(contentDiv);
  chatInput.value = '';
  chatBubbleContainer.scrollTop = chatBubbleContainer.scrollHeight;

  // hashtagBtn 다시 보이기
  hashtagBtn.style.display = 'block';
  sendBtn.style.display = 'none';
})
