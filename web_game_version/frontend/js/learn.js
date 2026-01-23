const input = document.getElementById("text-input");
const keys = document.querySelectorAll(".key");
const image = document.getElementById("sign-image");

// Path builder for valid characters
function getImageFor(char) {
  char = char.toUpperCase();
  if (!/^[A-Z0-9]$/.test(char)) return "ISL.jpg";
  return `images/signimages/${char}.jpg`;
}

// When typing directly into the input field
input?.addEventListener("input", () => {
  const val = input.value.toUpperCase();
  if (val.length > 1) {
    input.value = val[0];
  }

  updateImage(input.value);
});

// When clicking on the virtual keyboard
keys.forEach(key => {
  key.addEventListener("click", () => {
    const value = key.textContent.toUpperCase();
    if (input) input.value = value;
    updateImage(value);
  });
});

// When pressing a key on physical keyboard
document.addEventListener("keydown", (event) => {
  const char = event.key.toUpperCase();
  if (/^[A-Z0-9]$/.test(char)) {
    if (input) input.value = char;
    updateImage(char);
  }
});

function updateImage(char) {
  if (/^[A-Z0-9]$/.test(char)) {
    image.src = `images/images/${char}.jpg`;
  } else {
    image.src = "ISL.jpg";
  }
}
