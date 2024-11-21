let right = 0;
let questionnumber = document.querySelectorAll(".question").length;
function diable_buttons(element) {
  element.querySelectorAll("button").forEach((btn) => {
    btn.setAttribute("disabled", true);
  });
}
function isdone() {
  return document.querySelectorAll(".question").length == 0 && (document.querySelectorAll(".blank").length == 0 || document.querySelectorAll(".blank").length == 1);
}
function handel_questions(btn) {
  btn.onclick = () => {
    fetch(`http://127.0.0.1:5000/api/iscorrect`, {
  method: "POST",
  body: JSON.stringify({
    question_id: btn.parentElement.parentElement.querySelector("input[type='hidden']").value,
    choice_id: btn.getAttribute("choice_id"),
    user_answer: btn.parentElement.parentElement.querySelector(".user_answer").value
  }),
  headers: {
    "Content-type": "application/json",
  },
})
  .then((response) => response.json())
  .then((data) => {
    if(data["correct"] == 1)
    {
      btn.classList.add("correct");
      right++;
    }
    else{
      btn.classList.add("incorrect");
    }
  });
    setTimeout(function () {
      btn.parentElement.parentElement.remove();
    }, 1000);
    diable_buttons(btn.parentElement);
  };
}
document.querySelectorAll("button").forEach(handel_questions);
intervalid = setInterval(() => {
  if (isdone()) {
    document.querySelector("#score").innerHTML = `${right}/ ${questionnumber} `;
    document.querySelector(".done").style.display = "flex";
    clearInterval(intervalid);
  }
}, 500);