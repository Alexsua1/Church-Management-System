document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("darkModeToggle");
  const body = document.body;
  if (localStorage.getItem("churchDarkMode") === "on") {
    body.classList.add("dark-mode");
    if (toggle) toggle.checked = true;
  }
  if (toggle) {
    toggle.addEventListener("change", function () {
      body.classList.toggle("dark-mode");
      localStorage.setItem("churchDarkMode", body.classList.contains("dark-mode") ? "on" : "off");
    });
  }
});
