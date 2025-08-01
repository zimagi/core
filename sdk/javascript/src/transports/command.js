/**
 * Command HTTP transport for the Zimagi JavaScript SDK
 */

import { BaseTransport } from './base.js';
import { ResponseError } from '../exceptions.js';
import { CommandResponse } from '../command/response.js';
import { Message } from '../messages/index.js';

/**
 * Command HTTP transport implementation
 */
export class CommandHTTPTransport extends BaseTransport {
  /**
   * Create a new command transport
   * @param {Object} options - Transport options
   */
  constructor(options = {}) {
    super(options);
    this._messageCallback = options.messageCallback || null;
  }

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
    if (path.match(/^\/status\/?$/)) {
      return await this.requestPage(url, headers, null, decoders, {
        encrypted: false,
        useAuth: false,
        disableCallbacks: true,
      });
    }

    if (!path || path === '/' || path === '') {
      return await this.requestPage(url, headers, null, decoders, {
        encrypted: false,
        useAuth: true,
        disableCallbacks: true,
      });
    }

    return await this.requestCommand(url, headers, params, decoders);
  }

  /**
   * Request a command
   * @param {string} url - Request URL
   * @param {Object} headers - Request headers
   * @param {Object} params - Request parameters
   * @param {Array} decoders - Array of codec decoders
   * @returns {*} Response data
   */
  async requestCommand(url, headers, params, decoders) {
    const commandResponse = new CommandResponse();

    const [request, requestResponse] = await this._request('POST', url, {
      stream: true,
      headers: headers,
      params: params,
      encrypted: true,
      useAuth: true,
    });

    console.debug(`Stream ${url} request headers: ${JSON.stringify(headers)}`);

    if (requestResponse.status >= 400) {
      const error = this._formatResponseError(requestResponse, this.client && this.client.cipher);
      throw new ResponseError(error.message, requestResponse.status, error.data);
    }

    try {
      // Process streaming response
      const reader = requestResponse.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split('\n');

        for (const line of lines) {
          if (line.trim()) {
            const messageData = JSON.parse(line);
            const message = Message.get(messageData, this.client && this.client.cipher);

            if (this._messageCallback && typeof this._messageCallback === 'function') {
              this._messageCallback(message);
            }

            commandResponse.add(message);
          }
        }
      }
    } catch (error) {
      console.debug(
        `Stream ${url} error response headers: ${JSON.stringify(
          Object.fromEntries(requestResponse.headers.entries())
        )}`
      );
      console.debug(`Stream ${url} error status code: ${requestResponse.status}`);
      throw error;
    }

    if (commandResponse.error) {
      throw new ResponseError(commandResponse.errorMessage(), requestResponse.status);
    }

    return commandResponse;
  }
}
