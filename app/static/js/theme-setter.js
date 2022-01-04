// Theme Setter script

// Set localStorage key
const THEME_LOCAL_STORAGE_KEY = "dark-mode";

// Get localStorage value
const THEME_LOCAL_STORAGE_VALUE = JSON.parse(localStorage.getItem(THEME_LOCAL_STORAGE_KEY));

// Get theme style links
const LIGHT_THEME_STYLE_LINK = document.getElementById("light-theme-style-link");
const DARK_THEME_STYLE_LINK = document.getElementById("dark-theme-style-link");

// Set theme
let isDark = THEME_LOCAL_STORAGE_VALUE;
if (isDark) {
    enableDarkTheme();
} else {
    enableLightTheme();
}

function enableDarkTheme() {
    LIGHT_THEME_STYLE_LINK.setAttribute("rel", "stylesheet alternate");
    DARK_THEME_STYLE_LINK.setAttribute("rel", "stylesheet");
}

function enableLightTheme() {
    DARK_THEME_STYLE_LINK.setAttribute("rel", "stylesheet alternate");
    LIGHT_THEME_STYLE_LINK.setAttribute("rel", "stylesheet");
}
