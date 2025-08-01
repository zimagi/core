/**
 * Tests for transport layer implementations
 */

import { BaseTransport } from '../src/transports/base.js';
import { CommandHTTPTransport } from '../src/transports/command.js';
import { DataHTTPTransport } from '../src/transports/data.js';
import { ClientError, ConnectionError, ResponseError } from '../src/exceptions.js';

// Mock client for testing
const mockClient = {
  auth: {
    apply: (headers) => {
      headers['Authorization'] = 'Token testuser testtoken';
      return headers;
    },
  },
  cipher: {
    encrypt: (text) => `encrypted_${text}`,
    decrypt: (text) => text.replace('encrypted_', ''),
  },
};

// Mock response for testing
const mockResponse = {
  status: 200,
  statusText: 'OK',
  headers: {
    get: (name) => (name === 'content-type' ? 'application/json' : null),
  },
  text: () => Promise.resolve('{"test": "value"}'),
};

describe('BaseTransport', () => {
  test('should initialize with options', () => {
    const transport = new BaseTransport({
      client: mockClient,
      verifyCert: true,
      optionsCallback: jest.fn(),
      requestCallback: jest.fn(),
      responseCallback: jest.fn(),
    });

    expect(transport.client).toBe(mockClient);
    expect(transport.verifyCert).toBe(true);
    expect(transport.optionsCallback).toBeDefined();
    expect(transport.requestCallback).toBeDefined();
    expect(transport.responseCallback).toBeDefined();
  });

  test('should throw error for unimplemented handleRequest', async () => {
    const transport = new BaseTransport();
    await expect(
      transport.handleRequest('GET', 'http://test.com', '/', {}, {}, [])
    ).rejects.toThrow('Method handleRequest(...) must be overridden in all subclasses');
  });

  test('_getDecoder should throw error for unsupported media type', () => {
    const transport = new BaseTransport();

    class MockCodec {
      constructor() {
        this.mediaTypes = ['application/json'];
      }
    }

    expect(() => {
      transport._getDecoder('text/html', [new MockCodec()]);
    }).toThrow(ClientError);
  });

  test('_sleep should return a promise', () => {
    const transport = new BaseTransport();
    const promise = transport._sleep(1);
    expect(promise).toBeInstanceOf(Promise);
  });
});

describe('CommandHTTPTransport', () => {
  test('should initialize with message callback', () => {
    const callback = jest.fn();
    const transport = new CommandHTTPTransport({
      messageCallback: callback,
    });

    expect(transport._messageCallback).toBe(callback);
  });
});

describe('DataHTTPTransport', () => {
  test('should initialize', () => {
    const transport = new DataHTTPTransport();
    expect(transport).toBeInstanceOf(BaseTransport);
  });
});
