const slider = document.getElementById('slider');
const text = document.querySelector('.text');
const texts = text.children;

slider.addEventListener('input', (event) => {
  console.log(event);
  for(let text of texts) {
    text.style.fontWeight = event.target.value * 10;
  }
});