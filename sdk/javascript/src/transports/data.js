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
    // Reduce logging in test environment
    if (typeof process === 'undefined' || !process.env || process.env.NODE_ENV !== 'test') {
      console.debug(`[Zimagi SDK] DataHTTPTransport.handleRequest: ${method} ${url}`);
      console.debug(`[Zimagi SDK] Path: ${path}`);
    }

    if (method === 'GET') {
      if (path.match(/^\/status\/?$/)) {
        // Reduce logging in test environment
        if (typeof process === 'undefined' || !process.env || process.env.NODE_ENV !== 'test') {
          console.debug(`[Zimagi SDK] Handling status request`);
        }
        return await this.requestPage(url, headers, null, decoders, {
          encrypted: false,
          useAuth: false,
          disableCallbacks: true,
        });
      }

      if (!path || path === '/' || path.startsWith('/schema/')) {
        // Reduce logging in test environment
        if (typeof process === 'undefined' || !process.env || process.env.NODE_ENV !== 'test') {
          console.debug(`[Zimagi SDK] Handling schema/root request`);
        }
        return await this.requestPage(url, headers, null, decoders, {
          encrypted: false,
          useAuth: true,
          disableCallbacks: true,
        });
      }

      // Reduce logging in test environment
      if (typeof process === 'undefined' || !process.env || process.env.NODE_ENV !== 'test') {
        console.debug(`[Zimagi SDK] Handling data request`);
      }
      return await this.requestPage(url, headers, params, decoders, {
        encrypted: true,
        useAuth: true,
      });
    }

    // Reduce logging in test environment
    if (typeof process === 'undefined' || !process.env || process.env.NODE_ENV !== 'test') {
      console.debug(`[Zimagi SDK] Handling data update request`);
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
    // Reduce logging in test environment
    if (typeof process === 'undefined' || !process.env || process.env.NODE_ENV !== 'test') {
      console.debug(`[Zimagi SDK] DataHTTPTransport.updateData: ${method} ${url}`);
    }

    const [request, response] = await this._request(method, url, {
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
      params: JSON.stringify(params),
      encrypted: encrypted,
      useAuth: true,
    });

    // Reduce logging in test environment
    if (typeof process === 'undefined' || !process.env || process.env.NODE_ENV !== 'test') {
      console.debug(`[Zimagi SDK] Update data request completed: ${method} ${url}`);
      console.debug(`[Zimagi SDK] Response status: ${response.status}`);
    }

    if (response.status >= 400) {
      const error = this._formatResponseError(
        response,
        encrypted && this.client ? this.client.cipher : null
      );
      // Reduce logging in test environment
      if (typeof process === 'undefined' || !process.env || process.env.NODE_ENV !== 'test') {
        console.debug(`[Zimagi SDK] Update data request error:`, error);
      }
      throw new ResponseError(error.message, response.status, error.data);
    }

    return this.decodeMessage(request, response, decoders, null, encrypted);
  }
}
