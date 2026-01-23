document.addEventListener("DOMContentLoaded", () => {
  renderScrambleLeaderboard();
  renderQuizLeaderboard();
});

function renderScrambleLeaderboard() {
  const tbody = document.getElementById("scramble-leaderboard-body");
  let data = JSON.parse(localStorage.getItem("leaderboard") || "[]");
  if (data.length === 0) return;

  tbody.innerHTML = "";
  data.sort((a, b) => b.score - a.score);
  data.slice(0, 10).forEach((entry, index) => {
    const medal = index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : index + 1;
    const row = `<tr><td>${medal}</td><td>${entry.name}</td><td>${entry.score}</td><td>${entry.category}</td></tr>`;
    tbody.innerHTML += row;
  });
}

function renderQuizLeaderboard() {
  const tbody = document.getElementById("quiz-leaderboard-body");
  let data = JSON.parse(localStorage.getItem("quizLeaderboard") || "[]");
  if (data.length === 0) return;

  tbody.innerHTML = "";
  data.sort((a, b) => b.score - a.score || b.accuracy - a.accuracy);
  data.slice(0, 50).forEach((entry, index) => {
    const medal = index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : index + 1;
    const row = `<tr><td>${medal}</td><td>${entry.name}</td><td>${entry.score}</td></tr>`;
    tbody.innerHTML += row;
  });
}
