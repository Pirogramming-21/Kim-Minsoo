const minusBtn = document.getElementById('minus');
const plusBtn = document.getElementById('plus');
const countText = document.getElementById('cnt');

minusBtn.addEventListener('click', () => {
  countText.innerText = Number(countText.innerText) - 1;
})

plusBtn.addEventListener('click', () => {
  countText.innerText = Number(countText.innerText) + 1;
})