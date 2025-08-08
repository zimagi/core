/**
 * Base transport class for the Zimagi JavaScript SDK
 */

import fetch from 'node-fetch';
import { ConnectionError, ResponseError, ClientError } from '../exceptions';

/**
 * Transport options interface
 */
export interface TransportOptions {
  client?: any;
  verifyCert?: boolean;
  optionsCallback?: Function;
  requestCallback?: Function;
  responseCallback?: Function;
}

/**
 * Base transport class
 */
export class BaseTransport {
  protected client: any;
  protected verifyCert: boolean;
  protected optionsCallback: Function | null;
  protected requestCallback: Function | null;
  protected responseCallback: Function | null;

  /**
   * Create a new transport
   * @param {Object} options - Transport options
   */
  constructor(options: TransportOptions = {}) {
    this.client = options.client || null;
    this.verifyCert = options.verifyCert || false;
    this.optionsCallback = options.optionsCallback || null;
    this.requestCallback = options.requestCallback || null;
    this.responseCallback = options.responseCallback || null;
  }

  /**
   * Make an HTTP request
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {Array} decoders - Array of codec decoders
   * @param {Object} params - Request parameters
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async request(
    method: string,
    url: string,
    decoders: any[],
    params: any = null,
    options: any = {}
  ): Promise<any> {
    const connectionErrorMessage = `
The Zimagi client failed to connect with the server.

This could indicate the server is down or restarting.
If restarting, retry in a few minutes...
`;
    try {
      const acceptMediaTypes: string[] = [];
      for (const decoder of decoders) {
        acceptMediaTypes.push(...decoder.mediaTypes);
      }

      const headers = {
        accept: acceptMediaTypes.join(', '),
        'user-agent': 'zimagi-javascript',
      };

      if (!params) {
        params = {};
      }

      if (this.optionsCallback && typeof this.optionsCallback === 'function') {
        this.optionsCallback(params);
      }

      console.debug(`[Zimagi SDK] Making request: ${method} ${url}`);
      console.debug(`[Zimagi SDK] Request headers: ${JSON.stringify(headers)}`);
      console.debug(`[Zimagi SDK] Request params: ${JSON.stringify(params)}`);

      return await this.handleRequest(
        method,
        url,
        new URL(url).pathname,
        headers,
        params,
        decoders
      );
    } catch (error: any) {
      console.debug(`[Zimagi SDK] Request to ${url} failed: ${error.message}`);
      console.debug(`[Zimagi SDK] Error stack: ${error.stack}`);

      if ((options.tries || 3) > 0) {
        console.debug(`[Zimagi SDK] Retrying request (${options.tries || 3} tries remaining)`);
        await this._sleep((options.retryWait || 2) * 1000);
        return await this.request(method, url, decoders, params, {
          ...options,
          tries: (options.tries || 3) - 1,
          retryWait: options.retryWait || 2,
        });
      }

      throw new ConnectionError(connectionErrorMessage);
    }
  }

  /**
   * Handle a request - must be implemented by subclasses
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {string} path - Request path
   * @param {Object} headers - Request headers
   * @param {Object} params - Request parameters
   * @param {Array} decoders - Array of codec decoders
   * @returns {*} Response data
   */
  async handleRequest(
    _method: string,
    _url: string,
    _path: string,
    _headers: any,
    _params: any,
    _decoders: any[]
  ): Promise<any> {
    throw new Error('Method handleRequest(...) must be overridden in all subclasses');
  }

  /**
   * Request a page
   * @param {string} url - Request URL
   * @param {Object} headers - Request headers
   * @param {Object} params - Request parameters
   * @param {Array} decoders - Array of codec decoders
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async requestPage(
    url: string,
    headers: any,
    params: any,
    decoders: any[],
    options: any = {}
  ): Promise<any> {
    const encrypted = options.encrypted !== false;
    const useAuth = options.useAuth !== false;
    const disableCallbacks = options.disableCallbacks || false;

    console.debug(`[Zimagi SDK] Requesting page: ${url}`);
    console.debug(`[Zimagi SDK] Page request options:`, { encrypted, useAuth, disableCallbacks });

    const result = await this._request('GET', url, {
      headers: headers,
      params: params || {},
      encrypted: encrypted,
      useAuth: useAuth,
      disableCallbacks: disableCallbacks,
    });

    console.debug(`[Zimagi SDK] Page request completed: ${url}`);
    console.debug(`[Zimagi SDK] Response status: ${result[1].status}`);

    if (result[1].status >= 400) {
      const error = this._formatResponseError(
        result[1],
        encrypted && this.client ? this.client.cipher : null
      );
      console.debug(`[Zimagi SDK] Page request error:`, error);
      throw new ResponseError(error.message, result[1].status, error.data);
    }

    return this.decodeMessage(result[0], result[1], decoders, null, encrypted, disableCallbacks);
  }

  /**
   * Make an HTTP request
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {Object} options - Request options
   * @returns {Array} Request and response objects
   */
  async _request(method: string, url: string, options: any = {}): Promise<any[]> {
    const {
      headers = {},
      params = null,
      encrypted = true,
      useAuth = true,
      disableCallbacks = false,
    } = options;

    // Create request object
    const requestHeaders = { ...headers };

    if (useAuth && this.client && this.client.auth) {
      // Apply authentication
      this.client.auth.apply(requestHeaders);
    }

    let body: string | undefined = undefined;
    let requestUrl = url;

    if (params) {
      const parameterName = ['POST', 'PUT'].includes(method) ? 'data' : 'params';
      const processedParams =
        encrypted && this.client && this.client.cipher ? this._encryptParams(params) : params;

      if (parameterName === 'data') {
        body =
          typeof processedParams === 'string' ? processedParams : JSON.stringify(processedParams);
        requestHeaders['Content-Type'] = 'application/json';
      } else {
        // Handle query parameters
        const urlObj = new URL(requestUrl);
        for (const [key, value] of Object.entries(processedParams)) {
          if (value !== null && value !== undefined) {
            urlObj.searchParams.append(key, String(value));
          }
        }
        requestUrl = urlObj.toString();
      }
    }

    const fetchOptions: any = {
      method: method,
      headers: requestHeaders,
      body: body,
    };

    console.debug(`[Zimagi SDK] Making fetch request: ${method} ${requestUrl}`);
    console.debug(`[Zimagi SDK] Fetch options:`, fetchOptions);

    if (!disableCallbacks && this.requestCallback && typeof this.requestCallback === 'function') {
      this.requestCallback(fetchOptions);
    }

    const startTime = Date.now();
    console.debug(`[Zimagi SDK] Starting fetch request at ${startTime}`);

    const response: any = await fetch(requestUrl, fetchOptions);

    const endTime = Date.now();
    console.debug(
      `[Zimagi SDK] Fetch request completed at ${endTime} (duration: ${endTime - startTime}ms)`
    );
    console.debug(`[Zimagi SDK] Response status: ${response.status}`);
    console.debug(`[Zimagi SDK] Response headers:`, Object.fromEntries(response.headers.entries()));

    return [{ url: requestUrl, method, headers: requestHeaders }, response];
  }

  /**
   * Encrypt request parameters
   * @param {Object} params - Parameters to encrypt
   * @returns {Object} Encrypted parameters
   */
  _encryptParams(params: any): any {
    if (!this.client || !this.client.cipher) {
      return params;
    }

    if (typeof params === 'string') {
      return this.client.cipher.encrypt(params);
    }

    const encParams: any = {};
    for (const [key, value] of Object.entries(params)) {
      encParams[key] = this.client.cipher.encrypt(value);
    }
    return encParams;
  }

  /**
   * Decode a response message
   * @param {Object} request - Request object
   * @param {Object} response - Response object
   * @param {Array} decoders - Array of codec decoders
   * @param {*} message - Message to decode
   * @param {boolean} decrypt - Whether to decrypt
   * @param {boolean} disableCallbacks - Whether to disable callbacks
   * @returns {*} Decoded data
   */
  async decodeMessage(
    request: any,
    response: any,
    decoders: any[],
    message: any = null,
    decrypt: boolean = true,
    disableCallbacks: boolean = false
  ): Promise<any> {
    let content = message !== null ? message : null;

    // Get response content
    if (!content && response.body) {
      try {
        // For non-streaming responses, get the text content
        if (response.bodyUsed) {
          // If body is already used, we can't read it again
          content = '';
        } else {
          content = await response.text();
        }
      } catch (error: any) {
        console.debug(`[Zimagi SDK] Error reading response body: ${error.message}`);
        content = '';
      }
    }

    let data = null;

    if (content || content === '') {
      const contentType = response.headers.get('content-type') || '';
      console.debug(`[Zimagi SDK] Decoding response with content-type: ${contentType}`);

      const codec = this._getDecoder(contentType.split(';')[0].trim().toLowerCase(), decoders);

      if (decrypt && this.client && this.client.cipher) {
        console.debug(`[Zimagi SDK] Decrypting response content`);
        content = this.client.cipher.decrypt(content);
      }

      data = codec.decode(content, {
        baseURL: response.url,
        contentType: contentType,
      });

      if (
        !disableCallbacks &&
        this.responseCallback &&
        typeof this.responseCallback === 'function'
      ) {
        this.responseCallback(request, response, data);
      }
    }

    return data;
  }

  /**
   * Get appropriate decoder for content type
   * @param {string} contentType - Content type
   * @param {Array} decoders - Array of codec decoders
   * @returns {Object} Decoder
   */
  _getDecoder(contentType: string, decoders: any[]): any {
    console.debug(`[Zimagi SDK] Looking for decoder for content type: ${contentType}`);
    for (const codec of decoders) {
      if (codec.mediaTypes.includes(contentType)) {
        console.debug(`[Zimagi SDK] Found decoder: ${codec.constructor.name}`);
        return codec;
      }
    }

    throw new ClientError(`Unsupported media in Content-Type header '${contentType}'`);
  }

  /**
   * Format response error
   * @param {Object} response - Response object
   * @param {Object} cipher - Cipher for decryption
   * @returns {Object} Formatted error
   */
  _formatResponseError(response: any, cipher: any = null): any {
    let message = response.statusText;
    console.debug(
      `[Zimagi SDK] Formatting response error: ${response.status} ${response.statusText}`
    );

    if (cipher) {
      // Decrypt error message if needed
      console.debug(`[Zimagi SDK] Decrypting error message`);
      message = cipher.decrypt(response.body);
    }

    try {
      const errorData = JSON.parse(message);
      const errorRender = JSON.stringify(errorData, null, 2);
      console.debug(`[Zimagi SDK] Parsed error data:`, errorData);
      return {
        message: `Error ${response.status}: ${response.statusText}: ${errorRender}`,
        data: errorData,
      };
    } catch (error: any) {
      console.debug(`[Zimagi SDK] Error parsing error data: ${error.message}`);
      return {
        message: `Error ${response.status}: ${response.statusText}: ${message}`,
        data: message,
      };
    }
  }

  /**
   * Sleep for specified milliseconds
   * @param {number} ms - Milliseconds to sleep
   * @returns {Promise} Sleep promise
   */
  _sleep(ms: number): Promise<void> {
    console.debug(`[Zimagi SDK] Sleeping for ${ms}ms`);
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
