const modeButtons = document.querySelectorAll(".mode-button");
const nameInput = document.getElementById("player-name");
const errorMsg = document.getElementById("error-msg");
const nameBox = document.querySelector(".name-box");

modeButtons.forEach(button => {
  button.addEventListener("click", e => {
    e.preventDefault();
    const name = nameInput.value.trim();
    if (name === "") {
      errorMsg.textContent = "Please enter your name!";
      nameBox.classList.add("shake");
      setTimeout(() => nameBox.classList.remove("shake"), 400);
      return;
    }
    localStorage.setItem("playerName", name);
    window.location.href = button.dataset.mode;
  });
});
