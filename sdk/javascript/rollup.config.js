import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import { babel } from '@rollup/plugin-babel';
import terser from '@rollup/plugin-terser';

export default [
  // Browser-friendly UMD build
  {
    input: 'src/index.ts',
    output: {
      name: 'zimagi',
      file: 'dist/index.umd.js',
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
        extensions: ['.ts', '.js', '.json'],
      }),
      commonjs({
        include: /node_modules/,
      }),
      babel({
        babelHelpers: 'bundled',
        exclude: 'node_modules/**',
        extensions: ['.js', '.ts'],
        babelrc: false,
        presets: [
          [
            '@babel/preset-env',
            {
              targets: {
                browsers: ['last 2 versions'],
              },
            },
          ],
          '@babel/preset-typescript',
        ],
      }),
      terser(),
    ],
    external: ['node-fetch', 'crypto-js', 'papaparse'],
  },
  // CommonJS (for Node) build
  {
    input: 'src/index.ts',
    output: [
      {
        file: 'dist/index.js',
        format: 'cjs',
        exports: 'named',
      },
    ],
    plugins: [
      resolve({
        browser: false,
        preferBuiltins: true,
        mainFields: ['main', 'module'],
        extensions: ['.ts', '.js', '.json'],
      }),
      commonjs({
        include: /node_modules/,
      }),
      babel({
        babelHelpers: 'bundled',
        exclude: 'node_modules/**',
        extensions: ['.js', '.ts'],
        babelrc: false,
        presets: [
          [
            '@babel/preset-env',
            {
              targets: {
                node: '22.18.0',
              },
            },
          ],
          '@babel/preset-typescript',
        ],
      }),
    ],
    external: ['node-fetch', 'crypto-js', 'papaparse'],
  },
  // ES module (for bundlers) build
  {
    input: 'src/index.ts',
    output: [
      {
        file: 'dist/index.esm.js',
        format: 'es',
      },
    ],
    plugins: [
      resolve({
        browser: false,
        preferBuiltins: true,
        mainFields: ['module', 'main'],
        extensions: ['.ts', '.js', '.json'],
      }),
      commonjs({
        include: /node_modules/,
      }),
      babel({
        babelHelpers: 'bundled',
        exclude: 'node_modules/**',
        extensions: ['.js', '.ts'],
        babelrc: false,
        presets: [
          [
            '@babel/preset-env',
            {
              modules: false,
            },
          ],
          '@babel/preset-typescript',
        ],
      }),
    ],
    external: ['node-fetch', 'crypto-js', 'papaparse'],
  },
];
