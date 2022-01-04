// Theme Switcher script

// Get theme switch button
const THEME_SWITCH_BUTTON = document.getElementById("theme-switch-button");

// Add event listener to theme switch button
THEME_SWITCH_BUTTON.addEventListener("click", switchTheme);

// Set theme switch button content
if (isDark) {
    enableDarkThemeSwitchButton();
} else {
    enableLightThemeSwitchButton();
}

function switchTheme() {
    // Switch theme
    isDark = !isDark;
    if (isDark) {
        enableDarkTheme();
        enableDarkThemeSwitchButton();
    } else {
        enableLightTheme();
        enableLightThemeSwitchButton();
    }

    // Set localStorage value
    localStorage.setItem(THEME_LOCAL_STORAGE_KEY, JSON.stringify(isDark));
}

function enableDarkThemeSwitchButton() {
    THEME_SWITCH_BUTTON.innerHTML = "<i class='bi bi-moon'></i> Dark";
}

function enableLightThemeSwitchButton() {
    THEME_SWITCH_BUTTON.innerHTML = "<i class='bi bi-sun'></i> Light";
}
