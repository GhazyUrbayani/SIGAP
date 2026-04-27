/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: '#F7F6F3',
          subtle: '#EFEDE8',
        },
        surface: {
          DEFAULT: '#FFFFFF',
          raised: '#FDFDFC',
        },
        border: {
          DEFAULT: '#E8E4DC',
          strong: '#C9C4B8',
        },
        text: {
          primary: '#1C1916',
          secondary: '#6B6560',
          tertiary: '#9C968F',
          inverse: '#FAFAF8',
        },
        zone: {
          green: '#1A7A4A',
          'green-bg': '#EBFAF3',
          'green-muted': '#D1F0E0',
          yellow: '#B45309',
          'yellow-bg': '#FFF8EB',
          'yellow-muted': '#FDECC8',
          red: '#B91C1C',
          'red-bg': '#FFF1F0',
          'red-muted': '#FFD9D9',
          'red-pulse': '#EF4444',
        },
        accent: {
          DEFAULT: '#1B4F72',
          hover: '#154060',
          subtle: '#E8F0F7',
        },
      },
      fontFamily: {
        display: ['Syne', 'Plus Jakarta Sans', 'sans-serif'],
        body: ['Inter', 'DM Sans', 'sans-serif'],
        data: ['JetBrains Mono', 'IBM Plex Mono', 'monospace'],
      },
      fontSize: {
        xs: '0.64rem',
        sm: '0.8rem',
        base: '1rem',
        lg: '1.25rem',
        xl: '1.563rem',
        '2xl': '1.953rem',
        '3xl': '2.441rem',
      },
      borderRadius: {
        sm: '4px',
        md: '8px',
        lg: '12px',
        xl: '16px',
      },
      boxShadow: {
        xs: '0 1px 2px rgba(28,25,22,0.06)',
        sm: '0 1px 3px rgba(28,25,22,0.10), 0 1px 2px rgba(28,25,22,0.06)',
        md: '0 4px 6px rgba(28,25,22,0.07), 0 2px 4px rgba(28,25,22,0.06)',
        lg: '0 10px 15px rgba(28,25,22,0.08), 0 4px 6px rgba(28,25,22,0.05)',
        'zone-red': '0 0 0 3px rgba(185,28,28,0.15)',
      },
      keyframes: {
        'zone-pulse': {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(185,28,28,0.4)' },
          '50%': { boxShadow: '0 0 0 8px rgba(185,28,28,0)' },
        },
        'count-up': {
          from: { opacity: '0', transform: 'translateY(4px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      animation: {
        'zone-pulse': 'zone-pulse 2s infinite',
        'count-up': 'count-up 800ms ease-out',
        shimmer: 'shimmer 1.5s ease-in-out infinite',
      },
    },
  },
  plugins: [],
};
