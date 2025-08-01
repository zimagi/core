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
    const convert = (data) => {
      if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
        // Convert plain objects to a map-like structure if needed
        return data;
      } else if (Array.isArray(data)) {
        return data.map((value, index) => {
          data[index] = convert(value);
        });
      }
      return data;
    };

    try {
      const data = JSON.parse(bytestring.toString());
      return convert(data);
    } catch (error) {
      throw new ParseError(`Malformed JSON: ${error.message}`);
    }
  }
}
