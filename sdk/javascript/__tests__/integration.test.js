/**
 * Integration tests for command and data client functionality
 */

import { CommandClient } from '../src/client/command.js';
import { DataClient } from '../src/client/data.js';

// Skip integration tests if environment variables are not set
const hasEnvVars =
  process.env.ZIMAGI_COMMAND_HOST &&
  process.env.ZIMAGI_COMMAND_PORT &&
  process.env.ZIMAGI_DATA_HOST &&
  process.env.ZIMAGI_DATA_PORT &&
  process.env.ZIMAGI_DEFAULT_ADMIN_TOKEN &&
  process.env.ZIMAGI_ADMIN_API_KEY;

describe('Integration Tests', () => {
  describe('Command Client Integration', () => {
    // Skip tests if environment variables are not configured
    if (!hasEnvVars) {
      test('skipping command integration tests - environment variables not set', () => {
        expect(true).toBe(true);
      });
      return;
    }

    let commandClient;

    beforeAll(() => {
      commandClient = new CommandClient({
        host: process.env.ZIMAGI_COMMAND_HOST,
        port: parseInt(process.env.ZIMAGI_COMMAND_PORT),
        token: process.env.ZIMAGI_DEFAULT_ADMIN_TOKEN,
        encryptionKey: process.env.ZIMAGI_ADMIN_API_KEY,
      });
    });

    test('should get status', async () => {
      const status = await commandClient.getStatus();
      expect(status).toBeDefined();
      expect(status.encryption).toBeDefined();
    }, 10000); // Increase timeout to 10 seconds

    test('should get schema', async () => {
      const schema = await commandClient.getSchema();
      expect(schema).toBeDefined();
      expect(schema.commands).toBeDefined();
    }, 20000); // Increase timeout to 10 seconds
  });

  describe('Data Client Integration', () => {
    // Skip tests if environment variables are not configured
    if (!hasEnvVars) {
      test('skipping data integration tests - environment variables not set', () => {
        expect(true).toBe(true);
      });
      return;
    }

    let dataClient;

    beforeAll(() => {
      dataClient = new DataClient({
        host: process.env.ZIMAGI_DATA_HOST,
        port: parseInt(process.env.ZIMAGI_DATA_PORT),
        token: process.env.ZIMAGI_DEFAULT_ADMIN_TOKEN,
        encryptionKey: process.env.ZIMAGI_ADMIN_API_KEY,
      });
    });

    test('should get status', async () => {
      const status = await dataClient.getStatus();
      expect(status).toBeDefined();
      expect(status.encryption).toBeDefined();
    }, 10000); // Increase timeout to 10 seconds

    test('should get schema', async () => {
      const schema = await dataClient.getSchema();
      expect(schema).toBeDefined();
      expect(schema.paths).toBeDefined();
    }, 20000); // Increase timeout to 10 seconds

    test('should list users', async () => {
      const users = await dataClient.list('user');
      expect(users).toBeDefined();
      expect(users.results).toBeDefined();
    }, 10000); // Increase timeout to 10 seconds
  });
});
