/**
 * Tests for message implementations
 */

import { jest } from '@jest/globals';
import {
  Message,
  StatusMessage,
  DataMessage,
  InfoMessage,
  NoticeMessage,
  SuccessMessage,
  WarningMessage,
  ErrorMessage,
  TableMessage,
  ImageMessage,
} from '../src/messages/index';

describe('Message Classes', () => {
  test('Message should initialize with options', () => {
    const message = new Message({
      name: 'test',
      prefix: 'TEST: ',
      message: 'Test message',
      silent: true,
      system: true,
    });

    expect(message.type).toBe('Message');
    expect(message.name).toBe('test');
    expect(message.prefix).toBe('TEST: ');
    expect(message.message).toBe('Test message');
    expect(message.silent).toBe(true);
    expect(message.system).toBe(true);
  });

  test('StatusMessage should initialize with success status', () => {
    const message = new StatusMessage(true);

    expect(message.type).toBe('StatusMessage');
    expect(message.success).toBe(true);
  });

  test('DataMessage should initialize with data', () => {
    const message = new DataMessage({
      message: 'Test data',
      data: { key: 'value' },
    });

    expect(message.type).toBe('DataMessage');
    expect(message.message).toBe('Test data');
    expect((message as any).data).toEqual({ key: 'value' });
  });

  test('ErrorMessage should be identified as error', () => {
    const message = new ErrorMessage({
      message: 'Test error',
      traceback: 'Error traceback',
    });

    expect(message.isError()).toBe(true);
    expect((message as any).traceback).toBe('Error traceback');
  });

  test('WarningMessage should display to console.warn', () => {
    const message = new WarningMessage({
      message: 'Test warning',
    });

    const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation();

    message.display();

    expect(consoleWarnSpy).toHaveBeenCalledWith('Test warning');

    consoleWarnSpy.mockRestore();
  });

  test('Message rendering should include all fields', () => {
    const message = new Message({
      name: 'test',
      prefix: 'TEST: ',
      message: 'Test message',
      silent: true,
      system: true,
    });

    const rendered = message.render();

    expect(rendered).toEqual({
      type: 'Message',
      name: 'test',
      prefix: 'TEST: ',
      message: 'Test message',
      silent: true,
      system: true,
    });
  });

  test('Message formatting should work correctly', () => {
    const message = new Message({
      prefix: 'TEST: ',
      message: 'Test message',
    });

    const formatted = message.format();
    expect(formatted).toBe('TEST: Test message');
  });

  test('Message display should log to console by default', () => {
    const message = new Message({
      message: 'Test message',
    });

    const consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();

    message.display();

    expect(consoleLogSpy).toHaveBeenCalledWith('Test message');

    consoleLogSpy.mockRestore();
  });
});
