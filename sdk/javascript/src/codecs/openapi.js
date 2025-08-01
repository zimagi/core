/**
 * OpenAPI JSON codec for the Zimagi JavaScript SDK
 */

import { BaseCodec } from './base.js';
import { ParseError } from '../exceptions.js';

/**
 * OpenAPI JSON codec implementation
 */
export class OpenAPIJSONCodec extends BaseCodec {
  /**
   * Create a new OpenAPI JSON codec
   */
  constructor() {
    super();
    this.mediaTypes = ['application/openapi+json', 'application/vnd.oai.openapi+json'];
  }

  /**
   * Decode a byte string as OpenAPI JSON
   * @param {string} bytestring - Byte string to decode
   * @param {Object} options - Decoding options
   * @returns {*} Decoded data
   */
  decode(bytestring, options = {}) {
    try {
      const data = JSON.parse(bytestring.toString());
      return data;
    } catch (error) {
      throw new ParseError(`Malformed JSON: ${error.message}`);
    }
  }
}
