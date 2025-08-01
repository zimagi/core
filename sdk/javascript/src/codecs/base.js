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
  constructor() {
    this.mediaTypes = [];
  }

  /**
   * Decode a byte string
   * @param {string} bytestring - Byte string to decode
   * @param {Object} options - Decoding options
   * @returns {*} Decoded data
   */
  decode(bytestring, options = {}) {
    throw new Error('Method decode(...) must be implemented in subclasses');
  }
}
