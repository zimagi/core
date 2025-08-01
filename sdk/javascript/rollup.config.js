import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import { babel } from '@rollup/plugin-babel';
import terser from '@rollup/plugin-terser';

// Import package.json with JSON assertion
import pkg from './package.json' with { type: 'json' };

export default [
  // Browser-friendly UMD build
  {
    input: 'src/index.js',
    output: {
      name: 'zimagi',
      file: pkg.browser,
      format: 'umd',
      exports: 'named',
      inlineDynamicImports: true,
      globals: {
        'node-fetch': 'fetch',
        'crypto-js': 'CryptoJS',
        papaparse: 'Papa',
      },
    },
    plugins: [
      resolve({
        browser: true,
        preferBuiltins: false,
        mainFields: ['browser', 'module', 'main'],
      }),
      commonjs({
        include: /node_modules/,
      }),
      babel({
        babelHelpers: 'bundled',
        exclude: 'node_modules/**',
      }),
      terser(),
    ],
    external: ['node-fetch', 'crypto-js', 'papaparse'],
  },
  // CommonJS (for Node) build
  {
    input: 'src/index.js',
    output: [
      {
        file: pkg.main,
        format: 'cjs',
        exports: 'named',
      },
    ],
    plugins: [
      resolve({
        browser: false,
        preferBuiltins: true,
        mainFields: ['main', 'module'],
      }),
      commonjs({
        include: /node_modules/,
      }),
      babel({
        babelHelpers: 'bundled',
        exclude: 'node_modules/**',
      }),
    ],
    external: ['node-fetch', 'crypto-js', 'papaparse'],
  },
  // ES module (for bundlers) build
  {
    input: 'src/index.js',
    output: [
      {
        file: pkg.module,
        format: 'es',
      },
    ],
    plugins: [
      resolve({
        browser: false,
        preferBuiltins: true,
        mainFields: ['module', 'main'],
      }),
      commonjs({
        include: /node_modules/,
      }),
      babel({
        babelHelpers: 'bundled',
        exclude: 'node_modules/**',
      }),
    ],
    external: ['node-fetch', 'crypto-js', 'papaparse'],
  },
];
