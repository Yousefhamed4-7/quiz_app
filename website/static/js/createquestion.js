let select = document.querySelector("form select");
let mcq = document.querySelector(".MCQ");
let tf = document.querySelector(".TF");
let sq = document.querySelector(".SQ");

function hideall() {
  mcq.style.display = "none";
  tf.style.display = "none";
  sq.style.display = "none";
}
hideall();
sq.style.display = "block";

select.onchange = () => {
  hideall();
  document.querySelector(`.${select.value}`).style.display = "block";
};