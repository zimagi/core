/**
 * Tests for client implementations
 */

import { BaseAPIClient } from '../src/client/base';
import { CommandClient } from '../src/client/command';
import { DataClient } from '../src/client/data';
import { ClientError } from '../src/exceptions';

describe('BaseAPIClient', () => {
  test('should initialize with default options', () => {
    const client = new BaseAPIClient({
      port: 5123,
    });

    expect(client.host).toBe('localhost');
    expect(client.port).toBe(5123);
    expect(client.user).toBe('admin');
    expect(client.token).toBe('uy5c8xiahf93j2pl8s00e6nb32h87dn3');
    expect(client.protocol).toBe('http');
    expect(client.verifyCert).toBe(false);
  });

  test('should throw error when transport is not defined', async () => {
    const client = new BaseAPIClient({
      port: 5123,
    });

    await expect(client._request('GET', 'http://localhost:5123')).rejects.toThrow(ClientError);
  });

  test('should format service URL correctly', () => {
    const client = new BaseAPIClient({
      protocol: 'http',
      host: 'localhost',
      port: 8080,
    });

    expect(client.baseURL).toBe('http://localhost:8080/');
  });
});

describe('CommandClient', () => {
  test('should initialize with default options', () => {
    const client = new CommandClient({
      host: process.env.ZIMAGI_COMMAND_HOST || 'localhost',
      port: process.env.ZIMAGI_COMMAND_PORT
        ? parseInt(process.env.ZIMAGI_COMMAND_PORT || '5123', 10)
        : 5123,
      token: process.env.ZIMAGI_DEFAULT_ADMIN_TOKEN || 'uy5c8xiahf93j2pl8s00e6nb32h87dn3',
      encryptionKey: process.env.ZIMAGI_ADMIN_API_KEY || null,
    });

    expect(client.host).toBe(process.env.ZIMAGI_COMMAND_HOST || 'localhost');
    expect(client.port).toBe(
      process.env.ZIMAGI_COMMAND_PORT
        ? parseInt(process.env.ZIMAGI_COMMAND_PORT || '5123', 10)
        : 5123
    );
    expect(client.user).toBe('admin');
    expect(client.token).toBe(
      process.env.ZIMAGI_DEFAULT_ADMIN_TOKEN || 'uy5c8xiahf93j2pl8s00e6nb32h87dn3'
    );
    expect(client.protocol).toBe('http');
    expect(client.verifyCert).toBe(false);
  });

  test('should normalize command paths', () => {
    const client = new CommandClient({
      host: 'localhost',
      port: 5123,
    });

    // Override the method for testing
    client._normalizePath = function (name: string): string {
      return name.replace(/\s+/g, '/').replace(/\./g, '/');
    };

    expect(client._normalizePath('module add')).toBe('module/add');
    expect(client._normalizePath('module.add')).toBe('module/add');
  });
});

describe('DataClient', () => {
  test('should initialize with default options', () => {
    const client = new DataClient({
      host: process.env.ZIMAGI_DATA_HOST || 'localhost',
      port: process.env.ZIMAGI_DATA_PORT
        ? parseInt(process.env.ZIMAGI_DATA_PORT || '5323', 10)
        : 5323,
      token: process.env.ZIMAGI_DEFAULT_ADMIN_TOKEN || 'uy5c8xiahf93j2pl8s00e6nb32h87dn3',
      encryptionKey: process.env.ZIMAGI_ADMIN_API_KEY || null,
    });

    expect(client.host).toBe(process.env.ZIMAGI_DATA_HOST || 'localhost');
    expect(client.port).toBe(
      process.env.ZIMAGI_DATA_PORT ? parseInt(process.env.ZIMAGI_DATA_PORT || '5323', 10) : 5323
    );
    expect(client.user).toBe('admin');
    expect(client.token).toBe(
      process.env.ZIMAGI_DEFAULT_ADMIN_TOKEN || 'uy5c8xiahf93j2pl8s00e6nb32h87dn3'
    );
    expect(client.protocol).toBe('http');
    expect(client.verifyCert).toBe(false);
  });

  test('should format API paths correctly', () => {
    const client = new DataClient({
      host: 'localhost',
      port: 5323,
    });

    const result1 = client._formatOptions('GET', { tags: ['tag1', 'tag2'] });
    expect(result1).toEqual({
      tags: 'tag1,tag2',
    });

    const result2 = client._formatOptions('POST', { config: { key: 'value' } });
    expect(result2).toEqual({
      config: '{"key":"value"}',
    });
  });
});
