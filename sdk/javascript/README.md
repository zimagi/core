# Zimagi JavaScript SDK

JavaScript SDK for interacting with the Zimagi platform.

## Installation

npm install zimagi-js

## Usage

### Command Client

```js
import { CommandClient } from 'zimagi-js';

// Initialize command client
const commandClient = new CommandClient({
  host: 'localhost',
  port: 5123,
  user: 'admin',
  token: 'your-token',
  encryptionKey: 'your-encryption-key',
});

// Execute a command
const response = await commandClient.execute('module/add', {
  remote: 'https://example.com/module',
  reference: 'module-reference',
  moduleFields: {
    name: 'My Module',
    version: '1.0.0',
  },
});

// Run a task
await commandClient.runTask('module-key', 'task-name', {
  param1: 'value1',
  param2: 'value2',
});

// Extend with a module
await commandClient.extend('https://example.com/module', 'reference', 'provider', {
  field1: 'value1',
  field2: 'value2',
});
```

### Data Client

```js
import { DataClient } from 'zimagi-js';

// Initialize data client
const dataClient = new DataClient({
  host: 'localhost',
  port: 5323,
  user: 'admin',
  token: 'your-token',
  encryptionKey: 'your-encryption-key',
});

// Create a record
const newRecord = await dataClient.create('users', {
  name: 'John Doe',
  email: 'john@example.com',
});

// Get a record by ID
const user = await dataClient.get('users', '123');

// Get a record by key
const userByKey = await dataClient.getByKey('users', 'john-doe');

// List records
const users = await dataClient.list('users', {
  page: 1,
  page_size: 10,
});

// Update a record
await dataClient.update('users', '123', {
  name: 'Jane Doe',
});

// Delete a record
await dataClient.delete('users', '123');

// Get data in CSV format
const csvData = await dataClient.csv('users');

// Get data values
const values = await dataClient.values('users', 'name');

// Get count
const count = await dataClient.count('users');
```

## API Documentation

### CommandClient

#### Constructor Options

- host (string): Host name (default: 'localhost')
- port (number): Port number (default: 5123)
- user (string): Username (default: 'admin')
- token (string): Authentication token (default: 'uy5c8xiahf93j2pl8s00e6nb32h87dn3')
- encryptionKey (string): Encryption key (default: null)
- protocol (string): HTTP protocol (default: 'https')
- verifyCert (boolean): Verify SSL certificate (default: false)

#### Methods

- execute(commandName, options): Execute a command
- extend(remote, reference, provider, fields): Extend with a module
- runTask(moduleKey, taskName, config, options): Run a task
- runProfile(moduleKey, profileKey, config, components, options): Run a profile
- destroyProfile(moduleKey, profileKey, config, components, options): Destroy a profile
- runImports(names, tags, options): Run imports
- runCalculations(names, tags, options): Run calculations

### DataClient

#### Constructor Options

- host (string): Host name (default: 'localhost')
- port (number): Port number (default: 5323)
- user (string): Username (default: 'admin')
- token (string): Authentication token (default: 'uy5c8xiahf93j2pl8s00e6nb32h87dn3')
- encryptionKey (string): Encryption key (default: null)
- protocol (string): HTTP protocol (default: 'https')
- verifyCert (boolean): Verify SSL certificate (default: false)

#### Methods

- create(dataType, fields): Create a record
- update(dataType, id, fields): Update a record
- delete(dataType, id): Delete a record
- get(dataType, id, options): Get a record by ID
- getByKey(dataType, key, options): Get a record by key
- list(dataType, options): List records
- json(dataType, options): Get data in JSON format
- csv(dataType, options): Get data in CSV format
- values(dataType, fieldName, options): Get field values
- count(dataType, fieldName, options): Get record count
- download(datasetName): Download a dataset

## Development

### Building

npm run build

### Testing

npm test

### Linting

npm run lint

## License

Apache 2.0
