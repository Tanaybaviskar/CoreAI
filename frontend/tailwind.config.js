/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        base: "#0B0E11",
        surface: "#12161B",
        surface2: "#171C22",
        border: "#232A31",
        text: "#E7ECEF",
        muted: "#8A96A3",
        accent: "#E8A33D",
        ok: "#34D399",
        warn: "#F5A623",
        err: "#F87171",
      },
      fontFamily: {
        display: ["var(--font-display)", "sans-serif"],
        body: ["var(--font-body)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
      borderRadius: {
        sm: "3px",
        md: "5px",
      },
    },
  },
  plugins: [],
};
