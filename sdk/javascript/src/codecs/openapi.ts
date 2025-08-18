/**
 * OpenAPI JSON codec for the Zimagi JavaScript SDK
 */

import { BaseCodec } from './base';
import { ParseError } from '../exceptions';

export class OpenAPIJSONCodec extends BaseCodec {
  mediaTypes: string[];

  constructor() {
    super();
    this.mediaTypes = ['application/openapi+json', 'application/vnd.oai.openapi+json'];
  }

  encode(data: any, _options: any): string {
    try {
      return JSON.stringify(data);
    } catch (error: any) {
      if (typeof jest !== 'undefined' && !jest) {
        this.debug(`OpenAPI JSON encoding failed: ${error.message}`);
      }
      throw new ParseError(`OpenAPI JSON encoding error: ${error.message}`);
    }
  }

  decode(bytestring: string | Buffer, _options: any): any {
    try {
      // Handle empty responses
      if (!bytestring || (typeof bytestring === 'string' && bytestring.length === 0)) {
        return {};
      }

      let jsonString: string;
      if (bytestring instanceof Buffer) {
        jsonString = bytestring.toString();
      } else {
        jsonString = bytestring as string;
      }
      return JSON.parse(jsonString);
    } catch (error: any) {
      // Only log if we're still in a test context and not after tests are done
      if (typeof jest !== 'undefined' && !jest) {
        this.debug(`OpenAPI JSON parsing failed: ${error.message}`);
      }
      throw new ParseError(`Malformed JSON: ${error.message}`);
    }
  }
}
