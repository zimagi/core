/**
 * Command response handler for the Zimagi JavaScript SDK
 */

/**
 * Command response class
 */
export class CommandResponse {
  /**
   * Create a new command response
   */
  constructor() {
    this.aborted = true;
    this.messages = [];
    this.named = {};
    this.errors = [];
  }

  /**
   * Get iterator for messages
   * @returns {Iterator} Message iterator
   */
  *[Symbol.iterator]() {
    yield* this.messages;
  }

  /**
   * Get active user from named data
   * @returns {*} Active user data
   */
  get activeUser() {
    return this.getNamedData('active_user');
  }

  /**
   * Get log key from named data
   * @returns {*} Log key data
   */
  get logKey() {
    return this.getNamedData('log_key');
  }

  /**
   * Add messages to response
   * @param {Array|Object} messages - Messages to add
   */
  add(messages) {
    if (!Array.isArray(messages)) {
      messages = [messages];
    }

    for (const message of messages) {
      if (message.type === 'StatusMessage') {
        this.aborted = !message.message;
      } else {
        this.messages.push(message);
        if (message.name) {
          this.named[message.name] = message;
        }
        if (message.isError && message.isError()) {
          this.errors.push(message);
        }
      }
    }
  }

  /**
   * Check if response has errors
   * @returns {boolean} Whether response has errors
   */
  get error() {
    return this.aborted;
  }

  /**
   * Get error message
   * @returns {string} Error message
   */
  errorMessage() {
    return this.errors.map((message) => message.format()).join('\n\n');
  }

  /**
   * Get named data
   * @param {string} name - Name of data to retrieve
   * @returns {*} Named data
   */
  getNamedData(name) {
    const message = this.named[name];
    if (message) {
      try {
        return message.data;
      } catch (error) {
        return message.message;
      }
    }
    return null;
  }
}
