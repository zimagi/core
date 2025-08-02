/**
 * CSV codec for the Zimagi JavaScript SDK
 */

import Papa from 'papaparse';
import { BaseCodec } from './base.js';
import { ParseError } from '../exceptions.js';
import { normalizeValue } from '../utility.js';

/**
 * CSV codec implementation
 */
export class CSVCodec extends BaseCodec {
  /**
   * Create a new CSV codec
   */
  constructor() {
    super();
    this.mediaTypes = ['text/csv'];
  }

  /**
   * Decode a byte string as CSV
   * @param {string} bytestring - Byte string to decode
   * @param {Object} options - Decoding options
   * @returns {*} Decoded data
   */
  decode(bytestring, options = {}) {
    try {
      const csvString = bytestring.toString();
      const parsed = Papa.parse(csvString, {
        header: true,
        skipEmptyLines: true,
      });

      // Convert parsed data to our expected format
      const results = parsed.data.map((row) => {
        const normalizedRow = {};
        for (const [key, value] of Object.entries(row)) {
          normalizedRow[key] = this._normalizeValue(value);
        }
        return normalizedRow;
      });

      return {
        headers: parsed.meta.fields || [],
        rows: parsed.data,
        count: results.length,
        results: results,
      };
    } catch (error) {
      // Only log if we're still in a test context and not after tests are done
      if (typeof jest !== 'undefined' && !jest) {
        console.debug(`[Zimagi SDK] CSV parsing failed: ${error.message}`);
      }
      throw new ParseError(`Malformed CSV: ${error.message}`);
    }
  }

  /**
   * Normalize a CSV value
   * @param {*} value - Value to normalize
   * @returns {*} Normalized value
   */
  _normalizeValue(value) {
    return normalizeValue(value, true, false);
  }
}
