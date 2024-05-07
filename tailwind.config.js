/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./recipes/templates/recipes/*.html"],
  theme: {
    colors: {
      red: "#E55937",
      rose: "#eab7a8",
      navy: "#313849",
      white: "#FFF9EF",
    },
    extend: {},
  },
  safelist: [
    {
      pattern: /form-control/,
    },
  ],
  plugins: [],
};
