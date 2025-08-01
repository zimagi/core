/**
 * Base API client for the Zimagi JavaScript SDK
 */

import { getServiceURL } from '../utility.js';
import { Cipher } from '../encryption.js';
import { ClientTokenAuthentication } from '../auth.js';
import { ClientError } from '../exceptions.js';
import { defaultCache } from '../cache.js';
import { defaultMonitor } from '../performance.js';

/**
 * Base API client class
 */
export class BaseAPIClient {
  /**
   * Create a new API client
   * @param {Object} options - Client options
   */
  constructor(options = {}) {
    this.host = options.host || 'localhost';
    this.port = options.port;
    this.user = options.user || 'admin';
    this.token = options.token || 'uy5c8xiahf93j2pl8s00e6nb32h87dn3';
    this.encryptionKey = options.encryptionKey || null;
    this.protocol = options.protocol || 'https';
    this.verifyCert = options.verifyCert !== undefined ? options.verifyCert : false;

    this.baseURL = this._getServiceURL();
    this.cipher = this.encryptionKey ? Cipher.get(this.encryptionKey) : null;
    this.transport = null;
    this.decoders = options.decoders || [];
    this.cache = options.cache || defaultCache;
    this.performanceMonitor = options.performanceMonitor || defaultMonitor;

    this.auth = new ClientTokenAuthentication(this.user, this.token, this);
  }

  /**
   * Get service URL
   * @returns {string} Service URL
   */
  _getServiceURL() {
    return getServiceURL(this.protocol, this.host, this.port);
  }

  /**
   * Make a request
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {Object} params - Request parameters
   * @param {Function} validateCallback - Validation callback
   * @returns {*} Response data
   */
  _request(method, url, params = null, validateCallback = null) {
    if (!this.transport) {
      throw new ClientError('Zimagi API client transport not defined');
    }

    const timingId = this.performanceMonitor.startTiming(`${method}_${url}`);

    try {
      const result = this.transport.request(method, url, this.decoders, params, {
        retries: 20,
        retryWait: 3,
        validateCallback,
      });

      this.performanceMonitor.endTiming(timingId);
      return result;
    } catch (error) {
      this.performanceMonitor.endTiming(timingId);
      throw error;
    }
  }

  /**
   * Get service status
   * @returns {*} Status data
   */
  getStatus() {
    if (!this._status) {
      const statusURL = `${this.baseURL}status`;

      const processor = () => {
        return this._request('GET', statusURL);
      };

      this._status = this._wrapAPICall('status', statusURL, processor);
    }
    return this._status;
  }

  /**
   * Get API schema
   * @returns {*} Schema data
   */
  getSchema() {
    if (!this._schema) {
      const schemaGenerator = () => {
        const processor = () => {
          return this._request('GET', this.baseURL);
        };
        return this._wrapAPICall('schema', this.baseURL, processor);
      };

      this._schema = this._cacheData(
        `${this.host}.${this.port}`,
        schemaGenerator,
        86400000 // 24 hours
      );
    }
    return this._schema;
  }

  /**
   * Wrap API call with error handling
   * @param {string} type - API call type
   * @param {string} path - API path
   * @param {Function} processor - Processor function
   * @param {Object} params - Request parameters
   * @returns {*} Processed result
   */
  _wrapAPICall(type, path, processor, params = null) {
    try {
      return processor();
    } catch (error) {
      console.debug(`${type} API error: ${this._formatError(path, error, params)}`);
      throw error;
    }
  }

  /**
   * Format error message
   * @param {string} path - API path
   * @param {Error} error - Error object
   * @param {Object} params - Request parameters
   * @returns {string} Formatted error message
   */
  _formatError(path, error, params = null) {
    let paramRender = '';
    if (params) {
      paramRender = JSON.stringify(params, null, 2);
    }

    return `[${Array.isArray(path) ? path.join('/') : path}](${paramRender}) ${error.toString()}`;
  }

  /**
   * Cache data with expiration
   * @param {string} cacheName - Cache name
   * @param {Function} generatorFunction - Data generator function
   * @param {number} cacheLifetime - Cache lifetime in milliseconds
   * @returns {*} Cached data
   */
  _cacheData(cacheName, generatorFunction, cacheLifetime = 3600000) {
    const cacheKey = `zimagi_${cacheName}`;
    const cachedData = this.cache.get(cacheKey);

    if (cachedData) {
      return cachedData;
    }

    const data = generatorFunction();
    this.cache.set(cacheKey, data, cacheLifetime);

    return data;
  }

  /**
   * Get performance statistics
   * @returns {Object} Performance statistics
   */
  getPerformanceStats() {
    return this.performanceMonitor.getAllStatistics();
  }

  /**
   * Clear performance metrics
   */
  clearPerformanceMetrics() {
    this.performanceMonitor.clear();
  }
}
