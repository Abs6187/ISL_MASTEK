const keys = document.querySelectorAll(".key");
const image = document.getElementById("sign-image");

function updateImage(char) {
  char = char.toUpperCase();
  if (/^[A-Z0-9]$/.test(char)) {
    image.src = `images/quiz_images/${char}.jpg`;
    image.onerror = function () {
      this.src = 'images/quiz_images/A.jpg';
      this.onerror = null;
    };
  } else {
    image.src = 'images/quiz_images/A.jpg';
  }
}

keys.forEach(key => {
  key.addEventListener("click", () => {
    const value = key.textContent.toUpperCase();
    updateImage(value);

    keys.forEach(k => k.classList.remove("active-key"));
    key.classList.add("active-key");
  });
});

document.addEventListener("keydown", (event) => {
  const char = event.key.toUpperCase();
  if (/^[A-Z0-9]$/.test(char)) {
    updateImage(char);

    keys.forEach(k => {
      k.classList.remove("active-key");
      if (k.textContent === char) k.classList.add("active-key");
    });
  }
});
