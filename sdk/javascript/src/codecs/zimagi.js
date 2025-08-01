/**
 * Zimagi JSON codec for the Zimagi JavaScript SDK
 */

import { BaseCodec } from './base.js';
import { ParseError, CommandParseError } from '../exceptions.js';
import {
  Root,
  Error as SchemaError,
  Router,
  Action,
  Field,
  Object as SchemaObject,
  Array as SchemaArray,
} from '../schema/index.js';

/**
 * Zimagi JSON codec implementation
 */
export class ZimagiJSONCodec extends BaseCodec {
  /**
   * Create a new Zimagi JSON codec
   */
  constructor() {
    super();
    this.mediaTypes = ['application/vnd.zimagi+json', 'application/x-zimagi+json'];
  }

  /**
   * Decode a byte string as Zimagi JSON
   * @param {string} bytestring - Byte string to decode
   * @param {Object} options - Decoding options
   * @returns {*} Decoded data
   */
  decode(bytestring, options = {}) {
    const baseURL = options.baseURL || '';

    try {
      const data = JSON.parse(bytestring.toString());
      const document = this._convertToSchema(data, baseURL);

      if (!(document instanceof Root || document instanceof SchemaError)) {
        throw new CommandParseError('Top level node should be a root or error.');
      }

      return document;
    } catch (error) {
      throw new ParseError(`Malformed JSON. ${error.message}`);
    }
  }

  /**
   * Convert data to schema objects
   * @param {*} data - Data to convert
   * @param {string} baseURL - Base URL for resolving relative URLs
   * @returns {*} Converted schema object
   */
  _convertToSchema(data, baseURL = '') {
    if (typeof data === 'object' && data !== null && data._type === 'root') {
      const meta = data._meta || {};
      // Resolve URL relative to baseURL
      let url = meta.url || '';
      try {
        url = new URL(url, baseURL).href;
      } catch (e) {
        // If URL resolution fails, use as-is
        url = meta.url || '';
      }

      return new Root({
        commands: this._getDocumentContent(data, baseURL),
        url: url,
        title: meta.title || '',
        description: meta.description || '',
        mediaType: 'application/vnd.zimagi+json',
      });
    }

    if (typeof data === 'object' && data !== null && data._type === 'error') {
      const meta = data._meta || {};
      return new SchemaError({
        title: meta.title || '',
        content: this._getDocumentContent(data, baseURL),
      });
    }

    if (typeof data === 'object' && data !== null && data._type === 'router') {
      const meta = data._meta || {};
      return new Router({
        commands: this._getDocumentContent(data, baseURL),
        name: meta.name || '',
        overview: meta.overview || '',
        description: meta.description || '',
        epilog: data.epilog || '',
        priority: meta.priority !== undefined ? meta.priority : 1,
        resource: meta.resource || '',
      });
    }

    if (typeof data === 'object' && data !== null && data._type === 'action') {
      return new Action({
        url: data.url ? new URL(data.url, baseURL).href : '',
        name: data.name || '',
        overview: data.overview || '',
        description: data.description || '',
        epilog: data.epilog || '',
        priority: data.priority !== undefined ? data.priority : 1,
        resource: data.resource || '',
        confirm: !!data.confirm,
        fields: Array.isArray(data.fields)
          ? data.fields
              .map((item) => {
                if (typeof item === 'object' && item !== null) {
                  return new Field({
                    method: item.method || '',
                    name: item.name || '',
                    type: item.type || '',
                    argument: item.argument || '',
                    config: item.config || '',
                    description: item.description || '',
                    valueLabel: item.value_label || '',
                    system: !!item.system,
                    required: !!item.required,
                    default: item.default,
                    choices: Array.isArray(item.choices) ? item.choices : [],
                    tags: Array.isArray(item.tags) ? item.tags : [],
                  });
                }
                return null;
              })
              .filter((item) => item !== null)
          : [],
      });
    }

    if (typeof data === 'object' && data !== null) {
      return new SchemaObject(this._getDocumentContent(data, baseURL));
    }

    if (Array.isArray(data)) {
      return new SchemaArray(data.map((item) => this._convertToSchema(item, baseURL)));
    }

    return data;
  }

  /**
   * Get document content
   * @param {Object} item - Item to process
   * @param {string} baseURL - Base URL for resolving relative URLs
   * @returns {Object} Document content
   */
  _getDocumentContent(item, baseURL = '') {
    const content = {};
    for (const [key, value] of Object.entries(item)) {
      if (key !== '_type' && key !== '_meta') {
        const unescapedKey = this._unescapeKey(key);
        content[unescapedKey] = this._convertToSchema(value, baseURL);
      }
    }
    return content;
  }

  /**
   * Unescape special keys
   * @param {string} string - String to unescape
   * @returns {string} Unescaped string
   */
  _unescapeKey(string) {
    if (string.startsWith('__') && ['type', 'meta'].includes(string.substring(2))) {
      return string.substring(1);
    }
    return string;
  }
}
