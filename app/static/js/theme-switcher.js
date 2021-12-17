// Theme Switcher script

// Set localStorage key
const THEME_LOCAL_STORAGE_KEY = "dark-mode";

// Get localStorage value
const THEME_LOCAL_STORAGE_VALUE = JSON.parse(localStorage.getItem(THEME_LOCAL_STORAGE_KEY));

// Get theme style links
const LIGHT_THEME_STYLE_LINK = document.getElementById("light-theme-style-link");
const DARK_THEME_STYLE_LINK = document.getElementById("dark-theme-style-link");

// Get theme switch button
const THEME_SWITCH_BUTTON = document.getElementById("theme-switch-button");

// Set theme
let isDark = THEME_LOCAL_STORAGE_VALUE;
if (isDark) {
    enableDarkTheme();
} else {
    enableLightTheme();
}

// Add event listener to theme switch button
THEME_SWITCH_BUTTON.addEventListener("click", switchTheme);

function switchTheme() {
    // Switch theme
    isDark = !isDark;
    if (isDark) {
        enableDarkTheme();
    } else {
        enableLightTheme();
    }

    // Set localStorage value
    localStorage.setItem(THEME_LOCAL_STORAGE_KEY, JSON.stringify(isDark));
}

function enableDarkTheme() {
    LIGHT_THEME_STYLE_LINK.setAttribute("rel", "stylesheet alternate");
    DARK_THEME_STYLE_LINK.setAttribute("rel", "stylesheet");
    THEME_SWITCH_BUTTON.innerHTML = "<i class='bi bi-moon'></i> Dark";
}

function enableLightTheme() {
    DARK_THEME_STYLE_LINK.setAttribute("rel", "stylesheet alternate");
    LIGHT_THEME_STYLE_LINK.setAttribute("rel", "stylesheet");
    THEME_SWITCH_BUTTON.innerHTML = "<i class='bi bi-sun'></i> Light";
}
