=====================================================
README for Directory: sdk/javascript
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the main entry point and core implementation for the Zimagi JavaScript SDK. It provides a comprehensive set of functionalities for interacting with Zimagi backend services, including command execution, data management, authentication, encryption, caching, and performance monitoring, all designed to be consumed by client-side JavaScript applications.

**Key Functionality**
   *   Provides base classes and specific client implementations for Command and Data API interactions.
   *   Manages authentication and encryption for secure communication with Zimagi services.
   *   Offers a robust message system for handling various types of responses (status, data, info, error).
   *   Includes a flexible codec system for encoding and decoding different data formats (JSON, CSV, OpenAPI JSON, Zimagi JSON).
   *   Implements a caching mechanism and performance monitoring for optimized client operations.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed for JavaScript environments, primarily targeting execution within Node.js or modern web browsers as an integral part of the Zimagi JavaScript SDK. It is built to be compatible with standard JavaScript runtimes.

**Local Dependencies**
   This directory relies on standard JavaScript features and the `fetch` API for making HTTP requests. It also depends on internal SDK components for error handling, command-specific responses, message parsing, and utility functions. Key external dependencies include `papaparse` for CSV handling, `@babel/core`, `@babel/preset-env`, `@babel/preset-typescript` for Babel transpilation, `@rollup/plugin-babel`, `@rollup/plugin-commonjs`, `@rollup/plugin-node-resolve`, `@rollup/plugin-terser` for Rollup bundling, `eslint`, `eslint-config-prettier`, `eslint-plugin-prettier` for linting, `jest` for testing, `prettier` for code formatting, and `typescript` for type checking.


File Structure and Descriptions
-------------------------------

**sdk/javascript/src**
     **Role:** This directory serves as the main entry point and core implementation for the Zimagi JavaScript SDK.
     **Detailed Description:** It provides a comprehensive set of functionalities for interacting with Zimagi backend services, including command execution, data management, authentication, encryption, caching, and performance monitoring, all designed to be consumed by client-side JavaScript applications. It contains all the source code for the SDK's modules, clients, transports, codecs, and utilities.

**sdk/javascript/tests**
     **Role:** This directory serves as the comprehensive testing suite for the JavaScript SDK.
     **Detailed Description:** It ensures the reliability, correctness, and integration of the SDK's various components by validating client interactions, message handling, schema parsing, transport layers, and overall system integration. It contains unit and integration tests for the SDK's functionalities.

**sdk/javascript/package.json**
     **Role:** This file defines the project's metadata and manages its dependencies.
     **Detailed Description:** It specifies the project name, version, description, license, and scripts for building, testing, and linting. It also lists all production dependencies (e.g., `papaparse`) and development dependencies (e.g., `jest`, `rollup`, `typescript`, `eslint`) required for the SDK.

**sdk/javascript/.eslintrc.cjs**
     **Role:** This file configures the ESLint linter for the JavaScript SDK.
     **Detailed Description:** It defines the linting rules, environment settings (browser, Node.js, ES2021), and parser options for the project. It extends `eslint:recommended` and includes rules to enforce code quality and consistency, such as `no-console`, `no-unused-vars`, and `prefer-const`.

**sdk/javascript/package-lock.json**
     **Role:** This file records the exact dependency tree of the project.
     **Detailed Description:** It ensures that subsequent installations of the project use the exact same versions of dependencies, providing deterministic builds. It lists all direct and transitive dependencies with their versions, integrity hashes, and where they were resolved from.

**sdk/javascript/jest.config.cjs**
     **Role:** This file configures the Jest testing framework for the JavaScript SDK.
     **Detailed Description:** It specifies the test environment (`node`), files to collect coverage from, test match patterns, coverage reporters, and how TypeScript files should be transformed using `babel-jest`.

**sdk/javascript/README.md**
     **Role:** This file provides a quick overview and usage instructions for the Zimagi JavaScript SDK.
     **Detailed Description:** It includes information on installation, basic usage examples for the `CommandClient` and `DataClient`, and a summary of their constructor options and methods. It serves as the primary entry point for developers looking to use the SDK.

**sdk/javascript/babel.config.cjs**
     **Role:** This file configures Babel for transpiling JavaScript and TypeScript code.
     **Detailed Description:** It defines the Babel presets used, specifically `@babel/preset-env` for targeting specific environments (like the current Node.js version) and `@babel/preset-typescript` for TypeScript support. This configuration is used during the build and test processes.

**sdk/javascript/deploy.sh**
     **Role:** This script automates the deployment process of the JavaScript SDK to the npm registry.
     **Detailed Description:** It handles setting up npm authentication using `PKG_NPM_TOKEN`, updating the package version from the main application's `VERSION` file, installing dependencies, building the distribution files using Rollup, publishing the package to npm, and cleaning up temporary files.

**sdk/javascript/.prettierrc**
     **Role:** This file configures the Prettier code formatter for the JavaScript SDK.
     **Detailed Description:** It defines formatting rules such as semicolon usage, trailing commas, single quotes, print width, and tab width, ensuring consistent code style across the project.

**sdk/javascript/rollup.config.js**
     **Role:** This file configures Rollup.js for bundling the JavaScript SDK into various output formats.
     **Detailed Description:** It defines multiple build configurations for browser-friendly UMD, CommonJS (for Node), and ES module (for bundlers) outputs. It specifies input files, output formats, external dependencies, and integrates Rollup plugins like `@rollup/plugin-node-resolve`, `@rollup/plugin-commonjs`, `@rollup/plugin-babel`, and `@rollup/plugin-terser` for dependency resolution, CommonJS conversion, Babel transpilation, and minification.

**sdk/javascript/tsconfig.json**
     **Role:** This file configures the TypeScript compiler for the JavaScript SDK.
     **Detailed Description:** It defines compiler options such as target ECMAScript version, module system, output directory, strictness checks, declaration file generation, source map generation, and inclusion/exclusion patterns for source files. It ensures type safety and proper compilation of TypeScript code.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The typical execution flow begins when a JavaScript application imports and instantiates either a `CommandClient` or `DataClient` from the `sdk/javascript/src` directory. Upon instantiation, the client's `initialize()` method is often called, which in turn uses `BaseAPIClient` (from `sdk/javascript/src`) to fetch the API schema via a `GET` request. This request is handled by the appropriate transport (from `sdk/javascript/src`), which uses the `fetch` API and applies authentication (from `sdk/javascript/src`) and encryption (from `sdk/javascript/src`) if configured. The response is then decoded by one of the codecs (from `sdk/javascript/src`) and structured according to the schema definitions (from `sdk/javascript/src`). Subsequent API calls made through the client (e.g., `execute` for commands, `create` for data) follow a similar path, leveraging the transport, authentication, encryption, and codec layers. Performance metrics are collected throughout this process by `PerformanceMonitor` (from `sdk/javascript/src`), and frequently accessed data may be cached by `Cache` (from `sdk/javascript/src`). Errors encountered at any stage are handled by the exception classes defined in `sdk/javascript/src`. The `sdk/javascript/src/index.ts` file serves as the primary entry point for consuming all these functionalities.

**External Interfaces**
   The code in `sdk/javascript` primarily interacts with the Zimagi Command API and Data API endpoints over HTTP/HTTPS. It relies on the underlying Node.js environment and network stack to establish HTTP/HTTPS connections to the Zimagi backend services. Authentication is handled via tokens, potentially encrypted. Data is exchanged in various formats (JSON, CSV) as defined by the codecs. It also interacts with the browser's `console` for debugging and logging purposes. The `deploy.sh` script interacts with the npm registry for package publication.
