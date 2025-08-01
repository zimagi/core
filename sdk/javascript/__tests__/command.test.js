/**
 * Tests for command response functionality
 */

import { CommandResponse } from '../src/command/response.js';
import { StatusMessage, DataMessage, ErrorMessage } from '../src/messages/index.js';

describe('CommandResponse', () => {
  test('should initialize with default values', () => {
    const response = new CommandResponse();

    expect(response.aborted).toBe(true);
    expect(response.messages).toEqual([]);
    expect(response.named).toEqual({});
    expect(response.errors).toEqual([]);
  });

  test('should add status messages', () => {
    const response = new CommandResponse();
    const message = new StatusMessage(true);

    response.add(message);

    expect(response.aborted).toBe(false);
    expect(response.messages).toEqual([]);
  });

  test('should add data messages', () => {
    const response = new CommandResponse();
    const message = new DataMessage({
      name: 'test_data',
      message: 'Test data',
      data: { key: 'value' },
    });

    response.add(message);

    expect(response.messages).toEqual([message]);
    expect(response.named.test_data).toBe(message);
  });

  test('should add error messages', () => {
    const response = new CommandResponse();
    const message = new ErrorMessage({
      message: 'Test error',
    });

    response.add(message);

    expect(response.messages).toEqual([message]);
    expect(response.errors).toEqual([message]);
    expect(response.error).toBe(true);
  });

  test('should get named data', () => {
    const response = new CommandResponse();
    const message = new DataMessage({
      name: 'test_data',
      message: 'Test data',
      data: { key: 'value' },
    });

    response.add(message);

    expect(response.getNamedData('test_data')).toEqual({ key: 'value' });
    expect(response.getNamedData('nonexistent')).toBeNull();
  });

  test('should get active user and log key', () => {
    const response = new CommandResponse();

    const userMessage = new DataMessage({
      name: 'active_user',
      message: 'Active user',
      data: { username: 'testuser' },
    });

    const logMessage = new DataMessage({
      name: 'log_key',
      message: 'Log key',
      data: 'test-log-key',
    });

    response.add([userMessage, logMessage]);

    expect(response.activeUser).toEqual({ username: 'testuser' });
    expect(response.logKey).toBe('test-log-key');
  });

  test('should generate error message', () => {
    const response = new CommandResponse();

    const error1 = new ErrorMessage({
      message: 'Error 1',
    });

    const error2 = new ErrorMessage({
      message: 'Error 2',
    });

    response.add([error1, error2]);

    expect(response.errorMessage()).toBe('** Error 1\n\n** Error 2');
  });

  test('should be iterable', () => {
    const response = new CommandResponse();

    const message1 = new DataMessage({
      message: 'Message 1',
      data: 'data1',
    });

    const message2 = new DataMessage({
      message: 'Message 2',
      data: 'data2',
    });

    response.add([message1, message2]);

    const messages = [...response];
    expect(messages).toEqual([message1, message2]);
  });
});
