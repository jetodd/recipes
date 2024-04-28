/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./recipes/templates/recipes/*.html'],
  theme: {
    colors: {
      'red': '#ef4444',
      'rose': '#EDAF9D',
      'navy': '#344259',
      'white': '#FFF9EF'
    },
    extend: {},
  },
  safelist: [
    {
        pattern: /form-control/,
    }
],
  plugins: [],
}

