//---	Imports		---
import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import { terser } from 'rollup-plugin-terser';
import postcss from 'rollup-plugin-postcss';

export default {
  input: 'src/main.js',
  output: {
    globals: {
      '@fullcalendar/core': 'core',
      '@fullcalendar/daygrid': 'dayGridPlugin',
    },
    file: 'public/build/bundle.js',
    format: 'iife',
    name: 'app',
  },
  plugins: [
    svelte({
      compilerOptions: {
        dev: process.env.NODE_ENV !== 'production',
        css: false,
      },
      emitCss: true,
    }),
    postcss({
      extract: 'public/build/styles.css',
      minimize: true,
    }),
    resolve({
      browser: true,
    }),
    commonjs(),
    terser(),
  ],
};
