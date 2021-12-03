// Theme Switcher script

// Set themes paths
DARK_THEME_PATH = "/static/css/bootstrap-darkly.min.css"
LIGHT_THEME_PATH = "/static/css/bootstrap-flatly.min.css"

// Get localStorage value
const LOCAL_STORAGE_KEY = "dark-mode";
const LOCAL_STORAGE_VALUE = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));

// Get theme style link and theme switcher
const THEME_STYLE_LINK = document.getElementById("theme-style-link");
const THEME_SWITCHER = document.getElementById("theme-switcher")

// Set theme
let isDark = LOCAL_STORAGE_VALUE;
if (isDark) {
    enableDarkTheme();
} else {
    enableLightTheme();
}

function switchTheme() {
    // Switch theme
    isDark = !isDark;
    if (isDark) {
        enableDarkTheme();
    } else {
        enableLightTheme();
    }

    // Set localStorage value
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(isDark));
}

function enableDarkTheme() {
    THEME_STYLE_LINK.setAttribute("href", DARK_THEME_PATH);
    THEME_SWITCHER.innerHTML = "<i class='bi bi-moon'></i> Dark";
}

function enableLightTheme() {
    THEME_STYLE_LINK.setAttribute("href", LIGHT_THEME_PATH);
    THEME_SWITCHER.innerHTML = "<i class='bi bi-sun'></i> Light";
}
