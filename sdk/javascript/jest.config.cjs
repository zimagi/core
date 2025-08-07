module.exports = {
  testEnvironment: 'node',
  collectCoverageFrom: ['src/**/*.ts', '!src/index.ts'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  transform: {
    '^.+\\.ts$': 'babel-jest',
  },
  transformIgnorePatterns: ['/node_modules/(?!node-fetch)/'],
  moduleNameMapper: {
    '^node-fetch$': '<rootDir>/node_modules/node-fetch/src/index.js',
  },
};
