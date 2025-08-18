module.exports = {
  testEnvironment: 'node',
  collectCoverageFrom: ['src/**/*.ts', '!src/index.ts'],
  testMatch: ['tests/**/*.ts', '**/?(*.)+(spec|test).ts'],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  transform: {
    '^.+\\.ts$': 'babel-jest',
  },
};
