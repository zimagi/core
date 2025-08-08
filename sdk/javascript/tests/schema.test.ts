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

    expect(root.url).toBe('http://localhost');
    expect(root.title).toBe('Test Root');
    expect(root.description).toBe('Test description');
    expect(root.mediaType).toBe('application/vnd.zimagi+json');
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

    expect(router.name).toBe('Test Router');
    expect(router.overview).toBe('Test overview');
    expect(router.description).toBe('Test description');
    expect(router.epilog).toBe('Test epilog');
    expect(router.priority).toBe(5);
    expect(router.resource).toBe('test');
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

    expect(action.url).toBe('http://localhost/action');
    expect(action.name).toBe('Test Action');
    expect(action.overview).toBe('Test overview');
    expect(action.description).toBe('Test description');
    expect(action.epilog).toBe('Test epilog');
    expect(action.priority).toBe(3);
    expect(action.resource).toBe('test');
    expect(action.confirm).toBe(true);
    expect(action.fields).toEqual([]);
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

    expect(field.method).toBe('GET');
    expect(field.name).toBe('test_field');
    expect(field.type).toBe('string');
    expect(field.argument).toBe('test');
    expect(field.config).toBe('config');
    expect(field.description).toBe('Test description');
    expect(field.valueLabel).toBe('Test Label');
    expect(field.required).toBe(true);
    expect(field.system).toBe(false);
    expect(field.default).toBe('default_value');
    expect(field.choices).toEqual(['choice1', 'choice2']);
    expect(field.tags).toEqual(['tag1', 'tag2']);
  });

  test('Error should initialize with options', () => {
    const error = new Error({
      title: 'Test Error',
      content: {
        message: 'Error message',
      },
    });

    expect(error.title).toBe('Test Error');
    expect(error.get('message')).toBe('Error message');
  });

  test('Object should initialize with items', () => {
    const obj = new SchemaObject({
      key1: 'value1',
      key2: 'value2',
    });

    expect(obj.get('key1')).toBe('value1');
    expect(obj.get('key2')).toBe('value2');
  });

  test('Array should initialize with items', () => {
    const arr = new SchemaArray([1, 2, 3]);

    expect(arr[0]).toBe(1);
    expect(arr[1]).toBe(2);
    expect(arr[2]).toBe(3);
    expect(arr.length).toBe(3);
  });
});
