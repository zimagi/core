/**
 * Schema definitions for the Zimagi JavaScript SDK
 */

/**
 * Helper function for key sorting
 * @param {Array} item - Key-value pair
 * @returns {Array} Sort key
 */
function _keySorter(item: [string, any]): [number, any] {
  const [key, value] = item;
  if (value instanceof Action) {
    const actionPriority = { get: 0, post: 1 }[value.action] || 2;
    return [1, [value.url, actionPriority]];
  }
  return [0, key];
}

/**
 * Mixin for sorted items
 */
class SortedItemsMixin {
  _items: Map<string, any>;

  constructor() {
    this._items = new Map();
  }

  /**
   * Get sorted iterator
   * @returns {Iterator} Sorted iterator
   */
  *[Symbol.iterator](): Iterator<string> {
    const items = [...this._items.entries()].sort((a, b) => {
      const [sortA, sortB] = [_keySorter(a), _keySorter(b)];
      if (sortA[0] !== sortB[0]) {
        return sortA[0] - sortB[0];
      }
      // Compare the second elements of the sort keys
      if (Array.isArray(sortA[1]) && Array.isArray(sortB[1])) {
        for (let i = 0; i < Math.min(sortA[1].length, sortB[1].length); i++) {
          if (sortA[1][i] < sortB[1][i]) return -1;
          if (sortA[1][i] > sortB[1][i]) return 1;
        }
      }
      return 0;
    });
    for (const [key] of items) {
      yield key;
    }
  }
}

/**
 * Mixin for command indexing
 */
class CommandIndexMixin extends SortedItemsMixin {
  /**
   * Get data items (non-commands)
   * @returns {Object} Data items
   */
  get data(): { [key: string]: any } {
    const result: { [key: string]: any } = {};
    for (const [key, value] of this._items.entries()) {
      if (!(value instanceof Router || value instanceof Action)) {
        result[key] = value;
      }
    }
    return result;
  }

  /**
   * Get command items
   * @returns {Object} Command items
   */
  get commands(): { [key: string]: any } {
    const result: { [key: string]: any } = {};
    for (const [key, value] of this._items.entries()) {
      if (value instanceof Router || value instanceof Action) {
        result[key] = value;
      }
    }
    return result;
  }

  /**
   * Get router items
   * @returns {Object} Router items
   */
  get routers(): { [key: string]: any } {
    const result: { [key: string]: any } = {};
    for (const [key, value] of this._items.entries()) {
      if (value instanceof Router) {
        result[key] = value;
      }
    }
    return result;
  }

  /**
   * Get action items
   * @returns {Object} Action items
   */
  get actions(): { [key: string]: any } {
    const result: { [key: string]: any } = {};
    for (const [key, value] of this._items.entries()) {
      if (value instanceof Action) {
        result[key] = value;
      }
    }
    return result;
  }
}

/**
 * Root schema class
 */
export class Root extends CommandIndexMixin {
  url: string;
  title: string;
  description: string;
  mediaType: string;

  /**
   * Create a new root
   * @param {Object} options - Root options
   */
  constructor(
    options: {
      url?: string;
      title?: string;
      description?: string;
      mediaType?: string;
      commands?: { [key: string]: any };
    } = {}
  ) {
    super();
    this.url = options.url || '';
    this.title = options.title || '';
    this.description = options.description || '';
    this.mediaType = options.mediaType || 'application/vnd.zimagi+json';

    // Initialize with commands
    const commands = options.commands || {};
    for (const [key, value] of Object.entries(commands)) {
      this._items.set(key, value);
    }
  }

  /**
   * Set a key-value pair
   * @param {string} key - Key
   * @param {*} value - Value
   * @returns {Root} This instance
   */
  set(key: string, value: any): Root {
    this._items.set(key, value);
    return this;
  }

  /**
   * Get a value by key
   * @param {string} key - Key
   * @returns {*} Value
   */
  get(key: string): any {
    return this._items.get(key);
  }

  /**
   * Get all entries
   * @returns {Array} Entries
   */
  entries(): [string, any][] {
    return [...this._items.entries()];
  }
}

/**
 * Router schema class
 */
export class Router extends CommandIndexMixin {
  name: string;
  overview: string;
  description: string;
  epilog: string;
  priority: number;
  resource: string;

  /**
   * Create a new router
   * @param {Object} options - Router options
   */
  constructor(
    options: {
      name?: string;
      overview?: string;
      description?: string;
      epilog?: string;
      priority?: number;
      resource?: string;
      commands?: { [key: string]: any };
    } = {}
  ) {
    super();
    this.name = options.name || '';
    this.overview = options.overview || '';
    this.description = options.description || '';
    this.epilog = options.epilog || '';
    this.priority = options.priority !== undefined ? options.priority : 1;
    this.resource = options.resource || '';

    // Initialize with commands
    const commands = options.commands || {};
    for (const [key, value] of Object.entries(commands)) {
      this._items.set(key, value);
    }
  }

  /**
   * Set a key-value pair
   * @param {string} key - Key
   * @param {*} value - Value
   * @returns {Router} This instance
   */
  set(key: string, value: any): Router {
    this._items.set(key, value);
    return this;
  }

  /**
   * Get a value by key
   * @param {string} key - Key
   * @returns {*} Value
   */
  get(key: string): any {
    return this._items.get(key);
  }

  /**
   * Get all entries
   * @returns {Array} Entries
   */
  entries(): [string, any][] {
    return [...this._items.entries()];
  }
}

/**
 * Action schema class
 */
export class Action {
  url: string;
  name: string;
  overview: string;
  description: string;
  epilog: string;
  priority: number;
  resource: string;
  confirm: boolean;
  fields: any[];
  action: string;

  /**
   * Create a new action
   * @param {Object} options - Action options
   */
  constructor(
    options: {
      url?: string;
      name?: string;
      overview?: string;
      description?: string;
      epilog?: string;
      priority?: number;
      resource?: string;
      confirm?: boolean;
      fields?: any[];
      action?: string;
    } = {}
  ) {
    this.url = options.url || '';
    this.name = options.name || '';
    this.overview = options.overview || '';
    this.description = options.description || '';
    this.epilog = options.epilog || '';
    this.priority = options.priority !== undefined ? options.priority : 1;
    this.resource = options.resource || '';
    this.confirm = !!options.confirm;
    this.fields = Array.isArray(options.fields) ? options.fields : [];
    this.action = options.action || '';
  }
}

/**
 * Field schema class
 */
export class Field {
  method: string;
  name: string;
  type: string;
  argument: string;
  config: string;
  description: string;
  valueLabel: string;
  required: boolean;
  system: boolean;
  default: any;
  choices: any[];
  tags: string[];

  /**
   * Create a new field
   * @param {Object} options - Field options
   */
  constructor(
    options: {
      method?: string;
      name?: string;
      type?: string;
      argument?: string;
      config?: string;
      description?: string;
      valueLabel?: string;
      required?: boolean;
      system?: boolean;
      default?: any;
      choices?: any[];
      tags?: string[];
    } = {}
  ) {
    this.method = options.method || '';
    this.name = options.name || '';
    this.type = options.type || '';
    this.argument = options.argument || '';
    this.config = options.config || '';
    this.description = options.description || '';
    this.valueLabel = options.valueLabel || '';
    this.required = !!options.required;
    this.system = !!options.system;
    this.default = options.default;
    this.choices = Array.isArray(options.choices) ? options.choices : [];
    this.tags = Array.isArray(options.tags) ? options.tags : [];
  }
}

/**
 * Error schema class
 */
export class Error extends CommandIndexMixin {
  title: string;

  /**
   * Create a new error
   * @param {Object} options - Error options
   */
  constructor(
    options: {
      title?: string;
      content?: { [key: string]: any };
    } = {}
  ) {
    super();
    this.title = options.title || '';

    // Initialize with content
    const content = options.content || {};
    for (const [key, value] of Object.entries(content)) {
      this._items.set(key, value);
    }
  }

  /**
   * Set a key-value pair
   * @param {string} key - Key
   * @param {*} value - Value
   * @returns {Error} This instance
   */
  set(key: string, value: any): Error {
    this._items.set(key, value);
    return this;
  }

  /**
   * Get a value by key
   * @param {string} key - Key
   * @returns {*} Value
   */
  get(key: string): any {
    return this._items.get(key);
  }

  /**
   * Get all entries
   * @returns {Array} Entries
   */
  entries(): [string, any][] {
    return [...this._items.entries()];
  }

  /**
   * Get error messages
   * @returns {Array} Error messages
   */
  getMessages(): string[] {
    const messages: string[] = [];
    for (const [, value] of this._items.entries()) {
      if (Array.isArray(value)) {
        messages.push(...value.filter((item) => typeof item === 'string'));
      }
    }
    return messages;
  }
}

/**
 * Object schema class
 */
export class SchemaObject {
  private _items: Map<string, any>;

  /**
   * Create a new object
   * @param {Object} items - Object items
   */
  constructor(items: { [key: string]: any } = {}) {
    this._items = new Map();
    for (const [key, value] of Object.entries(items)) {
      this._items.set(key, value);
    }
  }

  /**
   * Set a key-value pair
   * @param {string} key - Key
   * @param {*} value - Value
   * @returns {SchemaObject} This instance
   */
  set(key: string, value: any): SchemaObject {
    this._items.set(key, value);
    return this;
  }

  /**
   * Get a value by key
   * @param {string} key - Key
   * @returns {*} Value
   */
  get(key: string): any {
    return this._items.get(key);
  }

  /**
   * Get all entries
   * @returns {Array} Entries
   */
  entries(): [string, any][] {
    return [...this._items.entries()];
  }
}

/**
 * Array schema class
 */
export class SchemaArray extends Array {
  /**
   * Create a new array
   * @param {Array} items - Array items
   */
  constructor(items: any[] = []) {
    // Call the parent constructor with the items
    super(...items);

    // Copy items to this array instance
    items.forEach((item, index) => {
      this[index] = item;
    });
  }
}

// Export classes with proper aliases
export { SchemaObject as Object };
export { SchemaArray as Array };
