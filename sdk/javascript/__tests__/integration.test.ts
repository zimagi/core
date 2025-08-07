/**
 * Integration tests for command and data client functionality
 */

import { CommandClient } from '../src/client/command';
import { DataClient } from '../src/client/data';

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

    let commandClient: CommandClient;

    beforeAll(() => {
      commandClient = new CommandClient({
        host: process.env.ZIMAGI_COMMAND_HOST || 'localhost',
        port: process.env.ZIMAGI_COMMAND_PORT
          ? parseInt(process.env.ZIMAGI_COMMAND_PORT || '5123', 10)
          : 5123,
        token: process.env.ZIMAGI_DEFAULT_ADMIN_TOKEN || 'uy5c8xiahf93j2pl8s00e6nb32h87dn3',
        encryptionKey: process.env.ZIMAGI_ADMIN_API_KEY || null,
      });
    });

    test('should get status', async () => {
      const status = await commandClient.getStatus();
      expect(status).toBeDefined();
      expect((status as any).encryption).toBeDefined();
    }, 10000); // Increase timeout to 10 seconds

    test('should get schema', async () => {
      const schema = await commandClient.getSchema();
      expect(schema).toBeDefined();
      expect((schema as any).commands).toBeDefined();
    }, 20000); // Increase timeout to 20 seconds
  });

  describe('Data Client Integration', () => {
    // Skip tests if environment variables are not configured
    if (!hasEnvVars) {
      test('skipping data integration tests - environment variables not set', () => {
        expect(true).toBe(true);
      });
      return;
    }

    let dataClient: DataClient;

    beforeAll(() => {
      dataClient = new DataClient({
        host: process.env.ZIMAGI_DATA_HOST || 'localhost',
        port: process.env.ZIMAGI_DATA_PORT
          ? parseInt(process.env.ZIMAGI_DATA_PORT || '5323', 10)
          : 5323,
        token: process.env.ZIMAGI_DEFAULT_ADMIN_TOKEN || 'uy5c8xiahf93j2pl8s00e6nb32h87dn3',
        encryptionKey: process.env.ZIMAGI_ADMIN_API_KEY || null,
      });
    });

    test('should get status', async () => {
      const status = await dataClient.getStatus();
      expect(status).toBeDefined();
      expect((status as any).encryption).toBeDefined();
    }, 10000); // Increase timeout to 10 seconds

    test('should get schema', async () => {
      const schema = await dataClient.getSchema();
      expect(schema).toBeDefined();
      expect((schema as any).paths).toBeDefined();
    }, 20000); // Increase timeout to 20 seconds

    test('should list users', async () => {
      const users = await dataClient.list('user');
      expect(users).toBeDefined();
      expect((users as any).results).toBeDefined();
    }, 10000); // Increase timeout to 10 seconds
  });
});
