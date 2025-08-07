/**
 * Tests for schema implementations
 */

import { Root, Router, Action, Field, Error, SchemaObject, SchemaArray } from '../src/schema/index';

describe('Schema Classes', () => {
  test('Root should initialize with options', () => {
    const root = new Root({
      url: 'http://localhost',
      title: 'Test Root',
      description: 'Test description',
    });

    expect((root as any).url).toBe('http://localhost');
    expect((root as any).title).toBe('Test Root');
    expect((root as any).description).toBe('Test description');
    expect((root as any).mediaType).toBe('application/vnd.zimagi+json');
  });

  test('Router should initialize with options', () => {
    const router = new Router({
      name: 'Test Router',
      overview: 'Test overview',
      description: 'Test description',
      epilog: 'Test epilog',
      priority: 5,
      resource: 'test',
    });

    expect((router as any).name).toBe('Test Router');
    expect((router as any).overview).toBe('Test overview');
    expect((router as any).description).toBe('Test description');
    expect((router as any).epilog).toBe('Test epilog');
    expect((router as any).priority).toBe(5);
    expect((router as any).resource).toBe('test');
  });

  test('Action should initialize with options', () => {
    const action = new Action({
      url: 'http://localhost/action',
      name: 'Test Action',
      overview: 'Test overview',
      description: 'Test description',
      epilog: 'Test epilog',
      priority: 3,
      resource: 'test',
      confirm: true,
      fields: [],
    });

    expect((action as any).url).toBe('http://localhost/action');
    expect((action as any).name).toBe('Test Action');
    expect((action as any).overview).toBe('Test overview');
    expect((action as any).description).toBe('Test description');
    expect((action as any).epilog).toBe('Test epilog');
    expect((action as any).priority).toBe(3);
    expect((action as any).resource).toBe('test');
    expect((action as any).confirm).toBe(true);
    expect((action as any).fields).toEqual([]);
  });

  test('Field should initialize with options', () => {
    const field = new Field({
      method: 'GET',
      name: 'test_field',
      type: 'string',
      argument: 'test',
      config: 'config',
      description: 'Test description',
      valueLabel: 'Test Label',
      required: true,
      system: false,
      default: 'default_value',
      choices: ['choice1', 'choice2'],
      tags: ['tag1', 'tag2'],
    });

    expect((field as any).method).toBe('GET');
    expect((field as any).name).toBe('test_field');
    expect((field as any).type).toBe('string');
    expect((field as any).argument).toBe('test');
    expect((field as any).config).toBe('config');
    expect((field as any).description).toBe('Test description');
    expect((field as any).valueLabel).toBe('Test Label');
    expect((field as any).required).toBe(true);
    expect((field as any).system).toBe(false);
    expect((field as any).default).toBe('default_value');
    expect((field as any).choices).toEqual(['choice1', 'choice2']);
    expect((field as any).tags).toEqual(['tag1', 'tag2']);
  });

  test('Error should initialize with options', () => {
    const error = new Error({
      title: 'Test Error',
      content: {
        message: 'Error message',
      },
    });

    expect((error as any).title).toBe('Test Error');
    expect((error as any).get('message')).toBe('Error message');
  });

  test('Object should initialize with items', () => {
    const obj = new SchemaObject({
      key1: 'value1',
      key2: 'value2',
    });

    expect((obj as any).get('key1')).toBe('value1');
    expect((obj as any).get('key2')).toBe('value2');
  });

  test('Array should initialize with items', () => {
    const arr = new SchemaArray([1, 2, 3]);

    expect(arr[0]).toBe(1);
    expect(arr[1]).toBe(2);
    expect(arr[2]).toBe(3);
    expect(arr.length).toBe(3);
  });
});
