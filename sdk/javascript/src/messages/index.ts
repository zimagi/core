/**
 * Message system for the Zimagi JavaScript SDK
 */

import { normalizeValue } from '../utility';

/**
 * Base message class
 */
export class Message {
  type: string;
  name: string | null;
  prefix: string;
  message: string;
  silent: boolean;
  system: boolean;

  /**
   * Create a new message
   * @param {Object} options - Message options
   */
  constructor(
    options: {
      name?: string | null;
      prefix?: string;
      message?: string;
      silent?: boolean;
      system?: boolean;
    } = {}
  ) {
    this.type = this.constructor.name;
    this.name = options.name || null;
    this.prefix = options.prefix || '';
    this.message = options.message || '';
    this.silent = !!options.silent;
    this.system = !!options.system;
  }

  /**
   * Load message data
   * @param {Object} data - Message data
   */
  load(data: any): void {
    for (const [field, value] of Object.entries(data)) {
      if (field !== 'type') {
        (this as any)[field] = value;
      }
    }
  }

  /**
   * Check if message is an error
   * @returns {boolean} Whether message is an error
   */
  isError(): boolean {
    return false;
  }

  /**
   * Render message data
   * @returns {Object} Rendered message data
   */
  render(): any {
    const data: any = {
      type: this.type,
      message: this.message,
    };

    if (this.name) {
      data.name = this.name;
    }

    if (this.prefix) {
      data.prefix = this.prefix;
    }

    if (this.silent) {
      data.silent = this.silent;
    }

    if (this.system) {
      data.system = this.system;
    }

    return data;
  }

  /**
   * Convert to JSON
   * @returns {string} JSON representation
   */
  toJSON(): string {
    return JSON.stringify(this.render());
  }

  /**
   * Format message
   * @param {Object} options - Formatting options
   * @returns {string} Formatted message
   */
  format(options: any = {}): string {
    return `${this.prefix}${this.message}`;
  }

  /**
   * Display message
   * @param {Object} options - Display options
   */
  display(options: any = {}): void {
    if (!this.silent) {
      console.log(this.format());
    }
  }

  /**
   * Get message instance from data
   * @param {Object} data - Message data
   * @param {Object} cipher - Cipher for decryption
   * @returns {Message} Message instance
   */
  static get(data: any, cipher: any = null): Message {
    let message = data;
    if (cipher) {
      message = cipher.decrypt(data.package, false);
    }

    const messageData = typeof message === 'string' ? JSON.parse(message) : data.package;

    // Map type to class
    const messageTypes: any = {
      StatusMessage: StatusMessage,
      DataMessage: DataMessage,
      InfoMessage: InfoMessage,
      NoticeMessage: NoticeMessage,
      SuccessMessage: SuccessMessage,
      WarningMessage: WarningMessage,
      ErrorMessage: ErrorMessage,
      TableMessage: TableMessage,
      ImageMessage: ImageMessage,
    };

    const MsgClass = messageTypes[messageData.type] || Message;
    const msg = new MsgClass();
    msg.load(messageData);
    return msg;
  }
}

/**
 * Status message class
 */
export class StatusMessage extends Message {
  /**
   * Create a new status message
   * @param {boolean} success - Success status
   */
  constructor(success: boolean = true) {
    super({ message: success as any });
  }

  /**
   * Format message
   * @param {Object} options - Formatting options
   * @returns {string} Formatted message
   */
  format(options: any = {}): string {
    return `Success: ${this.message}`;
  }

  /**
   * Display message
   * @param {Object} options - Display options
   */
  display(options: any = {}): void {
    // No display for status messages
  }
}

/**
 * Data message class
 */
export class DataMessage extends Message {
  data: any;

  /**
   * Create a new data message
   * @param {Object} options - Message options
   */
  constructor(
    options: {
      name?: string | null;
      prefix?: string;
      message?: string;
      silent?: boolean;
      system?: boolean;
      data?: any;
    } = {}
  ) {
    super(options);
    this.data = options.data;
  }

  /**
   * Load message data
   * @param {Object} data - Message data
   */
  load(data: any): void {
    super.load(data);
    // Normalize the data value
    this.data = normalizeValue(data.data, true, true);
  }

  /**
   * Render message data
   * @returns {Object} Rendered message data
   */
  render(): any {
    const result: any = super.render();
    result.data = this.data;
    return result;
  }

  /**
   * Format message
   * @param {Object} options - Formatting options
   * @returns {string} Formatted message
   */
  format(options: any = {}): string {
    let data = this.data;

    if (typeof this.data === 'object' && this.data !== null) {
      data = `\n${JSON.stringify(this.data, null, 2)}`;
    }

    return `${this.message}: ${data}`;
  }
}

/**
 * Info message class
 */
export class InfoMessage extends Message {
  // Inherits from Message
}

/**
 * Notice message class
 */
export class NoticeMessage extends Message {
  // Inherits from Message
}

/**
 * Success message class
 */
export class SuccessMessage extends Message {
  // Inherits from Message
}

/**
 * Warning message class
 */
export class WarningMessage extends Message {
  /**
   * Display message
   * @param {Object} options - Display options
   */
  display(options: any = {}): void {
    if (!this.silent) {
      console.warn(this.format());
    }
  }
}

/**
 * Error message class
 */
export class ErrorMessage extends Message {
  traceback: string | string[] | null;

  /**
   * Create a new error message
   * @param {Object} options - Message options
   */
  constructor(
    options: {
      message?: string;
      name?: string | null;
      prefix?: string;
      silent?: boolean;
      system?: boolean;
      traceback?: string | string[];
    } = {}
  ) {
    super(options);
    this.traceback = options.traceback || null;
  }

  /**
   * Check if message is an error
   * @returns {boolean} Whether message is an error
   */
  isError(): boolean {
    return true;
  }

  /**
   * Render message data
   * @returns {Object} Rendered message data
   */
  render(): any {
    const result: any = super.render();
    result.traceback = this.traceback;
    return result;
  }

  /**
   * Format message
   * @param {Object} options - Formatting options
   * @returns {string} Formatted message
   */
  format(options: any = {}): string {
    if (this.traceback) {
      const traceback = Array.isArray(this.traceback)
        ? this.traceback.map((item) => item.trim()).join('\n')
        : this.traceback;
      return `\n${this.prefix}** ${this.message}\n\n> ${traceback}\n`;
    }

    return `${this.prefix}** ${this.message}`;
  }

  /**
   * Display message
   * @param {Object} options - Display options
   */
  display(options: any = {}): void {
    if (!this.silent && this.message) {
      console.error(this.format());
    }
  }
}

/**
 * Table message class
 */
export class TableMessage extends Message {
  rowLabels: boolean;

  /**
   * Create a new table message
   * @param {Object} options - Message options
   */
  constructor(
    options: {
      name?: string | null;
      prefix?: string;
      message?: string;
      silent?: boolean;
      system?: boolean;
      rowLabels?: boolean;
    } = {}
  ) {
    super(options);
    this.rowLabels = !!options.rowLabels;
  }

  /**
   * Load message data
   * @param {Object} data - Message data
   */
  load(data: any): void {
    super.load(data);
    // Normalize the message value
    this.message = normalizeValue(data.message, true, true);
  }

  /**
   * Render message data
   * @returns {Object} Rendered message data
   */
  render(): any {
    const result: any = super.render();
    result.rowLabels = this.rowLabels;
    return result;
  }

  /**
   * Format message
   * @param {Object} options - Formatting options
   * @returns {string} Formatted message
   */
  format(options: any = {}): string {
    // Format data as a table
    return `${this.prefix}${JSON.stringify(this.message, null, 2)}`;
  }
}

/**
 * Image message class
 */
export class ImageMessage extends Message {
  data: any;
  mimetype: string | null;

  /**
   * Create a new image message
   * @param {string} location - Image location
   * @param {Object} options - Message options
   */
  constructor(
    location: string,
    options: {
      name?: string | null;
      prefix?: string;
      silent?: boolean;
      system?: boolean;
    } = {}
  ) {
    super({ message: location, ...options, silent: true, system: options.system || false });
    this.data = null;
    this.mimetype = null;
  }

  /**
   * Load message data
   * @param {Object} data - Message data
   */
  load(data: any): void {
    super.load(data);
    // In a real implementation, this would load and encode image data
    this.data = null;
    this.mimetype = null;
  }

  /**
   * Render message data
   * @returns {Object} Rendered message data
   */
  render(): any {
    const result: any = super.render();
    result.data = this.data;
    result.mimetype = this.mimetype;
    return result;
  }
}
