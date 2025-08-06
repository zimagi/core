import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import { babel } from '@rollup/plugin-babel';
import terser from '@rollup/plugin-terser';

// Dynamically import package.json
let pkg;
async function loadPkg() {
  if (!pkg) {
    pkg = await import('./package.json', { assert: { type: 'json' } });
    pkg = pkg.default;
  }
  return pkg;
}

export default async function () {
  const pkg = await loadPkg();

  return [
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
}
