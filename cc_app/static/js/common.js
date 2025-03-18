// Переключение темы
const themeToggleButton = document.getElementById('theme-toggle');
const body = document.body;

let isDarkTheme = true;

themeToggleButton.addEventListener('click', () => {
    isDarkTheme = !isDarkTheme;

    if (isDarkTheme) {
        body.classList.remove('light-theme');
        themeToggleButton.textContent = '🌙'; // Луна для темной темы
    } else {
        body.classList.add('light-theme');
        themeToggleButton.textContent = '☀️'; // Солнце для светлой темы
    }
});
