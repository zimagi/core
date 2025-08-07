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
   * Decode a byte string
   * @param {string} bytestring - Byte string to decode
   * @param {Object} options - Decoding options
   * @returns {*} Decoded data
   */
  decode(bytestring: string, options: any = {}): any {
    throw new Error('Method decode(...) must be implemented in subclasses');
  }
}
