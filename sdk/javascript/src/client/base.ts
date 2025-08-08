/**
 * Base API client for the Zimagi JavaScript SDK
 */

import { getServiceURL } from '../utility';
import { ClientTokenAuthentication } from '../auth';
import { Cipher } from '../encryption';
import { ClientError } from '../exceptions';
import { defaultCache } from '../cache';
import { defaultMonitor } from '../performance';

/**
 * Base API client class
 */
export class BaseAPIClient {
  /**
   * Create a new API client
   * @param {Object} options - Client options
   */
  host: string;
  port: number;
  user: string;
  token: string;
  encryptionKey: string | null;
  protocol: string;
  verifyCert: boolean;
  baseURL: string;
  cipher: any;
  transport: any;
  decoders: any[];
  cache: any;
  performanceMonitor: any;
  auth: ClientTokenAuthentication;
  _status: any;
  _schema: any;
  _initialized: boolean;

  constructor(options: any = {}) {
    this.host = options.host || 'localhost';
    this.port = options.port;
    this.user = options.user || 'admin';
    this.token = options.token || 'uy5c8xiahf93j2pl8s00e6nb32h87dn3';
    this.encryptionKey = options.encryptionKey || null;
    this.protocol = options.protocol || (this.host == 'localhost' ? 'http' : 'https');
    this.verifyCert = options.verifyCert !== undefined ? options.verifyCert : false;

    this.baseURL = this._getServiceURL();
    this.cipher = this.encryptionKey ? Cipher.get(this.encryptionKey) : null;
    this.transport = null;
    this.decoders = options.decoders || [];
    this.cache = options.cache || defaultCache;
    this.performanceMonitor = options.performanceMonitor || defaultMonitor;

    this.auth = new ClientTokenAuthentication(this.user, this.token, this);
    this._status = null;
    this._schema = null;
    this._initialized = false;

    console.debug(`[Zimagi SDK] BaseAPIClient initialized with:`, {
      host: this.host,
      port: this.port,
      protocol: this.protocol,
      baseURL: this.baseURL,
    });
  }

  /**
   * Initialize API client
   */
  async initialize() {
    throw new ClientError('Zimagi API client initialize method not defined');
  }

  /**
   * Get service URL
   * @returns {string} Service URL
   */
  _getServiceURL(): string {
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
  async _request(
    method: string,
    url: string,
    params: any = null,
    validateCallback: Function | null = null
  ): Promise<any> {
    if (!this.transport) {
      throw new ClientError('Zimagi API client transport not defined');
    }

    const timingId = this.performanceMonitor.startTiming(`${method}_${url}`);

    try {
      console.debug(`[Zimagi SDK] Making client request: ${method} ${url}`);
      console.debug(`[Zimagi SDK] Request params:`, params);

      const result = await this.transport.request(method, url, this.decoders, params, {
        retries: 20,
        retryWait: 3,
        validateCallback,
      });

      this.performanceMonitor.endTiming(timingId);
      return result;
    } catch (error: any) {
      console.debug(`${'type'} API error: ${this._formatError('path', error, params)}`);
      this.performanceMonitor.endTiming(timingId);
      throw error;
    }
  }

  /**
   * Get service status
   * @returns {*} Status data
   */
  async getStatus(): Promise<any> {
    console.debug(`[Zimagi SDK] Getting status`);

    if (!this._status) {
      const statusURL = `${this.baseURL}status`;
      console.debug(`[Zimagi SDK] Status URL: ${statusURL}`);

      const processor = async () => {
        return await this._request('GET', statusURL);
      };
      this._status = await this._wrapAPICall('status', statusURL, processor);

      console.debug(`[Zimagi SDK] Status result:`, this._status);
    }
    return this._status;
  }

  /**
   * Get API schema
   * @returns {*} Schema data
   */
  async getSchema(): Promise<any> {
    console.debug(`[Zimagi SDK] Getting schema`);

    if (!this._schema) {
      const schemaGenerator = async () => {
        const processor = async () => {
          return await this._request('GET', this.baseURL);
        };
        return await this._wrapAPICall('schema', this.baseURL, processor);
      };

      this._schema = await this._cacheData(
        `${this.host}.${this.port}`,
        schemaGenerator,
        86400000 // 24 hours
      );

      console.debug(`[Zimagi SDK] Schema result:`, this._schema);
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
  async _wrapAPICall(
    type: string,
    path: string,
    processor: Function,
    params: any = null
  ): Promise<any> {
    try {
      console.debug(`[Zimagi SDK] Wrapping API call: ${type} ${path}`);
      return await processor();
    } catch (error: any) {
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
  _formatError(path: string, error: Error, params: any = null): string {
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
  async _cacheData(
    cacheName: string,
    generatorFunction: Function,
    cacheLifetime: number = 3600000
  ): Promise<any> {
    const cacheKey = `zimagi_${cacheName}`;
    const cachedData = this.cache.get(cacheKey);

    console.debug(`[Zimagi SDK] Checking cache for: ${cacheKey}`);
    console.debug(`[Zimagi SDK] Cache hit: ${!!cachedData}`);

    if (cachedData) {
      return cachedData;
    }

    console.debug(`[Zimagi SDK] Generating data for cache: ${cacheKey}`);

    const data = await generatorFunction();
    this.cache.set(cacheKey, data, cacheLifetime);
    console.debug(`[Zimagi SDK] Data cached: ${cacheKey}`);

    return data;
  }

  /**
   * Get performance statistics
   * @returns {Object} Performance statistics
   */
  getPerformanceStats(): any {
    return this.performanceMonitor.getAllStatistics();
  }

  /**
   * Clear performance metrics
   */
  clearPerformanceMetrics(): void {
    this.performanceMonitor.clear();
  }
}
