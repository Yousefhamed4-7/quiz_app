let select = document.querySelector("select");
let questions = document.querySelectorAll(".card");
function hideall() {
  questions.forEach((question) => {
    question.style.display = "none";
  });
}
select.onchange = () => {
  hideall();
  questions.forEach((question) => {
    if (question.getAttribute("solved") == "1" && select.value == "solved") {
      question.style.display = "block";
    } else if (
      question.getAttribute("solved") == "0" &&
      select.value == "unsolved"
    ) {
      question.style.display = "block";
    } else if (select.value == "all") {
      question.style.display = "block";
    }
  });
};