let answerContinaer = document.querySelector(".answer ");
answerContinaer.style.height = "0px";
answerContinaer.innerHTML =
  document.querySelector("li[correct='1']").textContent;
let btn = document.querySelector("ul button");
let active = false;
btn.onclick = () => {
  if (active) {
    answerContinaer.style.cssText = `height: 0px;`;
    active = false;
  } else {
    answerContinaer.style.cssText = `height: 50px;`;
    active = true;
  }
};