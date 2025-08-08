/**
 * Tests for transport layer implementations
 */

import { jest } from '@jest/globals';
import { BaseTransport } from '../src/transports/base';
import { CommandHTTPTransport } from '../src/transports/command';
import { DataHTTPTransport } from '../src/transports/data';
import { ClientError } from '../src/exceptions';

// Mock client for testing
const mockClient: any = {
  auth: {
    apply: (headers: any) => {
      headers['Authorization'] = 'Token testuser testtoken';
      return headers;
    },
  },
  cipher: {
    encrypt: (text: string) => `encrypted_${text}`,
    decrypt: (text: string) => text.replace('encrypted_', ''),
  },
};

describe('BaseTransport', () => {
  test('should initialize with options', () => {
    const mockFn = jest.fn();
    const transport = new BaseTransport({
      client: mockClient,
      verifyCert: true,
      optionsCallback: mockFn,
      requestCallback: mockFn,
      responseCallback: mockFn,
    });

    expect((transport as any).client).toBe(mockClient);
    expect((transport as any).verifyCert).toBe(true);
    expect((transport as any).optionsCallback).toBeDefined();
    expect((transport as any).requestCallback).toBeDefined();
    expect((transport as any).responseCallback).toBeDefined();
  });

  test('should throw error for unimplemented handleRequest', () => {
    const transport = new BaseTransport();
    expect(
      (transport as any).handleRequest('GET', 'http://localhost', '/', {}, {}, [])
    ).rejects.toThrow('Method handleRequest(...) must be overridden in all subclasses');
  });

  test('_getDecoder should throw error for unsupported media type', () => {
    const transport = new BaseTransport();

    class MockCodec {
      mediaTypes: string[];
      constructor() {
        this.mediaTypes = ['application/json'];
      }
    }

    expect(() => {
      (transport as any)._getDecoder('text/html', [new MockCodec()]);
    }).toThrow(ClientError);
  });

  test('_sleep should return a promise', () => {
    const transport = new BaseTransport();
    const promise = (transport as any)._sleep(1);
    expect(promise).toBeInstanceOf(Promise);
  });
});

describe('CommandHTTPTransport', () => {
  test('should initialize with message callback', () => {
    const callback = jest.fn();
    const transport = new CommandHTTPTransport({
      messageCallback: callback,
    });

    expect((transport as any)._messageCallback).toBe(callback);
  });
});

describe('DataHTTPTransport', () => {
  test('should initialize', () => {
    const transport = new DataHTTPTransport();
    expect(transport).toBeInstanceOf(BaseTransport);
  });
});
