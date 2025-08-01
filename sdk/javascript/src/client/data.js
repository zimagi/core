/**
 * Data client for the Zimagi JavaScript SDK
 */

import { BaseAPIClient } from './base.js';
import { DataHTTPTransport } from '../transports/data.js';
import { OpenAPIJSONCodec, CSVCodec, JSONCodec } from '../codecs/index.js';
import { ResponseError } from '../exceptions.js';

/**
 * Data client class
 */
export class DataClient extends BaseAPIClient {
  /**
   * Create a new data client
   * @param {Object} options - Client options
   */
  constructor(options = {}) {
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

    if (!this.getStatus().encryption) {
      this.cipher = null;
    }

    this.schema = this.getSchema();
    this._dataInfo = this.schema['x-data'] || {};
  }

  /**
   * Get API paths
   * @returns {Object} API paths
   */
  getPaths() {
    return this.schema.paths;
  }

  /**
   * Get a specific API path
   * @param {string} path - Path to get
   * @returns {*} Path definition
   */
  getPath(path) {
    const normalizedPath = `/${path.replace(/^\/+|\/+$/g, '')}/`;
    return this.getPaths()[normalizedPath];
  }

  /**
   * Get ID field for data type
   * @param {string} dataType - Data type
   * @returns {string} ID field name
   */
  getIdField(dataType) {
    return this._dataInfo[dataType]?.id || null;
  }

  /**
   * Get key field for data type
   * @param {string} dataType - Data type
   * @returns {string} Key field name
   */
  getKeyField(dataType) {
    return this._dataInfo[dataType]?.key || null;
  }

  /**
   * Get system fields for data type
   * @param {string} dataType - Data type
   * @returns {Array} System fields
   */
  getSystemFields(dataType) {
    return this._dataInfo[dataType]?.system || [];
  }

  /**
   * Get unique fields for data type
   * @param {string} dataType - Data type
   * @returns {Array} Unique fields
   */
  getUniqueFields(dataType) {
    return this._dataInfo[dataType]?.unique || [];
  }

  /**
   * Get dynamic fields for data type
   * @param {string} dataType - Data type
   * @returns {Array} Dynamic fields
   */
  getDynamicFields(dataType) {
    return this._dataInfo[dataType]?.dynamic || [];
  }

  /**
   * Get atomic fields for data type
   * @param {string} dataType - Data type
   * @returns {Array} Atomic fields
   */
  getAtomicFields(dataType) {
    return this._dataInfo[dataType]?.atomic || [];
  }

  /**
   * Get scope fields for data type
   * @param {string} dataType - Data type
   * @returns {Object} Scope fields
   */
  getScopeFields(dataType) {
    return this._dataInfo[dataType]?.scope || {};
  }

  /**
   * Get relation fields for data type
   * @param {string} dataType - Data type
   * @returns {Object} Relation fields
   */
  getRelationFields(dataType) {
    return this._dataInfo[dataType]?.relations || {};
  }

  /**
   * Get reverse fields for data type
   * @param {string} dataType - Data type
   * @returns {Object} Reverse fields
   */
  getReverseFields(dataType) {
    return this._dataInfo[dataType]?.reverse || {};
  }

  /**
   * Set scope filters for data type
   * @param {string} dataType - Data type
   * @param {Object} values - Scope values
   * @param {Array} parents - Parent scope fields
   * @returns {Object} Scope filters
   */
  setScope(dataType, values, parents = null) {
    const scopeFields = this.getScopeFields(dataType);
    const filters = {};

    if (parents === null) {
      parents = [];
    }

    for (const [scopeField, scopeType] of Object.entries(scopeFields)) {
      const scopeParents = [...parents, scopeField];
      const fullScopeField = scopeParents.join('__');

      if (values[fullScopeField] !== undefined) {
        const scopeKey = this.getKeyField(scopeType);
        filters[`${fullScopeField}__${scopeKey}`] = values[fullScopeField];
        Object.assign(filters, this.setScope(scopeType, values, scopeParents));
      }
    }

    return filters;
  }

  /**
   * Get API schema
   * @param {boolean} full - Whether to get full schema
   * @returns {*} Schema data
   */
  getSchema(full = false) {
    if (full || !this._schema) {
      const processor = () => {
        const schema = this._request('GET', this.baseURL);

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

      this._schema = this._wrapAPICall('schema', this.baseURL, processor);
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
  _execute(method, path, options = null) {
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

    const processor = () => {
      return this._request(method, url, options);
    };

    return this._wrapAPICall('data', path, processor, options);
  }

  /**
   * Execute a data type operation
   * @param {string} method - HTTP method
   * @param {string} dataType - Data type
   * @param {string} op - Operation
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  _executeTypeOperation(method, dataType, op, options) {
    const path = op === null ? dataType : `${dataType}/${op}`;
    return this._execute(method, path, options);
  }

  /**
   * Execute a key operation
   * @param {string} method - HTTP method
   * @param {string} dataType - Data type
   * @param {string} op - Operation
   * @param {string} key - Key value
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  _executeKeyOperation(method, dataType, op, key, options) {
    const path = op === null ? `${dataType}/${key}` : `${dataType}/${key}/${op}`;
    return this._execute(method, path, options);
  }

  /**
   * Execute a field operation
   * @param {string} method - HTTP method
   * @param {string} dataType - Data type
   * @param {string} op - Operation
   * @param {string} fieldName - Field name
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  _executeFieldOperation(method, dataType, op, fieldName, options) {
    if (!fieldName) {
      fieldName = this.getIdField(dataType);
    }

    const path = `${dataType}/${op}/${fieldName}`;
    return this._execute(method, path, options);
  }

  /**
   * Create a new data record
   * @param {string} dataType - Data type
   * @param {Object} fields - Record fields
   * @returns {*} Response data
   */
  create(dataType, fields = {}) {
    return this._executeTypeOperation('POST', dataType, null, fields);
  }

  /**
   * Update an existing data record
   * @param {string} dataType - Data type
   * @param {string} id - Record ID
   * @param {Object} fields - Record fields
   * @returns {*} Response data
   */
  update(dataType, id, fields = {}) {
    return this._executeKeyOperation('PUT', dataType, null, id, fields);
  }

  /**
   * Delete a data record
   * @param {string} dataType - Data type
   * @param {string} id - Record ID
   * @returns {*} Response data
   */
  delete(dataType, id) {
    return this._executeKeyOperation('DELETE', dataType, null, id, {});
  }

  /**
   * Get a data record by ID
   * @param {string} dataType - Data type
   * @param {string} id - Record ID
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  get(dataType, id, options = {}) {
    return this._executeKeyOperation('GET', dataType, null, id, options);
  }

  /**
   * Get a data record by key
   * @param {string} dataType - Data type
   * @param {string} key - Record key
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  getByKey(dataType, key, options = {}) {
    const results = this._executeTypeOperation('GET', dataType, null, {
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
  list(dataType, options = {}) {
    return this._executeTypeOperation('GET', dataType, null, options);
  }

  /**
   * Get data in JSON format
   * @param {string} dataType - Data type
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  json(dataType, options = {}) {
    return this._executeTypeOperation('GET', dataType, 'json', options);
  }

  /**
   * Get data in CSV format
   * @param {string} dataType - Data type
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  csv(dataType, options = {}) {
    return this._executeTypeOperation('GET', dataType, 'csv', options);
  }

  /**
   * Get field values
   * @param {string} dataType - Data type
   * @param {string} fieldName - Field name
   * @param {Object} options - Request options
   * @returns {*} Response data
   */
  values(dataType, fieldName = null, options = {}) {
    return this._executeFieldOperation('GET', dataType, 'values', fieldName, options);
  }

  /**
   * Get record count
   * @param {string} dataType - Data type
   * @param {string} fieldName - Field name
   * @param {Object} options - Request options
   * @returns {number} Record count
   */
  count(dataType, fieldName = null, options = {}) {
    const result = this._executeFieldOperation('GET', dataType, 'count', fieldName, options);
    return result.count || 0;
  }

  /**
   * Download a dataset
   * @param {string} datasetName - Dataset name
   * @returns {*} Response data
   */
  download(datasetName) {
    return this._execute('GET', `download/${datasetName}`);
  }

  /**
   * Format request options
   * @param {string} method - HTTP method
   * @param {Object} options - Request options
   * @returns {Object} Formatted options
   */
  _formatOptions(method, options) {
    if (options === null) {
      options = {};
    }

    for (const [key, value] of Object.entries(options)) {
      if (typeof value === 'object' && value !== null) {
        if (Array.isArray(value) && method === 'GET') {
          options[key] = value.join(',');
        } else {
          options[key] = JSON.stringify(value);
        }
      }
    }

    return options;
  }
}
