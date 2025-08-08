/**
 * JSON codec for the Zimagi JavaScript SDK
 */

import { BaseCodec } from './base';
import { ParseError } from '../exceptions';

export class JSONCodec extends BaseCodec {
  mediaTypes: string[];

  constructor() {
    super();
    this.mediaTypes = ['application/json'];
  }

  encode(data: any, _options: any = {}): string {
    try {
      return JSON.stringify(data);
    } catch (error: any) {
      if (typeof jest !== 'undefined' && !jest) {
        this.debug(`JSON encoding failed: ${error.message}`);
      }
      throw new ParseError(`JSON encoding error: ${error.message}`);
    }
  }

  decode(bytestring: string | Buffer, _options: any = {}): any {
    try {
      // Handle empty responses
      if (!bytestring || (typeof bytestring === 'string' && bytestring.length === 0)) {
        return {};
      }

      const data = JSON.parse(bytestring.toString());
      return data;
    } catch (error: any) {
      // Only log if we're still in a test context and not after tests are done
      if (typeof jest !== 'undefined' && !jest) {
        this.debug(`JSON parsing failed: ${error.message}`);
      }
      throw new ParseError(`Malformed JSON: ${error.message}`);
    }
  }
}
