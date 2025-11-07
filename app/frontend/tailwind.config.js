/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Use class strategy for dark mode
  theme: {
    extend: {
      colors: {
        // Light theme
        'light-bg': '#f8f9fa',
        'light-surface': '#ffffff',
        'light-text': '#212529',
        // Dark theme
        'dark-bg': '#0d1117',
        'dark-surface': '#161b22',
        'dark-text': '#c9d1d9',
      },
    },
  },
  plugins: [],
}


