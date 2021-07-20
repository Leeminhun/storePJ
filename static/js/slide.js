let curPos = 0;
let postion = 0;
const IMAGE_WIDTH = 640;
const prevBtn = document.querySelector(".prev")
const nextBtn = document.querySelector(".next")
const images = document.querySelector(".images")

function prev(){
  if(curPos > 0){
    nextBtn.removeAttribute("disabled")
    postion += IMAGE_WIDTH;
    images.style.transform = `translateX(${postion}px)`;
    curPos = curPos - 1;
  }
  if(curPos == 0){
    prevBtn.setAttribute('disabled', 'true')
  }
}
function next(){
  if(curPos < 3){
    prevBtn.removeAttribute("disabled")
    postion -= IMAGE_WIDTH;
    images.style.transform = `translateX(${postion}px)`;
    curPos = curPos + 1;
  }
  if(curPos == 3){
    nextBtn.setAttribute('disabled', 'true')
  }
}

function init(){
  prevBtn.setAttribute('disabled', 'true')
  prevBtn.addEventListener("click", prev)
  nextBtn.addEventListener("click", next)
}

init();