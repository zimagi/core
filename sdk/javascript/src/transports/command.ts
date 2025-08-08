/**
 * Command HTTP transport for the Zimagi JavaScript SDK
 */

import { BaseTransport, TransportOptions } from './base';
import { ResponseError } from '../exceptions';
import { CommandResponse } from '../command/response';
import { Message } from '../messages';

export interface CommandTransportOptions extends TransportOptions {
  messageCallback?: Function;
}

export class CommandHTTPTransport extends BaseTransport {
  private _messageCallback: Function | undefined;

  constructor(options: CommandTransportOptions = {}) {
    super(options);
    this._messageCallback = options.messageCallback;
    this.debug(`CommandHTTPTransport initialized`);
  }

  /**
   * Handle a request
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {string} path - Request path
   * @param {Object} headers - Request headers
   * @param {Object} params - Request parameters
   * @param {Array} _decoders - Array of codec decoders
   * @returns {*} Response data
   */
  async handleRequest(
    method: string,
    url: string,
    path: string,
    headers: any,
    params: any,
    _decoders: any[]
  ): Promise<any> {
    this.debug(`CommandHTTPTransport.handleRequest: ${method} ${url}`);
    this.debug(`Path: ${path}`);

    if (path.match(/^\/status\/?$/)) {
      this.debug(`Handling status request`);

      return await this.requestPage(url, headers, null, _decoders, {
        encrypted: false,
        useAuth: false,
        disableCallbacks: true,
      });
    }

    if (!path || path === '/' || path === '') {
      this.debug(`Handling root request`);

      return await this.requestPage(url, headers, null, _decoders, {
        encrypted: false,
        useAuth: true,
        disableCallbacks: true,
      });
    }

    this.debug(`Handling command request`);
    return await this.requestCommand(url, headers, params);
  }

  /**
   * Request a command
   * @param {string} url - Request URL
   * @param {Object} headers - Request headers
   * @param {Object} params - Request parameters
   * @returns {*} Response data
   */
  async requestCommand(url: string, headers: any, params: any): Promise<any> {
    this.debug(`CommandHTTPTransport.requestCommand: ${url}`);

    const commandResponse = new CommandResponse();

    const result = await this._request('POST', url, {
      headers: headers,
      params: params,
      encrypted: true,
      useAuth: true,
    });

    this.debug(`Command request completed: ${url}`);
    this.debug(`Response status: ${result[1].status}`);

    if (result[1].status >= 400) {
      const error = this._formatResponseError(result[1], this.client && this.client.cipher);
      this.debug(`Command request error:`, error);
      throw new ResponseError(error.message, result[1].status, error.data);
    }

    try {
      // Process streaming response
      this.debug(`Processing streaming response`);

      const reader = result[1].body.getReader();
      const decoder = new TextDecoder();

      let done = false;
      let messageCount = 0;

      while (!done) {
        const { done: readerDone, value } = await reader.read();
        done = readerDone;

        if (value) {
          const text = decoder.decode(value);
          this.debug(`Received stream chunk:`, text);

          const lines = text.split('\n');

          for (const line of lines) {
            if (line.trim()) {
              messageCount++;
              this.debug(`Processing message ${messageCount}:`, line);

              const messageData = JSON.parse(line);
              const message = Message.get(messageData, this.client && this.client.cipher);

              if (this._messageCallback && typeof this._messageCallback === 'function') {
                this.debug(`Calling message callback`);
                this._messageCallback(message);
              }

              commandResponse.add(message);
            }
          }
        }
      }

      this.debug(`Stream processing complete. Total messages: ${messageCount}`);
    } catch (error: any) {
      this.debug(`Error processing stream:`, error);
      this.debug(`Response headers:`, Object.fromEntries(result[1].headers.entries()));
      this.debug(`Response status: ${result[1].status}`);
      throw error;
    }

    if (commandResponse.error()) {
      this.debug(`Command response has errors`);
      throw new ResponseError(commandResponse.errorMessage(), result[1].status);
    }

    return commandResponse;
  }
}
