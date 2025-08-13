import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{js, jsx, ts ,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        primary: ['"Albert Sans"', 'sans-serif'],
        mono: ['"Azeret Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
};

export default config;
