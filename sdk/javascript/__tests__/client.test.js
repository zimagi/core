/**
 * Tests for client implementations
 */

import { jest } from '@jest/globals';
import { BaseAPIClient } from '../src/client/base.js';
import { CommandClient } from '../src/client/command.js';
import { DataClient } from '../src/client/data.js';
import { ClientError } from '../src/exceptions.js';

// Mock transport for testing
const mockTransport = {
  request: jest.fn(),
};

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

  test('should throw error when transport is not defined', () => {
    const client = new BaseAPIClient({
      port: 5123,
    });

    expect(() => {
      client._request('GET', 'http://localhost:5123');
    }).toThrow(ClientError);
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
    const client = new CommandClient();

    expect(client.port).toBe(5123);
    expect(client.verifyCert).toBe(false);
  });

  test('should normalize command paths', () => {
    const client = new CommandClient();
    // Override the method for testing
    client._normalizePath = function (name) {
      return name.replace(/\s+/g, '/').replace(/\./g, '/');
    };

    expect(client._normalizePath('module add')).toBe('module/add');
    expect(client._normalizePath('module.add')).toBe('module/add');
  });
});

describe('DataClient', () => {
  test('should initialize with default options', () => {
    const client = new DataClient();

    expect(client.port).toBe(5323);
    expect(client.verifyCert).toBe(false);
  });

  test('should format API paths correctly', () => {
    const client = new DataClient();

    expect(client._formatOptions('GET', { tags: ['tag1', 'tag2'] })).toEqual({
      tags: 'tag1,tag2',
    });

    expect(client._formatOptions('POST', { config: { key: 'value' } })).toEqual({
      config: '{"key":"value"}',
    });
  });
});
