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
    console.debug(`[Zimagi SDK] CommandHTTPTransport initialized`);
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
    console.debug(`[Zimagi SDK] CommandHTTPTransport.handleRequest: ${method} ${url}`);
    console.debug(`[Zimagi SDK] Path: ${path}`);

    if (path.match(/^\/status\/?$/)) {
      console.debug(`[Zimagi SDK] Handling status request`);

      return await this.requestPage(url, headers, null, _decoders, {
        encrypted: false,
        useAuth: false,
        disableCallbacks: true,
      });
    }

    if (!path || path === '/' || path === '') {
      console.debug(`[Zimagi SDK] Handling root request`);

      return await this.requestPage(url, headers, null, _decoders, {
        encrypted: false,
        useAuth: true,
        disableCallbacks: true,
      });
    }

    console.debug(`[Zimagi SDK] Handling command request`);
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
    console.debug(`[Zimagi SDK] CommandHTTPTransport.requestCommand: ${url}`);

    const commandResponse = new CommandResponse();

    const result = await this._request('POST', url, {
      headers: headers,
      params: params,
      encrypted: true,
      useAuth: true,
    });

    console.debug(`[Zimagi SDK] Command request completed: ${url}`);
    console.debug(`[Zimagi SDK] Response status: ${result[1].status}`);

    if (result[1].status >= 400) {
      const error = this._formatResponseError(result[1], this.client && this.client.cipher);
      console.debug(`[Zimagi SDK] Command request error:`, error);
      throw new ResponseError(error.message, result[1].status, error.data);
    }

    try {
      // Process streaming response
      console.debug(`[Zimagi SDK] Processing streaming response`);

      const reader = result[1].body.getReader();
      const decoder = new TextDecoder();

      let done = false;
      let messageCount = 0;

      while (!done) {
        const { done: readerDone, value } = await reader.read();
        done = readerDone;

        if (value) {
          const text = decoder.decode(value);
          console.debug(`[Zimagi SDK] Received stream chunk:`, text);

          const lines = text.split('\n');

          for (const line of lines) {
            if (line.trim()) {
              messageCount++;
              console.debug(`[Zimagi SDK] Processing message ${messageCount}:`, line);

              const messageData = JSON.parse(line);
              const message = Message.get(messageData, this.client && this.client.cipher);

              if (this._messageCallback && typeof this._messageCallback === 'function') {
                console.debug(`[Zimagi SDK] Calling message callback`);
                this._messageCallback(message);
              }

              commandResponse.add(message);
            }
          }
        }
      }

      console.debug(`[Zimagi SDK] Stream processing complete. Total messages: ${messageCount}`);
    } catch (error: any) {
      console.debug(`[Zimagi SDK] Error processing stream:`, error);
      console.debug(
        `[Zimagi SDK] Response headers:`,
        Object.fromEntries(result[1].headers.entries())
      );
      console.debug(`[Zimagi SDK] Response status: ${result[1].status}`);
      throw error;
    }

    if (commandResponse.error()) {
      console.debug(`[Zimagi SDK] Command response has errors`);
      throw new ResponseError(commandResponse.errorMessage(), result[1].status);
    }

    return commandResponse;
  }
}
