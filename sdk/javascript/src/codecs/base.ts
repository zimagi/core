/**
 * Base codec class for the Zimagi JavaScript SDK
 */

/**
 * Base codec class
 */
export class BaseCodec {
  /**
   * Create a new codec
   */
  mediaTypes: string[];

  constructor() {
    this.mediaTypes = [];
  }

  /**
   * Render debug statements
   */
  debug(...args: any[]): void {
    // In test environment, be more careful about logging
    if (typeof process !== 'undefined' && process.env && process.env.NODE_ENV === 'test') {
      // During tests, minimize logging to prevent "Cannot log after tests are done" errors
      return;
    }

    // Outside of test environment, log normally
    try {
      console.debug('[Zimagi SDK Codec]: ', ...args);
    } catch (e) {
      // Silently ignore logging if context is invalid
      return;
    }
  }

  /**
   * Decode a byte string
   * @param {string} _bytestring - Byte string to decode
   * @param {Object} _options - Decoding options
   * @returns {*} Decoded data
   */
  decode(_bytestring: string, _options: any = {}): any {
    throw new Error('Method decode(...) must be implemented in subclasses');
  }
}
