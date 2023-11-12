let header = document.querySelector("header");
let main = document.querySelector("main");
main.style.paddingTop = header.offsetHeight + "px";
let link = document.querySelector(".links");

function menu() {
  link.classList.toggle("active");
}

function toggleDiv(a) {
  a = a.parentNode.parentNode.parentNode
  replybox = a.querySelector('.comment-box')
  if (replybox.style.display === "none") {
    replybox.style.display = "block";
  } else {
    replybox.style.display = "none";
  }
}



const btns = document.querySelectorAll('.nav-btn');
const slides = document.querySelectorAll('.video-slider')
const contents = document.querySelectorAll('.content')  
var sliderNav = function(index) {
  btns.forEach((btn) => {
      btn.classList.remove('active');
  })

  slides.forEach((slide) => {
      slide.classList.remove('active');
  })

  contents.forEach((content) => {
      content.classList.remove('active');
  })

  btns[index].classList.add('active');
  slides[index].classList.add('active');
  contents[index].classList.add('active');
}

btns.forEach((btn, i)=> {
  btn.addEventListener('click', () => {
      sliderNav(i);
  })
})

