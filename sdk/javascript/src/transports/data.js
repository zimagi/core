/**
 * Data HTTP transport for the Zimagi JavaScript SDK
 */

import { BaseTransport } from './base.js';
import { ResponseError } from '../exceptions.js';

/**
 * Data HTTP transport implementation
 */
export class DataHTTPTransport extends BaseTransport {
  /**
   * Handle a request
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {string} path - Request path
   * @param {Object} headers - Request headers
   * @param {Object} params - Request parameters
   * @param {Array} decoders - Array of codec decoders
   * @returns {*} Response data
   */
  async handleRequest(method, url, path, headers, params, decoders) {
    if (method === 'GET') {
      if (path.match(/^\/status\/?$/)) {
        return await this.requestPage(url, headers, null, decoders, {
          encrypted: false,
          useAuth: false,
          disableCallbacks: true,
        });
      }

      if (!path || path === '/' || path.startsWith('/schema/')) {
        return await this.requestPage(url, headers, null, decoders, {
          encrypted: false,
          useAuth: true,
          disableCallbacks: true,
        });
      }

      return await this.requestPage(url, headers, params, decoders, {
        encrypted: true,
        useAuth: true,
      });
    }

    return await this.updateData(method, url, headers, params, decoders);
  }

  /**
   * Update data
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {Object} headers - Request headers
   * @param {Object} params - Request parameters
   * @param {Array} decoders - Array of codec decoders
   * @param {boolean} encrypted - Whether to encrypt
   * @returns {*} Response data
   */
  async updateData(method, url, headers, params, decoders, encrypted = true) {
    const [request, response] = await this._request(method, url, {
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
      params: JSON.stringify(params),
      encrypted: encrypted,
      useAuth: true,
    });

    console.debug(`${method} ${url} request headers: ${JSON.stringify(headers)}`);

    if (response.status >= 400) {
      const error = this._formatResponseError(
        response,
        encrypted && this.client ? this.client.cipher : null
      );
      throw new ResponseError(error.message, response.status, error.data);
    }

    return this.decodeMessage(request, response, decoders, null, encrypted);
  }
}
