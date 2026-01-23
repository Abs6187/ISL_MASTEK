const video = document.getElementById("webcam");
const signImage = document.getElementById("sign-image");
const inputBox = document.getElementById("letter-input");
const startBtn = document.getElementById("start-btn");
const quitBtn = document.getElementById("quit-btn");
const resultPopup = document.getElementById("result-popup");
const finalMessage = document.getElementById("final-message");
const closePopupBtn = document.getElementById("close-popup-btn");
const homeBtn = document.getElementById("home-btn");

const playerName = localStorage.getItem("playerName") || "Player";
document.getElementById("player-name").textContent = `👤 Player: ${playerName}`;

const scoreEl = document.getElementById("score");
const streakEl = document.getElementById("streak");
const timeEl = document.getElementById("time-left");
const instruction = document.getElementById("question-text");
const currentLetterDisplay = document.getElementById("current-letter");
const leaderboardBody = document.getElementById("leaderboard-body");

let quizTypes = ["letter-to-sign", "sign-to-letter"];
let currentType = "";
let currentLetter = "";
let totalQuestions = 0;
let correctAnswers = 0;
let score = 0;
let streak = 0;
let timer = null;
let gameStarted = false;

let lastPredicted = "";
let predictionInterval = null;

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => video.srcObject = stream)
  .catch(error => console.error("Webcam error:", error));

function getRandomLetter() {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  return chars[Math.floor(Math.random() * chars.length)];
}

function updateStats() {
  scoreEl.textContent = `⭐ Points: ${score}`;
  streakEl.textContent = `🔥 Streak: ${streak}`;
}

function generateNewQuestion() {
  currentType = quizTypes[Math.floor(Math.random() * quizTypes.length)];
  currentLetter = getRandomLetter();
  totalQuestions++;

  if (currentType === "letter-to-sign") {
    instruction.textContent = "✋ Show the hand sign for:";
    currentLetterDisplay.textContent = currentLetter;
    video.classList.add("active");
    signImage.classList.remove("active");
    inputBox.style.display = "none";
    inputBox.disabled = true;
  } else {
    instruction.textContent = "Guess the letter shown in the sign:";
    currentLetterDisplay.textContent = "";
    signImage.src = `images/quiz_images/${currentLetter}.jpg`;
    signImage.classList.add("active");
    video.classList.remove("active");
    inputBox.style.display = "block";
    inputBox.disabled = false;
    inputBox.value = "";
    inputBox.focus();
  }
}

function handleInput(input) {
  input = input.toUpperCase();
  if (input === currentLetter) {
    score += 3;
    streak++;
    instruction.classList.add("correct-flash");
    setTimeout(() => instruction.classList.remove("correct-flash"), 300);
    updateStats();
    generateNewQuestion();

  } else {
    streak = 0;
    instruction.classList.add("wrong-flash");
    inputBox.classList.add("shake");
    setTimeout(() => {
      instruction.classList.remove("wrong-flash");
      inputBox.classList.remove("shake");
      inputBox.value = "";
    }, 400);
    updateStats();
  }
}

inputBox.addEventListener("input", e => {
  const val = inputBox.value.trim().slice(0, 1);
  inputBox.value = val;
  if (/^[a-zA-Z0-9]$/.test(val)) {
    handleInput(val);
  }
});

startBtn.addEventListener("click", () => {
  if (gameStarted) return;
  gameStarted = true;
  startBtn.style.display = "none";
  quitBtn.disabled = false;
  generateNewQuestion();
  startTimer();
  startPrediction();
});

quitBtn.addEventListener("click", () => {
  endGame("👋 You quit the quiz.");
});

closePopupBtn.addEventListener("click", () => {
  resultPopup.classList.add("hidden");
  homeBtn.style.display = "block";

  // Create and show "Play Again" button
  if (!document.getElementById("play-again-btn")) {
    const playAgainBtn = document.createElement("button");
    playAgainBtn.id = "play-again-btn";
    playAgainBtn.textContent = "🔁 Play Again";
    playAgainBtn.onclick = () => window.location.href = "qm.html";
    playAgainBtn.classList.add("main-btn");
    document.body.appendChild(playAgainBtn);
    playAgainBtn.style.display = "block";
    playAgainBtn.style.margin = "30px auto";
  }
});

function startTimer() {
  let timeLeft = 30;
  timeEl.textContent = `⏳ Time: ${timeLeft}s`;
  timer = setInterval(() => {
    if (!gameStarted) return;
    timeLeft--;
    timeEl.textContent = `⏳ Time: ${timeLeft}s`;

    if (timeLeft <= 10) {
      timeEl.style.color = "red";
      timeEl.style.fontSize = "1.8rem";
      timeEl.style.transform = "scale(1.2)";
      setTimeout(() => {
        timeEl.style.transform = "scale(1)";
      }, 300);
    }

    if (timeLeft <= 0) {
      clearInterval(timer);
      endGame("⏰ Time's up!");
    }
  }, 1000);
}

function endGame(msg) {
  clearInterval(timer);
  gameStarted = false;
  inputBox.disabled = true;
  quitBtn.disabled = true;
  stopPrediction();

  const accuracy = totalQuestions > 0 ? Math.floor((correctAnswers / totalQuestions) * 100) : 0;
  const leaderboard = JSON.parse(localStorage.getItem("quizLeaderboard") || "[]");
  leaderboard.push({ name: playerName, score, accuracy });
  leaderboard.sort((a, b) => b.score === a.score ? b.accuracy - a.accuracy : b.score - a.score);
  const userRank = leaderboard.findIndex(entry => entry.name === playerName && entry.score === score && entry.accuracy === accuracy) + 1;
  localStorage.setItem("quizLeaderboard", JSON.stringify(leaderboard.slice(0, 50)));

  finalMessage.innerHTML = `${msg}<br><br>You answered ${totalQuestions} question(s)and<br>scored ${score} points.<br><br>🏅 Your rank: ${userRank}`;
  resultPopup.classList.remove("hidden");
  renderLeaderboard(leaderboard.slice(0, 15), playerName);
}

function renderLeaderboard(data, highlightName) {
  leaderboardBody.innerHTML = "";
  data.forEach((entry, index) => {
    const tr = document.createElement("tr");
    const medal = index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : index + 1;
    tr.innerHTML = `<td>${medal}</td><td>${entry.name}</td><td>${entry.score}</td>`;
    if (entry.name === highlightName) {
      tr.classList.add("highlighted");
      setTimeout(() => tr.classList.remove("highlighted"), 4000);
    }
    leaderboardBody.appendChild(tr);
  });
}

// ✅ Home button now tracks mid-game exit
homeBtn.addEventListener("click", () => {
  if (gameStarted) {
    endGame("🏃‍♂️ You left the game early.");
    setTimeout(() => window.location.href = "index.html", 500);
  } else {
    window.location.href = "index.html";
  }
});

// ✅ Show leaderboard immediately on page load
const storedLeaderboard = JSON.parse(localStorage.getItem("quizLeaderboard") || "[]");
renderLeaderboard(storedLeaderboard.slice(0, 50), playerName);

function resetGame() {
  // Reset variables
  score = 0;
  streak = 0;
  currentIndex = 0;
  timeLeft = 60;
  answeredQuestions = 0;
  gameActive = true;
  gameStarted = true;

  // Clear and reload words
  const category = categorySelect.value;
  loadWordList(category);

  // Hide result popup
  document.getElementById("result-popup").classList.add("hidden");

  // Reset UI
  categorySelect.disabled = true;
  updateStats();

  // Restart webcam prediction
  stopPrediction();
  startPrediction();

  // Load first question and restart timer
  setTimeout(() => {
    loadNextQuestion();
    startTimer();
  }, 500);
}

function sendFrameToBackend() {
  if (!gameStarted || currentType !== "letter-to-sign") return;
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataURL = canvas.toDataURL('image/jpeg');

  fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: dataURL })
  })
    .then(res => res.json())
    .then(data => {
      const predictedLetter = data.letter;
      if (
        predictedLetter &&
        typeof predictedLetter === "string" &&
        predictedLetter !== lastPredicted
      ) {
        localStorage.setItem("last_prediction", predictedLetter);
        handleInput(predictedLetter);
        lastPredicted = predictedLetter;
      }
    })
    .catch(err => {
      console.error("Prediction API error:", err);
    });
}

function startPrediction() {
  if (predictionInterval) clearInterval(predictionInterval);
  predictionInterval = setInterval(sendFrameToBackend, 1500);
}

function stopPrediction() {
  if (predictionInterval) clearInterval(predictionInterval);
  lastPredicted = "";
}