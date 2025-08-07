/**
 * Command client for the Zimagi JavaScript SDK
 */

import { BaseAPIClient } from './base';
import { CommandHTTPTransport } from '../transports/command';
import { ZimagiJSONCodec, JSONCodec } from '../codecs/index';
import { ParseError } from '../exceptions';

/**
 * Command client class
 */
export class CommandClient extends BaseAPIClient {
  optionsCallback: Function | null;
  messageCallback: Function | null;
  initCommands: boolean;
  schema: any;
  commands: any;
  actions: any;

  /**
   * Create a new command client
   * @param {Object} options - Client options
   */
  constructor(options: any = {}) {
    super({
      port: options.port || 5123,
      verifyCert: options.verifyCert !== undefined ? options.verifyCert : false,
      decoders: [new ZimagiJSONCodec(), new JSONCodec()],
      ...options,
    });

    this.optionsCallback = options.optionsCallback || null;
    this.messageCallback = options.messageCallback || null;
    this.initCommands = options.initCommands !== false;

    this.transport = new CommandHTTPTransport({
      client: this,
      verifyCert: this.verifyCert,
      optionsCallback: this.optionsCallback,
      messageCallback: this.messageCallback,
    });

    if (!this.getStatus().encryption) {
      this.cipher = null;
    }

    this.schema = this.getSchema();
    if (this.initCommands) {
      this._initCommands();
    }
  }

  /**
   * Clone client with new message callback
   * @param {Function} messageCallback - New message callback
   * @returns {CommandClient} Cloned client
   */
  clone(messageCallback: Function): CommandClient {
    // Create new client with same options but different message callback
    const cloneOptions: any = {
      host: this.host,
      port: this.port,
      user: this.user,
      token: this.token,
      encryptionKey: this.encryptionKey,
      protocol: this.protocol,
      verifyCert: this.verifyCert,
      optionsCallback: this.optionsCallback,
      messageCallback: messageCallback,
      initCommands: this.initCommands,
    };

    return new CommandClient(cloneOptions);
  }

  /**
   * Initialize commands from schema
   */
  _initCommands(): void {
    this.commands = {};
    this.actions = {};

    const collectCommands = (commandInfo: any, parents: string[]) => {
      for (const [commandName, info] of Object.entries(commandInfo)) {
        const apiPath = [...parents, commandName].join('/');
        // In a full implementation, we would check if info is an Action or Router
        this.commands[apiPath] = info;
        // For now, we'll assume all are actions for testing
        this.actions[apiPath] = info;
      }
    };

    collectCommands(this.schema, []);
  }

  /**
   * Normalize command path
   * @param {string} commandName - Command name
   * @returns {string} Normalized path
   */
  _normalizePath(commandName: string): string {
    return commandName.replace(/(\s+|\.)/g, '/');
  }

  /**
   * Set message callback
   * @param {Function} messageCallback - Message callback
   */
  setMessageCallback(messageCallback: Function): void {
    this.messageCallback = messageCallback;
    this.transport = new CommandHTTPTransport({
      client: this,
      verifyCert: this.verifyCert,
      optionsCallback: this.optionsCallback,
      messageCallback: messageCallback,
    });
  }

  /**
   * Execute a command
   * @param {string} commandName - Command name
   * @param {Object} options - Command options
   * @returns {*} Command response
   */
  execute(commandName: string, options: any = {}): any {
    const commandPath = this._normalizePath(commandName);
    const command = this._lookup(commandPath);
    const commandOptions = this._formatOptions('POST', options);

    const validate = (url: string, params: any) => {
      this._validate(command, params);
    };

    const processor = () => {
      return this._request('POST', command.url, commandOptions, validate);
    };

    return this._wrapAPICall('command', commandPath, processor, commandOptions);
  }

  /**
   * Extend with a remote module
   * @param {string} remote - Remote module URL
   * @param {string} reference - Module reference
   * @param {string} provider - Provider name
   * @param {Object} fields - Module fields
   * @returns {*} Command response
   */
  extend(remote: string, reference: string, provider: string | null = null, fields: any = {}): any {
    fields.reference = reference;

    const options: any = {
      remote: remote,
      moduleFields: fields,
    };

    if (provider) {
      options.moduleProviderName = provider;
    }

    return this.execute('module/add', options);
  }

  /**
   * Run a task
   * @param {string} moduleKey - Module key
   * @param {string} taskName - Task name
   * @param {Object} config - Task configuration
   * @param {Object} options - Additional options
   * @returns {*} Command response
   */
  runTask(moduleKey: string, taskName: string, config: any | null = null, options: any = {}): any {
    return this.execute('task', {
      ...options,
      moduleKey: moduleKey,
      taskKey: taskName,
      taskFields: config || {},
    });
  }

  /**
   * Run a profile
   * @param {string} moduleKey - Module key
   * @param {string} profileKey - Profile key
   * @param {Object} config - Profile configuration
   * @param {Array} components - Profile components
   * @param {Object} options - Additional options
   * @returns {*} Command response
   */
  runProfile(
    moduleKey: string,
    profileKey: string,
    config: any | null = null,
    components: any[] | null = null,
    options: any = {}
  ): any {
    return this.execute('run', {
      ...options,
      moduleKey: moduleKey,
      profileKey: profileKey,
      profileConfigFields: config || {},
      profileComponents: components || [],
    });
  }

  /**
   * Destroy a profile
   * @param {string} moduleKey - Module key
   * @param {string} profileKey - Profile key
   * @param {Object} config - Profile configuration
   * @param {Array} components - Profile components
   * @param {Object} options - Additional options
   * @returns {*} Command response
   */
  destroyProfile(
    moduleKey: string,
    profileKey: string,
    config: any | null = null,
    components: any[] | null = null,
    options: any = {}
  ): any {
    return this.execute('destroy', {
      ...options,
      moduleKey: moduleKey,
      profileKey: profileKey,
      profileConfigFields: config || {},
      profileComponents: components || [],
    });
  }

  /**
   * Run imports
   * @param {Array} names - Import names
   * @param {Array} tags - Import tags
   * @param {Object} options - Additional options
   * @returns {*} Command response
   */
  runImports(names: string[] | null = null, tags: string[] | null = null, options: any = {}): any {
    return this.execute('import', {
      ...options,
      importNames: names || [],
      tags: tags || [],
    });
  }

  /**
   * Run calculations
   * @param {Array} names - Calculation names
   * @param {Array} tags - Calculation tags
   * @param {Object} options - Additional options
   * @returns {*} Command response
   */
  runCalculations(
    names: string[] | null = null,
    tags: string[] | null = null,
    options: any = {}
  ): any {
    return this.execute('calculate', {
      ...options,
      calculationNames: names || [],
      tags: tags || [],
    });
  }

  /**
   * Lookup a command
   * @param {string} commandName - Command name
   * @returns {*} Command object
   */
  _lookup(commandName: string): any {
    // Placeholder implementation - in a full implementation this would
    // traverse the schema to find the command
    let node = this.schema;
    let found = true;

    for (const key of commandName.split('/')) {
      if (node[key] !== undefined) {
        node = node[key];
      } else {
        found = false;
        break;
      }
    }

    // For now, we'll just return a mock action object for testing
    if (!found) {
      if (!this.initCommands) {
        this._initCommands();
      }

      const relatedActions: string[] = [];
      for (const otherAction of Object.keys(this.actions)) {
        if (otherAction.includes(commandName)) {
          relatedActions.push(otherAction);
        }
      }

      throw new ParseError(
        `Command ${commandName} does not exist. Try one of: ${relatedActions.join(', ')}`
      );
    }

    // Return a mock action object
    return {
      url: `${this.baseURL}${commandName}`,
      fields: [],
    };
  }

  /**
   * Validate command options
   * @param {Object} command - Command object
   * @param {Object} options - Command options
   */
  _validate(command: any, options: any): void {
    // Placeholder implementation - in a full implementation this would
    // validate the options against the command's field definitions
    const provided = new Set(Object.keys(options));
    const required = new Set(); // Would come from command.fields
    const optional = new Set(); // Would come from command.fields
    const errors: any = {};

    const missing = [...required].filter((item) => !provided.has(item));
    for (const item of missing) {
      errors[item] = 'Parameter is required';
    }

    const unexpected = [...provided].filter((item) => !optional.has(item) && !required.has(item));
    for (const item of unexpected) {
      errors[item] = 'Unknown parameter';
    }

    if (Object.keys(errors).length > 0) {
      throw new ParseError(errors);
    }
  }

  /**
   * Format command options
   * @param {string} method - HTTP method
   * @param {Object} options - Command options
   * @returns {Object} Formatted options
   */
  _formatOptions(method: string, options: any): any {
    if (options === null) {
      options = {};
    }

    for (const [key, value] of Object.entries(options)) {
      if (typeof value === 'object' && value !== null) {
        if (Array.isArray(value) && method === 'GET') {
          (options as any)[key] = (value as any[]).join(',');
        } else {
          (options as any)[key] = JSON.stringify(value);
        }
      }
    }

    return options;
  }
}
