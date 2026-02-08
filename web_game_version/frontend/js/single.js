const playerName = localStorage.getItem("playerName") || "Player";
const categorySelect = document.getElementById("category");
const playerNameEl = document.getElementById("player-name");
const scrambledWordEl = document.getElementById("scrambled-word");
const hintEl = document.querySelector(".hint");
const instruction = document.getElementById("current-instruction");
const currentLetterEl = document.getElementById("current-letter");
const answerLineEl = document.getElementById("answer-line");
const scoreEl = document.getElementById("score");
const streakEl = document.getElementById("streak");
const timeEl = document.getElementById("time-left");
const leaderboardBody = document.getElementById("leaderboard-body");
const playAgainInlineBtn = document.getElementById("inline-play-again-btn");
const startBtn = document.getElementById("start-btn");
const timerWrapper = document.getElementById("timer");

let currentWord = "";
let hint = "";
let jumbled = "";
let currentIndex = 0;
let score = 0;
let streak = 0;
let answeredQuestions = 0;
let wordList = [];
let usedWords = [];
let timeLeft = 60;
let timer;
let gameActive = false;
let gameStarted = false;

playerNameEl.textContent = `👤 Name: ${playerName}`;
loadWordList(categorySelect.value);
setupCamera();

categorySelect.addEventListener("change", e => {
  if (!gameStarted) {
    localStorage.setItem("category", e.target.value);
    loadWordList(e.target.value);
  } else {
    alert("❗ Can't change category after game start.");
    categorySelect.value = localStorage.getItem("category") || "general";
  }
});


startBtn.addEventListener("click", () => {
  soundManager.playClick();

  if (gameStarted) return;
  gameStarted = true;
  gameActive = true;
  categorySelect.disabled = true;
  startPrediction();
  loadNextQuestion();
  startTimer();
});

function setupCamera() {
  const video = document.getElementById("webcam");
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => (video.srcObject = stream))
    .catch(err => console.error("Camera access denied:", err));
}

async function loadWordList(category) {
  try {
    const response = await fetch(`${category}.json`);
    const data = await response.json();
    wordList = [...data];
    shuffleArray(wordList);
    usedWords = [];
  } catch (err) {
    scrambledWordEl.textContent = "Error loading words.";
    console.error("Error loading JSON:", err);
  }
}

function loadNextQuestion() {
  if (wordList.length === 0 || usedWords.length >= wordList.length) {
    return endGame("🎉 You've completed all available words!");
  }

  let nextWordObj;
  do {
    nextWordObj = wordList[Math.floor(Math.random() * wordList.length)];
  } while (usedWords.includes(nextWordObj.word));

  usedWords.push(nextWordObj.word);
  currentWord = nextWordObj.word.toUpperCase();
  hint = nextWordObj.hint;
  jumbled = shuffleWord(currentWord);
  currentIndex = 0;
  updateUI();
}

function updateUI() {
  const isMath = categorySelect.value === "math";

  if (isMath) {
    scrambledWordEl.textContent = `${hint} = ?`;
    hintEl.innerHTML = "";
    instruction.innerHTML = "";
  } else {
    scrambledWordEl.textContent = jumbled;
    hintEl.innerHTML = `
      <button id="reveal-btn" class="hint-button" title="Show Sign Hint">💡</button>
      <button id="ai-btn" class="hint-button" style="margin-left: 10px; background-color: #7b2cbf;" title="Ask AI for a Hint">🤖</button>
    `;
    hintEl.innerHTML += `<span class="hint-text">Hint: ${hint}</span>`;
    hintEl.innerHTML += `<div id="ai-response-text" style="display:none; color: #d0d0ff; margin-top: 10px; font-size: 0.9em; background: rgba(0,0,0,0.5); padding: 5px; border-radius: 5px;"></div>`;

    instruction.innerHTML = "";

    // Hint Reveal Logic
    const revealBtn = document.getElementById("reveal-btn");
    revealBtn.addEventListener("click", () => {
      if (currentIndex < currentWord.length) {
        instruction.innerHTML = `✋ Show hand sign for: <span id="current-letter">${currentWord[currentIndex]}</span>`;
      }
    });

    // AI Intelligent Response Logic
    const aiBtn = document.getElementById("ai-btn");
    const aiTextEl = document.getElementById("ai-response-text");

    aiBtn.addEventListener("click", async () => {
      soundManager.playClick();
      if (aiBtn.disabled) return;
      aiBtn.disabled = true;
      aiTextEl.style.display = "block";
      aiTextEl.textContent = "🤔 AI is thinking...";

      const response = await fetchAIResponse(currentWord);

      if (response && response.content) {
        aiTextEl.textContent = `🤖 AI: ${response.content}`;
      } else {
        aiTextEl.textContent = `⚠️ ${response.error || "AI could not help right now."}`;
      }
      aiBtn.disabled = false;
    });
  }

  updateAnswerLine();
  updateStats();
}

function updateAnswerLine() {
  answerLineEl.textContent = currentWord.split("").map((c, i) => i < currentIndex ? c : "_").join(" ");
}

function updateStats() {
  scoreEl.textContent = `⭐ Score: ${score}`;
  streakEl.textContent = `🔥 Streak: ${streak}`;
  // Always update the leaderboard in real time
  const category = categorySelect.value;
  const leaderboard = getLeaderboard(category);
  renderLeaderboard(leaderboard);
}

// Helper to get leaderboard for current category
function getLeaderboard(category) {
  let leaderboard = JSON.parse(localStorage.getItem("leaderboard") || "[]");
  if (category) {
    leaderboard = leaderboard.filter(entry => entry.category === category);
  }
  leaderboard.sort((a, b) => b.score - a.score);
  return leaderboard.slice(0, 15);
}

function handleInput(input) {
  if (!gameActive) return;
  input = input.toUpperCase();

  if (input === "BACKSPACE" && currentIndex > 0) {
    currentIndex--;
    streak = 0;
    updateUI();
    return;
  }

  if (input === currentWord[currentIndex]) {
    currentIndex++;
    soundManager.playSuccess();

    if (categorySelect.value === "math") {
      score += 1;
    } else {
      score += 2;
    }

    streak++;
    // Add 5 seconds to the timer after each correct letter
    timeLeft += 5;
    timeEl.textContent = timeLeft;
    if (currentIndex === currentWord.length) {
      answeredQuestions++;
      clearInterval(timer);
      timeLeft = 60;
      updateStats();
      setTimeout(() => {
        loadNextQuestion();
        startTimer();
      }, 700);
    }
    updateUI();
  } else {
    soundManager.playError();
    flashIncorrectInput();
    streak = 0;
    updateStats();
  }
}

function flashIncorrectInput() {
  const letterEl = document.getElementById("current-letter");
  if (!letterEl) return; // Prevent error if element is missing
  letterEl.style.color = "red";
  letterEl.style.transform = "scale(1.2)";
  setTimeout(() => {
    letterEl.style.color = "#00ffc8";
    letterEl.style.transform = "scale(1)";
  }, 300);
}

function startTimer() {
  timeLeft = 60;
  timeEl.textContent = timeLeft;
  timerWrapper.classList.remove("red-timer");

  timer = setInterval(() => {
    if (!gameActive) return;

    timeLeft--;
    timeEl.textContent = timeLeft;

    if (timeLeft <= 10) {
      timerWrapper.classList.add("red-timer");
      soundManager.playTick();
    } else {
      timerWrapper.classList.remove("red-timer");
    }

    if (timeLeft <= 0) {
      clearInterval(timer);
      endGame("⏰ Time's up!");
    }
  }, 1000);
}

function endGame(msg) {
  gameActive = false;
  clearInterval(timer);
  stopPrediction();
  const category = categorySelect.value;
  const leaderboard = updateLeaderboard(playerName, score, category);
  const rank = leaderboard.findIndex(entry => entry.name === playerName && entry.score === score) + 1;

  document.getElementById("final-message").innerHTML =
    `${msg}<br>You answered ${answeredQuestions} word(s) and scored ${score} points.<br>📂 Category: ${category}<br>🏅 Your rank is: ${rank}`;
  document.getElementById("result-popup").classList.remove("hidden");

}
document.getElementById("home-btn").style.display = "block";


function updateLeaderboard(name, score, category) {
  let leaderboard = JSON.parse(localStorage.getItem("leaderboard") || "[]");
  leaderboard.push({ name, score, category });

  leaderboard.sort((a, b) => b.score - a.score);
  leaderboard = leaderboard.slice(0, 100);
  localStorage.setItem("leaderboard", JSON.stringify(leaderboard));
  renderLeaderboard(leaderboard);
  return leaderboard;
}

function renderLeaderboard(data) {
  leaderboardBody.innerHTML = "";
  data.forEach((entry, index) => {
    const tr = document.createElement("tr");
    let medal = index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : index + 1;
    tr.innerHTML = `<td>${medal}</td><td>${entry.name}</td><td>${entry.score}</td><td>${entry.category}</td>`;
    if (entry.name === playerName && entry.score === score) {
      tr.style.backgroundColor = "rgba(255,255,255,0.1)";
      tr.style.color = "#00ffc8";
    }
    leaderboardBody.appendChild(tr);
  });
}

document.addEventListener("keydown", e => {
  if (e.key === "Backspace") {
    handleInput(e.key);
  }
});

document.getElementById("quit-btn").addEventListener("click", () => {
  if (gameStarted) {
    endGame("👋 You quit the game.");
  } else {
    window.location.href = "mode.html"; // redirect if the game hasn't started
  }
});

document.getElementById("close-popup-btn").addEventListener("click", () => {
  window.location.href = "mode.html";
});

playAgainInlineBtn.addEventListener("click", () => {
  resetGame();
});

function shuffleWord(word) {
  const chars = word.split("");
  for (let i = chars.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [chars[i], chars[j]] = [chars[j], chars[i]];
  }
  return chars.join("");
}

function shuffleArray(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}
document.getElementById("home-btn").addEventListener("click", () => {
  window.location.href = "index.html";
});

let predictionInterval = null;
let lastPredicted = "";

function startPrediction() {
  predictionInterval = setInterval(() => {
    if (!gameActive) return;
    sendFrameToBackend();
  }, 800);
}

function stopPrediction() {
  clearInterval(predictionInterval);
  lastPredicted = "";
}

// Capture a frame from the video element and send to backend
function sendFrameToBackend() {
  const video = document.getElementById('webcam');
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataURL = canvas.toDataURL('image/jpeg');
  const category = categorySelect.value;

  fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: dataURL, category: category })
  })
    .then(res => res.json())
    .then(data => {
      const predictedLetter = data.letter;
      const confidence = data.confidence || 0;
      if (
        predictedLetter &&
        typeof predictedLetter === "string" &&
        confidence >= 0.5 &&
        predictedLetter !== lastPredicted
      ) {
        localStorage.setItem("last_prediction", predictedLetter);
        handleInput(predictedLetter);
        lastPredicted = predictedLetter;
        setTimeout(() => { lastPredicted = ""; }, 1500);
      }
    })
    .catch(err => console.error("Prediction error:", err));
}

function resetGame() {
  // Reset variables
  score = 0;
  streak = 0;
  currentIndex = 0;
  timeLeft = 60;
  answeredQuestions = 0;
  gameActive = true;
  gameStarted = true;
  lastPredicted = "";

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
