/**
 * Data client for the Zimagi JavaScript SDK
 */

import { BaseAPIClient } from './base';
import { DataHTTPTransport } from '../transports/data';
import { OpenAPIJSONCodec, CSVCodec, JSONCodec } from '../codecs/index';
import { ResponseError } from '../exceptions';

/**
 * Data client class
 */
export class DataClient extends BaseAPIClient {
  schema: any;
  _dataInfo: any;

  /**
   * Create a new data client
   * @param {Object} options - Client options
   */
  constructor(options: any = {}) {
    super({
      port: options.port || 5323,
      verifyCert: options.verifyCert !== undefined ? options.verifyCert : false,
      decoders: [new OpenAPIJSONCodec(), new CSVCodec(), new JSONCodec()],
      ...options,
    });

    this.transport = new DataHTTPTransport({
      client: this,
      verifyCert: options.verifyCert,
      optionsCallback: options.optionsCallback,
    });
  }

  /**
   * Initialize data API client
   */
  async initialize() {
    if (!(await this.getStatus()).encryption) {
      this.cipher = null;
    }

    this.schema = await this.getSchema();
    this._dataInfo = this.schema['x-data'] || {};
  }

  /**
   * Get API paths
   * @returns {Object} API paths
   */
  getPaths(): any {
    return this.schema.paths;
  }

  /**
   * Get a specific API path
   * @param {string} path - Path to get
   * @returns {*} Path definition
   */
  getPath(path: string): any {
    const normalizedPath = `/${path.replace(/^\/+|\/+$/g, '')}/`;
    return this.getPaths()[normalizedPath];
  }

  /**
   * Get ID field for data type
   * @param {string} dataType - Data type
   * @returns {string} ID field name
   */
  getIdField(dataType: string): string {
    return this._dataInfo[dataType]?.id || '';
  }

  /**
   * Get key field for data type
   * @param {string} dataType - Data type
   * @returns {string} Key field name
   */
  getKeyField(dataType: string): string {
    return this._dataInfo[dataType]?.key || '';
  }

  /**
   * Get system fields for data type
   * @param {string} dataType - Data type
   * @returns {Array} System fields
   */
  getSystemFields(dataType: string): string[] {
    return this._dataInfo[dataType]?.system || [];
  }

  /**
   * Get unique fields for data type
   * @param {string} dataType - Data type
   * @returns {Array} Unique fields
   */
  getUniqueFields(dataType: string): string[] {
    return this._dataInfo[dataType]?.unique || [];
  }

  /**
   * Get dynamic fields for data type
   * @param {string} dataType - Data type
   * @returns {Array} Dynamic fields
   */
  getDynamicFields(dataType: string): string[] {
    return this._dataInfo[dataType]?.dynamic || [];
  }

  /**
   * Get atomic fields for data type
   * @param {string} dataType - Data type
   * @returns {Array} Atomic fields
   */
  getAtomicFields(dataType: string): string[] {
    return this._dataInfo[dataType]?.atomic || [];
  }

  /**
   * Get scope fields for data type
   * @param {string} dataType - Data type
   * @returns {Object} Scope fields
   */
  getScopeFields(dataType: string): any {
    return this._dataInfo[dataType]?.scope || {};
  }

  /**
   * Get relation fields for data type
   * @param {string} dataType - Data type
   * @returns {Object} Relation fields
   */
  getRelationFields(dataType: string): any {
    return this._dataInfo[dataType]?.relations || {};
  }

  /**
   * Get reverse fields for data type
   * @param {string} dataType - Data type
   * @returns {Object} Reverse fields
   */
  getReverseFields(dataType: string): any {
    return this._dataInfo[dataType]?.reverse || {};
  }

  /**
   * Set scope filters for data type
   * @param {string} dataType - Data type
   * @param {Object} values - Scope values
   * @param {Array} parents - Parent scope fields
   * @returns {Object} Scope filters
   */
  setScope(dataType: string, values: any, parents: string[] | null = null): any {
    const scopeFields = this.getScopeFields(dataType);
    const filters: any = {};

    if (parents === null) {
      parents = [];
    }

    for (const [scopeField, scopeType] of Object.entries(scopeFields)) {
      const scopeParents = [...parents, scopeField];
      const fullScopeField = scopeParents.join('__');

      if (values[fullScopeField] !== undefined) {
        const scopeKey = this.getKeyField(scopeType as string);
        filters[`${fullScopeField}__${scopeKey}`] = values[fullScopeField];
        Object.assign(filters, this.setScope(scopeType as string, values, scopeParents));
      }
    }

    return filters;
  }

  /**
   * Get API schema
   * @param {boolean} full - Whether to get full schema
   * @returns {*} Schema data
   */
  async getSchema(full: boolean = false): Promise<any> {
    if (full || !this._schema) {
      const processor = async () => {
        const schema = await this._request('GET', this.baseURL);

        if (full) {
          // Replace path references with actual path objects
          for (const path of Object.keys(schema.paths)) {
            if (schema.paths[path].$ref) {
              schema.paths[path] = this._request('GET', schema.paths[path].$ref);
            }
          }
        }
        return schema;
      };
      this._schema = await this._wrapAPICall('schema', this.baseURL, processor);
    }
    return this._schema;
  }

  /**
   * Execute a data operation
   * @param {string} method - HTTP method
   * @param {string} path - API path
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async _execute(method: string, path: string, options: any = null): Promise<any> {
    const url = `${this.baseURL.replace(/\/+$/, '')}/${path.replace(/^\/+|\/+$/g, '')}`.replace(
      /\/+$/,
      ''
    );

    if (!options) {
      options = {};
    }
    if (method === 'GET') {
      options = this._formatOptions(method, options);
    }

    if (!this._initialized) {
      await this.initialize();
    }

    const processor = async () => {
      return await this._request(method, url, options);
    };
    return await this._wrapAPICall('data', path, processor, options);
  }

  /**
   * Execute a data type operation
   * @param {string} method - HTTP method
   * @param {string} dataType - Data type
   * @param {string | null} op - Operation
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async _executeTypeOperation(
    method: string,
    dataType: string,
    op: string | null,
    options: any
  ): Promise<any> {
    const path = op === null ? dataType : `${dataType}/${op}`;
    return await this._execute(method, path, options);
  }

  /**
   * Execute a key operation
   * @param {string} method - HTTP method
   * @param {string} dataType - Data type
   * @param {string | null} op - Operation
   * @param {string} key - Key value
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async _executeKeyOperation(
    method: string,
    dataType: string,
    op: string | null,
    key: string,
    options: any
  ): Promise<any> {
    const path = op === null ? `${dataType}/${key}` : `${dataType}/${key}/${op}`;
    return await this._execute(method, path, options);
  }

  /**
   * Execute a field operation
   * @param {string} method - HTTP method
   * @param {string} dataType - Data type
   * @param {string} op - Operation
   * @param {string | null} fieldName - Field name
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async _executeFieldOperation(
    method: string,
    dataType: string,
    op: string,
    fieldName: string | null,
    options: any
  ): Promise<any> {
    if (!fieldName) {
      fieldName = this.getIdField(dataType);
    }

    const path = `${dataType}/${op}/${fieldName}`;
    return await this._execute(method, path, options);
  }

  /**
   * Create a new data record
   * @param {string} dataType - Data type
   * @param {Object} fields - Record fields
   * @returns {*} Response data
   */
  async create(dataType: string, fields: any = {}): Promise<any> {
    return await this._executeTypeOperation('POST', dataType, null, fields);
  }

  /**
   * Update an existing data record
   * @param {string} dataType - Data type
   * @param {string} id - Record ID
   * @param {Object} fields - Record fields
   * @returns {*} Response data
   */
  async update(dataType: string, id: string, fields: any = {}): Promise<any> {
    return await this._executeKeyOperation('PUT', dataType, null, id, fields);
  }

  /**
   * Delete a data record
   * @param {string} dataType - Data type
   * @param {string} id - Record ID
   * @returns {*} Response data
   */
  async delete(dataType: string, id: string): Promise<any> {
    return await this._executeKeyOperation('DELETE', dataType, null, id, {});
  }

  /**
   * Get a data record by ID
   * @param {string} dataType - Data type
   * @param {string} id - Record ID
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async get(dataType: string, id: string, options: any = {}): Promise<any> {
    return await this._executeKeyOperation('GET', dataType, null, id, options);
  }

  /**
   * Get a data record by key
   * @param {string} dataType - Data type
   * @param {string} key - Record key
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async getByKey(dataType: string, key: string, options: any = {}): Promise<any> {
    const results = await this._executeTypeOperation('GET', dataType, null, {
      [this.getKeyField(dataType)]: key,
      ...this.setScope(dataType, options),
    });

    if (results.count === null) {
      throw new ResponseError(`Instance ${dataType} ${key}: ${results}`);
    } else if (results.count === 0) {
      throw new ResponseError(`Instance ${dataType} ${key}: not found`);
    } else if (results.count > 1) {
      throw new ResponseError(`Instance ${dataType} ${key}: too many found`);
    }

    return results.results[0];
  }

  /**
   * List data records
   * @param {string} dataType - Data type
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async list(dataType: string, options: any = {}): Promise<any> {
    return await this._executeTypeOperation('GET', dataType, null, options);
  }

  /**
   * Get data in JSON format
   * @param {string} dataType - Data type
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async json(dataType: string, options: any = {}): Promise<any> {
    return await this._executeTypeOperation('GET', dataType, 'json', options);
  }

  /**
   * Get data in CSV format
   * @param {string} dataType - Data type
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async csv(dataType: string, options: any = {}): Promise<any> {
    return await this._executeTypeOperation('GET', dataType, 'csv', options);
  }

  /**
   * Get field values
   * @param {string} dataType - Data type
   * @param {string | null} fieldName - Field name
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  async values(dataType: string, fieldName: string | null = null, options: any = {}): Promise<any> {
    return await this._executeFieldOperation('GET', dataType, 'values', fieldName, options);
  }

  /**
   * Get record count
   * @param {string} dataType - Data type
   * @param {string | null} fieldName - Field name
   * @param {Object} options - Request options
   * @returns {number} Record count
   */
  async count(
    dataType: string,
    fieldName: string | null = null,
    options: any = {}
  ): Promise<number> {
    const result = await this._executeFieldOperation('GET', dataType, 'count', fieldName, options);
    return result.count || 0;
  }

  /**
   * Download a dataset
   * @param {string} datasetName - Dataset name
   * @returns {*} Response data
   */
  async download(datasetName: string): Promise<any> {
    return await this._execute('GET', `download/${datasetName}`);
  }

  /**
   * Format request options
   * @param {string} method - HTTP method
   * @param {Object} options - Request options
   * @returns {Object} Formatted options
   */
  _formatOptions(method: string, options: any): any {
    if (options === null) {
      options = {};
    }

    for (const [key, value] of Object.entries(options)) {
      if (typeof value === 'object' && value !== null) {
        if (Array.isArray(value) && method === 'GET') {
          options[key] = (value as any[]).join(',');
        } else {
          options[key] = JSON.stringify(value);
        }
      }
    }
    return options;
  }
}
