/**
 * JSON codec for the Zimagi JavaScript SDK
 */

import { BaseCodec } from './base.js';
import { ParseError } from '../exceptions.js';

/**
 * JSON codec implementation
 */
export class JSONCodec extends BaseCodec {
  /**
   * Create a new JSON codec
   */
  constructor() {
    super();
    this.mediaTypes = ['application/json'];
  }

  /**
   * Decode a byte string as JSON
   * @param {string} bytestring - Byte string to decode
   * @param {Object} options - Decoding options
   * @returns {*} Decoded data
   */
  decode(bytestring, options = {}) {
    try {
      // Handle empty responses
      if (!bytestring || bytestring.length === 0) {
        return {};
      }

      const data = JSON.parse(bytestring.toString());
      return data;
    } catch (error) {
      // Only log if we're still in a test context and not after tests are done
      if (typeof jest !== 'undefined' && !jest) {
        console.debug(`[Zimagi SDK] JSON parsing failed: ${error.message}`);
      }
      throw new ParseError(`Malformed JSON: ${error.message}`);
    }
  }
}
