/**
 * Base transport class for the Zimagi JavaScript SDK
 */

import fetch from 'node-fetch';
import { ConnectionError, ResponseError, ClientError } from '../exceptions.js';

/**
 * Base transport class
 */
export class BaseTransport {
  /**
   * Create a new transport
   * @param {Object} options - Transport options
   */
  constructor(options = {}) {
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
  async request(method, url, decoders, params = null, options = {}) {
    const connectionErrorMessage = `
The Zimagi client failed to connect with the server.

This could indicate the server is down or restarting.
If restarting, retry in a few minutes...
`;

    try {
      const acceptMediaTypes = [];
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

      if (options.validateCallback && typeof options.validateCallback === 'function') {
        options.validateCallback(url, params);
      }

      return await this.handleRequest(
        method,
        url,
        new URL(url).pathname,
        headers,
        params,
        decoders
      );
    } catch (error) {
      console.debug(`Request ${url} connection error: ${error}`);

      if ((options.tries || 3) > 0) {
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
  async handleRequest(method, url, path, headers, params, decoders) {
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
  async requestPage(url, headers, params, decoders, options = {}) {
    const encrypted = options.encrypted !== false;
    const useAuth = options.useAuth !== false;
    const disableCallbacks = options.disableCallbacks || false;

    const result = await this._request('GET', url, {
      headers: headers,
      params: params,
      encrypted: encrypted,
      useAuth: useAuth,
      disableCallbacks: disableCallbacks,
    });

    console.debug(`Page ${url} request headers: ${JSON.stringify(headers)}`);

    if (result[1].status >= 400) {
      const error = this._formatResponseError(
        result[1],
        encrypted && this.client ? this.client.cipher : null
      );
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
  async _request(method, url, options = {}) {
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

    let body = null;
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
          urlObj.searchParams.append(key, value);
        }
        requestUrl = urlObj.toString();
      }
    }

    const fetchOptions = {
      method: method,
      headers: requestHeaders,
      body: body,
    };

    if (!disableCallbacks && this.requestCallback && typeof this.requestCallback === 'function') {
      this.requestCallback(fetchOptions);
    }

    const response = await fetch(requestUrl, fetchOptions);

    return [{ url: requestUrl, method, headers: requestHeaders }, response];
  }

  /**
   * Encrypt request parameters
   * @param {Object} params - Parameters to encrypt
   * @returns {Object} Encrypted parameters
   */
  _encryptParams(params) {
    if (!this.client || !this.client.cipher) {
      return params;
    }

    if (typeof params === 'string') {
      return this.client.cipher.encrypt(params);
    }

    const encParams = {};
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
  decodeMessage(
    request,
    response,
    decoders,
    message = null,
    decrypt = true,
    disableCallbacks = false
  ) {
    let content = message !== null ? message : null;

    // Get response content
    if (!content && response.body) {
      content = response.body;
    }

    let data = null;

    if (content) {
      const contentType = response.headers.get('content-type') || '';
      const codec = this._getDecoder(contentType.split(';')[0].trim().toLowerCase(), decoders);

      if (decrypt && this.client && this.client.cipher) {
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
  _getDecoder(contentType, decoders) {
    for (const codec of decoders) {
      if (codec.mediaTypes.includes(contentType)) {
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
  _formatResponseError(response, cipher = null) {
    let message = response.statusText;
    if (cipher) {
      // Decrypt error message if needed
      message = cipher.decrypt(response.body);
    }

    try {
      const errorData = JSON.parse(message);
      const errorRender = JSON.stringify(errorData, null, 2);
      return {
        message: `Error ${response.status}: ${response.statusText}: ${errorRender}`,
        data: errorData,
      };
    } catch (error) {
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
  _sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
