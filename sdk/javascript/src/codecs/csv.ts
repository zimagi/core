/**
 * CSV codec for the Zimagi JavaScript SDK
 */

import Papa from 'papaparse';
import { BaseCodec } from './base';
import { ParseError } from '../exceptions';
import { normalizeValue } from '../utility';

export class CSVCodec extends BaseCodec {
  mediaTypes: string[];

  constructor() {
    super();
    this.mediaTypes = ['text/csv'];
  }

  /**
   * Normalize a CSV value
   * @param {*} value - Value to normalize
   * @returns {*} Normalized value
   */
  _normalizeValue(value: any): any {
    return normalizeValue(value, true, false);
  }

  /**
   * Decode CSV data
   * @param {string | Buffer} bytestring - CSV data to decode
   * @param {Object} _options - Decoding options
   * @returns {*} Decoded data
   */
  decode(bytestring: string | Buffer, _options: any = {}): any {
    try {
      let csvString: string;
      if (Buffer.isBuffer(bytestring)) {
        csvString = bytestring.toString();
      } else {
        csvString = bytestring as string;
      }

      const parsed = Papa.parse(csvString, {
        header: true,
        skipEmptyLines: true,
      });

      // Convert parsed data to our expected format
      const results = parsed.data.map((row: any) => {
        const normalizedRow: any = {};
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
    } catch (error: any) {
      // Only log if we're still in a test context and not after tests are done
      if (typeof jest !== 'undefined' && !jest) {
        console.debug(`[Zimagi SDK] CSV parsing failed: ${error.message}`);
      }
      throw new ParseError(`Malformed CSV: ${error.message}`);
    }
  }
}
