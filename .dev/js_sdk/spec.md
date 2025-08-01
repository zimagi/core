# Zimagi JavaScript SDK Specification

## Overview

This document specifies the JavaScript implementation of the Zimagi SDK, mirroring the functionality and architecture of the existing Python SDK. The JavaScript SDK will provide the same capabilities for interacting with Zimagi services through a consistent API.

## Architecture

### Core Modules

- Client Layer: Main interface for command and data operations
- Transport Layer: HTTP communication with encryption support
- Codec System: Response parsing for different media types
- Authentication: Token-based authentication handling
- Encryption: Data encryption/decryption utilities
- Utility Functions: Helper functions for data processing

### File Structure

sdk/javascript/
├── src/
│ ├── client/
│ │ ├── index.js # Base client classes
│ │ ├── command.js # Command client implementation
│ │ └── data.js # Data client implementation
│ ├── transports/
│ │ ├── base.js # Base transport functionality
│ │ ├── command.js # Command-specific transport
│ │ └── data.js # Data-specific transport
│ ├── codecs/
│ │ ├── base.js # Base codec class
│ │ ├── json.js # JSON codec implementation
│ │ └── csv.js # CSV codec implementation
│ ├── auth.js # Authentication handling
│ ├── encryption.js # Encryption utilities
│ ├── utility.js # Helper functions
│ ├── exceptions.js # Error classes
│ └── index.js # Main entry point
├── package.json
└── README.md

## Client Implementation

### BaseAPIClient

The base client class that provides common functionality for both command and data clients.

class BaseAPIClient {
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

}

\_getServiceURL() {
return `${this.protocol}://${this.host}:${this.port}/`;
}

\_request(method, url, params = null, validateCallback = null) {
if (!this.transport) {
throw new ClientError('Zimagi API client transport not defined');
}

    return this.transport.request(
      method,
      url,
      this.decoders,
      params,
      {
        retries: 20,
        retryWait: 3,
        validateCallback
      }
    );

}

getStatus() {
if (!this.\_status) {
const statusURL = `${this.baseURL}status`;

      const processor = () => {
        return this._request('GET', statusURL);
      };

      this._status = this._wrapAPICall('status', statusURL, processor);
    }
    return this._status;

}

getSchema() {
if (!this.\_schema) {
const schemaGenerator = () => {
const processor = () => {
return this.\_request('GET', this.baseURL);
};
return this.\_wrapAPICall('schema', this.baseURL, processor);
};

      this._schema = this._cacheData(
        `${this.host}.${this.port}`,
        schemaGenerator,
        86400 // 24 hours
      );
    }
    return this._schema;

}

\_wrapAPICall(type, path, processor, params = null) {
try {
return processor();
} catch (error) {
console.debug(`${type} API error: ${this._formatError(path, error, params)}`);
throw error;
}
}

\_formatError(path, error, params = null) {
let paramRender = '';
if (params) {
paramRender = JSON.stringify(params, null, 2);
}

    return `[${Array.isArray(path) ? path.join('/') : path}](${paramRender}) ${error.toString()}`;

}

\_cacheData(cacheName, generatorFunction, cacheLifetime = 3600) {
// Implementation for caching data
}
}

### CommandClient

Client for executing Zimagi commands.

class CommandClient extends BaseAPIClient {
constructor(options = {}) {
super({
port: options.port || 5123,
verifyCert: options.verifyCert !== undefined ? options.verifyCert : false,
decoders: [
new ZimagiJSONCodec(),
new JSONCodec()
],
...options
});

    this.optionsCallback = options.optionsCallback || null;
    this.messageCallback = options.messageCallback || null;
    this.initCommands = options.initCommands !== false;

    this.transport = new CommandHTTPTransport({
      client: this,
      verifyCert: this.verifyCert,
      optionsCallback: this.optionsCallback,
      messageCallback: this.messageCallback
    });

    if (!this.getStatus().encryption) {
      this.cipher = null;
    }

    this.schema = this.getSchema();
    if (this.initCommands) {
      this._initCommands();
    }

}

clone(messageCallback) {
// Deep clone implementation
const clone = JSON.parse(JSON.stringify(this));
clone.messageCallback = messageCallback;
clone.transport = new CommandHTTPTransport({
client: clone,
verifyCert: clone.verifyCert,
optionsCallback: clone.optionsCallback,
messageCallback: messageCallback
});
return clone;
}

\_initCommands() {
this.commands = {};
this.actions = {};

    const collectCommands = (commandInfo, parents) => {
      for (const [commandName, info] of Object.entries(commandInfo)) {
        const apiPath = [...parents, commandName].join('/');
        if (info instanceof Router || info instanceof Action) {
          this.commands[apiPath] = info;
          if (info instanceof Action) {
            this.actions[apiPath] = info;
          }
        } else {
          collectCommands(info, [...parents, commandName]);
        }
      }
    };

    collectCommands(this.schema, []);

}

\_normalizePath(commandName) {
return commandName.replace(/(\s+|\.)/g, '/');
}

setMessageCallback(messageCallback) {
this.messageCallback = messageCallback;
this.transport = new CommandHTTPTransport({
client: this,
verifyCert: this.verifyCert,
optionsCallback: this.optionsCallback,
messageCallback: messageCallback
});
}

execute(commandName, options = {}) {
const commandPath = this.\_normalizePath(commandName);
const command = this.\_lookup(commandPath);
const commandOptions = this.\_formatOptions('POST', options);

    const validate = (url, params) => {
      this._validate(command, params);
    };

    const processor = () => {
      return this._request('POST', command.url, commandOptions, validate);
    };

    return this._wrapAPICall('command', commandPath, processor, commandOptions);

}

extend(remote, reference, provider = null, fields = {}) {
fields.reference = reference;

    const options = {
      remote: remote,
      moduleFields: fields
    };

    if (provider) {
      options.moduleProviderName = provider;
    }

    return this.execute('module/add', options);

}

runTask(moduleKey, taskName, config = null, options = {}) {
return this.execute('task', {
...options,
moduleKey: moduleKey,
taskKey: taskName,
taskFields: config || {}
});
}

runProfile(moduleKey, profileKey, config = null, components = null, options = {}) {
return this.execute('run', {
...options,
moduleKey: moduleKey,
profileKey: profileKey,
profileConfigFields: config || {},
profileComponents: components || []
});
}

destroyProfile(moduleKey, profileKey, config = null, components = null, options = {}) {
return this.execute('destroy', {
...options,
moduleKey: moduleKey,
profileKey: profileKey,
profileConfigFields: config || {},
profileComponents: components || []
});
}

runImports(names = null, tags = null, options = {}) {
return this.execute('import', {
...options,
importNames: names || [],
tags: tags || []
});
}

runCalculations(names = null, tags = null, options = {}) {
return this.execute('calculate', {
...options,
calculationNames: names || [],
tags: tags || []
});
}

\_lookup(commandName) {
let node = this.schema;
let found = true;

    for (const key of commandName.split('/')) {
      if (node[key] !== undefined) {
        node = node[key];
      } else {
        found = false;
        break;
      }
    }

    if (!found || !(node instanceof Action)) {
      if (!this.initCommands) {
        this._initCommands();
      }

      const relatedActions = [];
      for (const otherAction of Object.keys(this.actions)) {
        if (otherAction.includes(commandName)) {
          relatedActions.push(otherAction);
        }
      }

      throw new ParseError(
        `Command ${commandName} does not exist. Try one of: ${relatedActions.join(', ')}`
      );
    }
    return node;

}

\_validate(command, options) {
const provided = new Set(Object.keys(options));
const required = new Set(command.fields.filter(field => field.required).map(field => field.name));
const optional = new Set(command.fields.filter(field => !field.required).map(field => field.name));
const errors = {};

    const missing = [...required].filter(item => !provided.has(item));
    for (const item of missing) {
      errors[item] = 'Parameter is required';
    }

    const unexpected = [...provided].filter(item => !optional.has(item) && !required.has(item));
    for (const item of unexpected) {
      errors[item] = 'Unknown parameter';
    }

    if (Object.keys(errors).length > 0) {
      throw new ParseError(errors);
    }

}

\_formatOptions(method, options) {
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

### DataClient

Client for data operations.

class DataClient extends BaseAPIClient {
constructor(options = {}) {
super({
port: options.port || 5323,
verifyCert: options.verifyCert !== undefined ? options.verifyCert : false,
decoders: [
new OpenAPIJSONCodec(),
new CSVCodec(),
new JSONCodec()
],
...options
});

    this.transport = new DataHTTPTransport({
      client: this,
      verifyCert: options.verifyCert,
      optionsCallback: options.optionsCallback
    });

    if (!this.getStatus().encryption) {
      this.cipher = null;
    }

    this.schema = this.getSchema();
    this._dataInfo = this.schema['x-data'] || {};

}

getPaths() {
return this.schema.paths;
}

getPath(path) {
const normalizedPath = `/${path.replace(/^\/+|\/+$/g, '')}/`;
return this.getPaths()[normalizedPath];
}

getIdField(dataType) {
return this.\_dataInfo[dataType]?.id || null;
}

getKeyField(dataType) {
return this.\_dataInfo[dataType]?.key || null;
}

getSystemFields(dataType) {
return this.\_dataInfo[dataType]?.system || [];
}

getUniqueFields(dataType) {
return this.\_dataInfo[dataType]?.unique || [];
}

getDynamicFields(dataType) {
return this.\_dataInfo[dataType]?.dynamic || [];
}

getAtomicFields(dataType) {
return this.\_dataInfo[dataType]?.atomic || [];
}

getScopeFields(dataType) {
return this.\_dataInfo[dataType]?.scope || {};
}

getRelationFields(dataType) {
return this.\_dataInfo[dataType]?.relations || {};
}

getReverseFields(dataType) {
return this.\_dataInfo[dataType]?.reverse || {};
}

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

getSchema(full = false) {
if (full || !this.\_schema) {
const processor = () => {
const schema = this.\_request('GET', this.baseURL);

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

\_execute(method, path, options = null) {
const url = `${this.baseURL.replace(/\/+$/, '')}/${path.replace(/^\/+|\/+$/g, '')}`.replace(/\/+$/, '');

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

\_executeTypeOperation(method, dataType, op, options) {
const path = op === null ? dataType : `${dataType}/${op}`;
return this.\_execute(method, path, options);
}

\_executeKeyOperation(method, dataType, op, key, options) {
const path = op === null ? `${dataType}/${key}` : `${dataType}/${key}/${op}`;
return this.\_execute(method, path, options);
}

\_executeFieldOperation(method, dataType, op, fieldName, options) {
if (!fieldName) {
fieldName = this.getIdField(dataType);
}

    const path = `${dataType}/${op}/${fieldName}`;
    return this._execute(method, path, options);

}

create(dataType, fields = {}) {
return this.\_executeTypeOperation('POST', dataType, null, fields);
}

update(dataType, id, fields = {}) {
return this.\_executeKeyOperation('PUT', dataType, null, id, fields);
}

delete(dataType, id) {
return this.\_executeKeyOperation('DELETE', dataType, null, id, {});
}

get(dataType, id, options = {}) {
return this.\_executeKeyOperation('GET', dataType, null, id, options);
}

getByKey(dataType, key, options = {}) {
const results = this.\_executeTypeOperation(
'GET',
dataType,
null,
{
[this.getKeyField(dataType)]: key,
...this.setScope(dataType, options)
}
);

    if (results.count === null) {
      throw new ResponseError(`Instance ${dataType} ${key}: ${results}`);
    } else if (results.count === 0) {
      throw new ResponseError(`Instance ${dataType} ${key}: not found`);
    } else if (results.count > 1) {
      throw new ResponseError(`Instance ${dataType} ${key}: too many found`);
    }

    return results.results[0];

}

list(dataType, options = {}) {
return this.\_executeTypeOperation('GET', dataType, null, options);
}

json(dataType, options = {}) {
return this.\_executeTypeOperation('GET', dataType, 'json', options);
}

csv(dataType, options = {}) {
return this.\_executeTypeOperation('GET', dataType, 'csv', options);
}

values(dataType, fieldName = null, options = {}) {
return this.\_executeFieldOperation('GET', dataType, 'values', fieldName, options);
}

count(dataType, fieldName = null, options = {}) {
const result = this.\_executeFieldOperation('GET', dataType, 'count', fieldName, options);
return result.count || 0;
}

download(datasetName) {
return this.\_execute('GET', `download/${datasetName}`);
}

\_formatOptions(method, options) {
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

## Transport Implementation

### BaseTransport

Base class for all transport implementations.

class BaseTransport {
constructor(options = {}) {
this.client = options.client || null;
this.verifyCert = options.verifyCert || false;
this.optionsCallback = options.optionsCallback || null;
this.requestCallback = options.requestCallback || null;
this.responseCallback = options.responseCallback || null;
}

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
        'accept': acceptMediaTypes.join(', '),
        'user-agent': 'zimagi-javascript'
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

      return await this.handleRequest(method, url, new URL(url).pathname, headers, params, decoders);
    } catch (error) {
      console.debug(`Request ${url} connection error: ${error}`);

      if (options.tries > 0) {
        await this._sleep(options.retryWait * 1000);
        return await this.request(method, url, decoders, params, {
          ...options,
          tries: options.tries - 1
        });
      }

      throw new ConnectionError(connectionErrorMessage);
    }

}

async handleRequest(method, url, path, headers, params, decoders) {
throw new Error('Method handleRequest(...) must be overridden in all subclasses');
}

async requestPage(url, headers, params, decoders, options = {}) {
const encrypted = options.encrypted !== false;
const useAuth = options.useAuth !== false;
const disableCallbacks = options.disableCallbacks || false;

    const [request, response] = await this._request(
      'GET',
      url,
      {
        headers: headers,
        params: params,
        encrypted: encrypted,
        stream: false,
        useAuth: useAuth,
        disableCallbacks: disableCallbacks
      }
    );

    console.debug(`Page ${url} request headers: ${JSON.stringify(headers)}`);

    if (response.status >= 400) {
      const error = this._formatResponseError(response, encrypted ? this.client.cipher : null);
      throw new ResponseError(error.message, response.status, error.data);
    }

    return this.decodeMessage(request, response, decoders, null, encrypted, disableCallbacks);

}

async \_request(method, url, options = {}) {
const {
headers = {},
params = null,
encrypted = true,
stream = false,
useAuth = true,
disableCallbacks = false
} = options;

    // Create request object
    const requestHeaders = { ...headers };

    if (useAuth && this.client.auth) {
      // Apply authentication
      this.client.auth(requestHeaders);
    }

    let body = null;
    if (params) {
      const parameterName = ['POST', 'PUT'].includes(method) ? 'data' : 'params';
      const processedParams = encrypted ? this._encryptParams(params) : params;

      if (parameterName === 'data') {
        body = typeof processedParams === 'string' ? processedParams : JSON.stringify(processedParams);
        requestHeaders['Content-Type'] = 'application/json';
      } else {
        // Handle query parameters
        const urlObj = new URL(url);
        for (const [key, value] of Object.entries(processedParams)) {
          urlObj.searchParams.append(key, value);
        }
        url = urlObj.toString();
      }
    }

    const fetchOptions = {
      method: method,
      headers: requestHeaders,
      body: body
    };

    if (!disableCallbacks && this.requestCallback && typeof this.requestCallback === 'function') {
      this.requestCallback(fetchOptions);
    }

    const response = await fetch(url, fetchOptions);

    return [{ url, method, headers: requestHeaders }, response];

}

\_encryptParams(params) {
if (!this.client.cipher) {
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

decodeMessage(request, response, decoders, message = null, decrypt = true, disableCallbacks = false) {
let content = message !== null ? message : null;

    // Get response content
    if (!content && response.body) {
      content = response.body;
    }

    let data = null;

    if (content) {
      const contentType = response.headers.get('content-type') || '';
      const codec = this._getDecoder(contentType.split(';')[0].trim().toLowerCase(), decoders);

      if (decrypt && this.client.cipher) {
        content = this.client.cipher.decrypt(content);
      }

      data = codec.decode(content, {
        baseURL: response.url,
        contentType: contentType
      });

      if (!disableCallbacks && this.responseCallback && typeof this.responseCallback === 'function') {
        this.responseCallback(request, response, data);
      }
    }

    return data;

}

\_getDecoder(contentType, decoders) {
for (const codec of decoders) {
if (codec.mediaTypes.includes(contentType)) {
return codec;
}
}

    throw new ClientError(`Unsupported media in Content-Type header '${contentType}'`);

}

\_formatResponseError(response, cipher = null) {
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
        data: errorData
      };
    } catch (error) {
      return {
        message: `Error ${response.status}: ${response.statusText}: ${message}`,
        data: message
      };
    }

}

\_sleep(ms) {
return new Promise(resolve => setTimeout(resolve, ms));
}
}

### CommandHTTPTransport

Transport for command operations.

class CommandHTTPTransport extends BaseTransport {
constructor(options = {}) {
super(options);
this.\_messageCallback = options.messageCallback || null;
}

async handleRequest(method, url, path, headers, params, decoders) {
if (path.match(/^\/status\/?$/)) {
return await this.requestPage(url, headers, null, decoders, {
encrypted: false,
useAuth: false,
disableCallbacks: true
});
}

    if (!path || path === '/' || path === '') {
      return await this.requestPage(url, headers, null, decoders, {
        encrypted: false,
        useAuth: true,
        disableCallbacks: true
      });
    }

    return await this.requestCommand(url, headers, params, decoders);

}

async requestCommand(url, headers, params, decoders) {
const commandResponse = new CommandResponse();

    const [request, requestResponse] = await this._request(
      'POST',
      url,
      {
        stream: true,
        headers: headers,
        params: params,
        encrypted: true,
        useAuth: true
      }
    );

    console.debug(`Stream ${url} request headers: ${JSON.stringify(headers)}`);

    if (requestResponse.status >= 400) {
      const error = this._formatResponseError(requestResponse, this.client.cipher);
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
            const message = Message.get(messageData, this.client.cipher);

            if (this._messageCallback && typeof this._messageCallback === 'function') {
              this._messageCallback(message);
            }

            commandResponse.add(message);
          }
        }
      }
    } catch (error) {
      console.debug(`Stream ${url} error response headers: ${JSON.stringify(Object.fromEntries(requestResponse.headers.entries()))}`);
      console.debug(`Stream ${url} error status code: ${requestResponse.status}`);
      throw error;
    }

    if (commandResponse.error) {
      throw new ResponseError(commandResponse.errorMessage(), requestResponse.status);
    }

    return commandResponse;

}
}

### DataHTTPTransport

Transport for data operations.

class DataHTTPTransport extends BaseTransport {
async handleRequest(method, url, path, headers, params, decoders) {
if (method === 'GET') {
if (path.match(/^\/status\/?$/)) {
return await this.requestPage(url, headers, null, decoders, {
encrypted: false,
useAuth: false,
disableCallbacks: true
});
}

      if (!path || path === '/' || path.startsWith('/schema/')) {
        return await this.requestPage(url, headers, null, decoders, {
          encrypted: false,
          useAuth: true,
          disableCallbacks: true
        });
      }

      return await this.requestPage(url, headers, params, decoders, {
        encrypted: true,
        useAuth: true
      });
    }

    return await this.updateData(method, url, headers, params, decoders);

}

async updateData(method, url, headers, params, decoders, encrypted = true) {
const [request, response] = await this.\_request(
method,
url,
{
headers: {
'Content-Type': 'application/json',
...headers
},
params: JSON.stringify(params),
encrypted: encrypted,
useAuth: true
}
);

    console.debug(`${method} ${url} request headers: ${JSON.stringify(headers)}`);

    if (response.status >= 400) {
      const error = this._formatResponseError(response, encrypted ? this.client.cipher : null);
      throw new ResponseError(error.message, response.status, error.data);
    }

    return this.decodeMessage(request, response, decoders, null, encrypted);

}
}

## Codec System

### Base Codec

class BaseCodec {
constructor() {
this.mediaTypes = [];
}

decode(bytestring, options = {}) {
throw new Error('Method decode(...) must be implemented in subclasses');
}
}

### JSON Codec

class JSONCodec extends BaseCodec {
constructor() {
super();
this.mediaTypes = ['application/json'];
}

decode(bytestring, options = {}) {
const convert = (data) => {
if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
return new RecursiveCollection(data);
} else if (Array.isArray(data)) {
return data.map((value, index) => {
data[index] = convert(value);
});
}
return data;
};

    try {
      const data = JSON.parse(bytestring.toString());
      return convert(data);
    } catch (error) {
      throw new ParseError(`Malformed JSON: ${error.message}`);
    }

}
}

### CSV Codec

class CSVCodec extends BaseCodec {
constructor() {
super();
this.mediaTypes = ['text/csv'];
}

decode(bytestring, options = {}) {
try {
const csvData = this.\_getCSVData(bytestring.toString());
let data;

      if (csvData.length > 0) {
        // Convert to DataFrame-like structure
        const headers = csvData[0];
        const rows = csvData.slice(1);

        data = {
          headers: headers,
          rows: rows,
          count: rows.length,
          results: rows.map(row => {
            const obj = {};
            headers.forEach((header, index) => {
              obj[header] = this._normalizeValue(row[index]);
            });
            return obj;
          })
        };
      } else {
        data = {
          headers: [],
          rows: [],
          count: 0,
          results: []
        };
      }

      return data;
    } catch (error) {
      throw new ParseError(`Malformed CSV: ${error.message}`);
    }

}

\_getCSVData(csvString) {
const csvData = [];
const lines = csvString.trim().split('\n');

    for (const csvLine of lines) {
      let line = csvLine.trim().replace(/^["']|["']$/g, '');
      if (line) {
        const values = line.split(',').map(value => {
          return this._normalizeValue(value.trim().replace(/^["']|["']$/g, ''));
        });
        csvData.push(values);
      }
    }

    return csvData;

}

\_normalizeValue(value) {
if (value === null || value === undefined) {
return null;
}

    if (typeof value === 'string') {
      if (value.match(/^(NONE|None|none|NULL|Null|null)$/)) {
        return null;
      } else if (value.match(/^(TRUE|True|true)$/)) {
        return true;
      } else if (value.match(/^(FALSE|False|false)$/)) {
        return false;
      } else if (value.match(/^\d+$/)) {
        return parseInt(value, 10);
      } else if (value.match(/^\d*\.\d+$/)) {
        return parseFloat(value);
      }
    }

    return value;

}
}

### Zimagi JSON Codec

class ZimagiJSONCodec extends BaseCodec {
constructor() {
super();
this.mediaTypes = ['application/vnd.zimagi+json', 'application/x-zimagi+json'];
}

decode(bytestring, options = {}) {
const baseURL = options.baseURL || '';

    try {
      const data = JSON.parse(bytestring.toString());
      const document = this._convertToSchema(data, baseURL);

      if (!(document instanceof Root || document instanceof Error)) {
        throw new CommandParseError('Top level node should be a root or error.');
      }

      return document;
    } catch (error) {
      throw new ParseError(`Malformed JSON. ${error.message}`);
    }

}

\_convertToSchema(data, baseURL = '') {
if (typeof data === 'object' && data !== null && data.\_type === 'root') {
const meta = data.\_meta || {};
const url = new URL(meta.url || '', baseURL).href;

      return new Root({
        commands: this._getDocumentContent(data, url),
        url: url,
        title: meta.title || '',
        description: meta.description || '',
        mediaType: 'application/vnd.zimagi+json'
      });
    }

    if (typeof data === 'object' && data !== null && data._type === 'error') {
      const meta = data._meta || {};
      return new Error({
        title: meta.title || '',
        content: this._getDocumentContent(data, baseURL)
      });
    }

    if (typeof data === 'object' && data !== null && data._type === 'router') {
      const meta = data._meta || {};
      return new Router({
        commands: this._getDocumentContent(data, baseURL),
        name: meta.name || '',
        overview: meta.overview || '',
        description: meta.description || '',
        epilog: data.epilog || '',
        priority: meta.priority !== undefined ? meta.priority : 1,
        resource: meta.resource || ''
      });
    }

    if (typeof data === 'object' && data !== null && data._type === 'action') {
      return new Action({
        url: new URL(data.url || '', baseURL).href,
        name: data.name || '',
        overview: data.overview || '',
        description: data.description || '',
        epilog: data.epilog || '',
        priority: data.priority !== undefined ? data.priority : 1,
        resource: data.resource || '',
        confirm: !!data.confirm,
        fields: Array.isArray(data.fields) ? data.fields.map(item => {
          if (typeof item === 'object' && item !== null) {
            return new Field({
              method: item.method || '',
              name: item.name || '',
              type: item.type || '',
              argument: item.argument || '',
              config: item.config || '',
              description: item.description || '',
              valueLabel: item.value_label || '',
              system: !!item.system,
              required: !!item.required,
              default: item.default,
              choices: Array.isArray(item.choices) ? item.choices : [],
              tags: Array.isArray(item.tags) ? item.tags : []
            });
          }
          return null;
        }).filter(item => item !== null) : []
      });
    }

    if (typeof data === 'object' && data !== null) {
      return new Object(this._getDocumentContent(data, baseURL));
    }

    if (Array.isArray(data)) {
      return new Array(data.map(item => this._convertToSchema(item, baseURL)));
    }

    return data;

}

\_getDocumentContent(item, baseURL = '') {
const content = {};
for (const [key, value] of Object.entries(item)) {
if (key !== '\_type' && key !== '\_meta') {
const unescapedKey = this.\_unescapeKey(key);
content[unescapedKey] = this.\_convertToSchema(value, baseURL);
}
}
return content;
}

\_unescapeKey(string) {
if (string.startsWith('\_\_') && ['type', 'meta'].includes(string.substring(2))) {
return string.substring(1);
}
return string;
}
}

### OpenAPI JSON Codec

class OpenAPIJSONCodec extends BaseCodec {
constructor() {
super();
this.mediaTypes = ['application/openapi+json', 'application/vnd.oai.openapi+json'];
}

decode(bytestring, options = {}) {
try {
const data = JSON.parse(bytestring.toString());
return data;
} catch (error) {
throw new ParseError(`Malformed JSON: ${error.message}`);
}
}
}

## Schema Definitions

### Root

class Root extends Map {
constructor(options = {}) {
const commands = options.commands || {};
super(Object.entries(commands));

    this.url = options.url || '';
    this.title = options.title || '';
    this.description = options.description || '';
    this.mediaType = options.mediaType || '';

}

get data() {
const result = {};
for (const [key, value] of this.entries()) {
if (!(value instanceof Router || value instanceof Action)) {
result[key] = value;
}
}
return result;
}

get commands() {
const result = {};
for (const [key, value] of this.entries()) {
if (value instanceof Router || value instanceof Action) {
result[key] = value;
}
}
return result;
}

get routers() {
const result = {};
for (const [key, value] of this.entries()) {
if (value instanceof Router) {
result[key] = value;
}
}
return result;
}

get actions() {
const result = {};
for (const [key, value] of this.entries()) {
if (value instanceof Action) {
result[key] = value;
}
}
return result;
}
}

### Router

class Router extends Map {
constructor(options = {}) {
const commands = options.commands || {};
super(Object.entries(commands));

    this.name = options.name || '';
    this.overview = options.overview || '';
    this.description = options.description || '';
    this.epilog = options.epilog || '';
    this.priority = options.priority !== undefined ? options.priority : 1;
    this.resource = options.resource || '';

}

get data() {
const result = {};
for (const [key, value] of this.entries()) {
if (!(value instanceof Router || value instanceof Action)) {
result[key] = value;
}
}
return result;
}

get commands() {
const result = {};
for (const [key, value] of this.entries()) {
if (value instanceof Router || value instanceof Action) {
result[key] = value;
}
}
return result;
}

get routers() {
const result = {};
for (const [key, value] of this.entries()) {
if (value instanceof Router) {
result[key] = value;
}
}
return result;
}

get actions() {
const result = {};
for (const [key, value] of this.entries()) {
if (value instanceof Action) {
result[key] = value;
}
}
return result;
}
}

### Action

class Action {
constructor(options = {}) {
this.url = options.url || '';
this.name = options.name || '';
this.overview = options.overview || '';
this.description = options.description || '';
this.epilog = options.epilog || '';
this.priority = options.priority !== undefined ? options.priority : 1;
this.resource = options.resource || '';
this.confirm = !!options.confirm;
this.fields = Array.isArray(options.fields) ? options.fields : [];
}
}

### Field

class Field {
constructor(options = {}) {
this.method = options.method || '';
this.name = options.name || '';
this.type = options.type || '';
this.argument = options.argument || '';
this.config = options.config || '';
this.description = options.description || '';
this.valueLabel = options.valueLabel || '';
this.required = !!options.required;
this.system = !!options.system;
this.default = options.default;
this.choices = Array.isArray(options.choices) ? options.choices : [];
this.tags = Array.isArray(options.tags) ? options.tags : [];
}
}

### Error

class Error extends Map {
constructor(options = {}) {
const content = options.content || {};
super(Object.entries(content));

    this.title = options.title || '';

}

getMessages() {
const messages = [];
for (const [, value] of this.entries()) {
if (value instanceof Array) {
messages.push(...value.filter(item => typeof item === 'string'));
}
}
return messages;
}
}

### Object

class Object extends Map {
constructor(items = {}) {
super(Object.entries(items));
}
}

### Array

class Array extends Array {
constructor(items = []) {
super(...items);
}
}

## Authentication

### ClientTokenAuthentication

class ClientTokenAuthentication {
constructor(user, token, client = null) {
this.client = client;
this.user = user;
this.token = token;
this.encrypted = false;
}

apply(headers) {
if (!this.encrypted && this.client.cipher) {
this.token = this.client.cipher.encrypt(this.token).toString('utf-8');
this.encrypted = true;
}

    headers['Authorization'] = `Token ${this.user} ${this.token}`;
    return headers;

}
}

## Encryption

### Cipher

class Cipher {
static get(key = null) {
return key ? new AESCipher(key) : new NullCipher();
}
}

### NullCipher

class NullCipher {
constructor(key = null) {
this.key = key;
}

encrypt(message) {
return Buffer.from(String(message), 'utf-8');
}

decrypt(ciphertext, decode = true) {
if (decode && (ciphertext instanceof Buffer || ciphertext instanceof Uint8Array)) {
return ciphertext.toString('utf-8');
}
return ciphertext;
}
}

### AESCipher

class AESCipher {
constructor(key) {
this.binaryMarker = '<<<<-->BINARY<-->>>>';
this.key = key;
}

encrypt(message) {
// AES encryption implementation
// This would use a library like crypto-js or the Web Crypto API
throw new Error('AES encryption not yet implemented');
}

decrypt(ciphertext, decode = true) {
// AES decryption implementation
// This would use a library like crypto-js or the Web Crypto API
throw new Error('AES decryption not yet implemented');
}
}

## Messages

### Base Message

class Message {
static get(data, cipher = null) {
let message = data;
if (cipher) {
message = cipher.decrypt(data.package, false);
}

    const messageData = typeof message === 'string' || message instanceof Buffer ?
      JSON.parse(message.toString()) : data.package;

    const MsgClass = messageTypes[messageData.type] || Message;
    const msg = new MsgClass();
    msg.load(messageData);
    return msg;

}

constructor(options = {}) {
this.type = this.constructor.name;
this.name = options.name || null;
this.prefix = options.prefix || '';
this.message = options.message || '';
this.silent = !!options.silent;
this.system = !!options.system;
}

load(data) {
for (const [field, value] of Object.entries(data)) {
if (field !== 'type') {
this[field] = value;
}
}
}

isError() {
return false;
}

render() {
const data = {
type: this.type,
message: this.message
};

    if (this.name) {
      data.name = this.name;
    }

    if (this.prefix) {
      data.prefix = this.prefix;
    }

    if (this.silent) {
      data.silent = this.silent;
    }

    if (this.system) {
      data.system = this.system;
    }

    return data;

}

toJSON() {
return JSON.stringify(this.render());
}

format(options = {}) {
const { debug = false, width = null } = options;
return `${this.prefix}${this.message}`;
}

display(options = {}) {
const { debug = false, width = null } = options;
if (!this.silent) {
console.log(this.format({ debug, width }));
}
}
}

### StatusMessage

class StatusMessage extends Message {
constructor(success = true) {
super({ message: success });
}

format(options = {}) {
const { debug = false, disableColor = false, width = null } = options;
return `Success: ${this.message}`;
}

display(options = {}) {
// No display for status messages
}
}

### DataMessage

class DataMessage extends Message {
constructor(options = {}) {
super(options);
this.data = options.data;
}

load(data) {
super.load(data);
this.data = this.\_normalizeValue(this.data, true, true);
}

render() {
const result = super.render();
result.data = this.data;
return result;
}

format(options = {}) {
const { debug = false, width = null } = options;
let data = this.data;

    if (typeof data === 'object' && data !== null) {
      data = `\n${JSON.stringify(data, null, 2)}`;
    }

    return `${this.message}: ${data}`;

}

\_normalizeValue(value, stripQuotes = false, parseJSON = false) {
// Implementation of value normalization
return value;
}
}

### ErrorMessage

class ErrorMessage extends Message {
constructor(options = {}) {
super(options);
this.traceback = options.traceback || null;
}

isError() {
return true;
}

render() {
const result = super.render();
result.traceback = this.traceback;
return result;
}

format(options = {}) {
const { debug = false, width = null } = options;

    if (debug && this.traceback) {
      const traceback = Array.isArray(this.traceback) ?
        this.traceback.map(item => item.trim()).join('\n') : this.traceback;
      return `\n${this.prefix}** ${this.message}\n\n> ${traceback}\n`;
    }

    return `${this.prefix}** ${this.message}`;

}

display(options = {}) {
const { debug = false, width = null } = options;
if (!this.silent && this.message) {
console.error(this.format({ debug, width }));
}
}
}

## Response Handling

### CommandResponse

class CommandResponse {
constructor() {
this.aborted = true;
this.messages = [];
this.named = {};
this.errors = [];
}

[Symbol.iterator]() {
return this.messages[Symbol.iterator]();
}

get activeUser() {
return this.getNamedData('active_user');
}

get logKey() {
return this.getNamedData('log_key');
}

add(messages) {
if (!Array.isArray(messages)) {
messages = [messages];
}

    for (const message of messages) {
      if (message instanceof StatusMessage) {
        this.aborted = !message.message;
      } else {
        this.messages.push(message);
        if (message.name) {
          this.named[message.name] = message;
        }
        if (message.isError()) {
          this.errors.push(message);
        }
      }
    }

}

get error() {
return this.aborted;
}

errorMessage() {
return this.errors.map(message => message.format()).join('\n\n');
}

getNamedData(name) {
const message = this.named[name];
if (message) {
try {
return message.data;
} catch (error) {
return message.message;
}
}
return null;
}
}

## Utility Functions

### Data Processing

class Utility {
static getServiceURL(protocol, host, port) {
return `${protocol}://${host}:${port}/`;
}

static wrapAPICall(type, path, processor, params = null) {
try {
return processor();
} catch (error) {
console.debug(`${type} API error: ${this.formatError(path, error, params)}`);
throw error;
}
}

static normalizeValue(value, stripQuotes = false, parseJSON = false) {
if (value !== null && value !== undefined) {
if (typeof value === 'string') {
if (stripQuotes) {
value = value.replace(/^["']|["']$/g, '');
}

        if (value) {
          if (value.match(/^(NONE|None|none|NULL|Null|null)$/)) {
            value = null;
          } else if (value.match(/^(TRUE|True|true)$/)) {
            value = true;
          } else if (value.match(/^(FALSE|False|false)$/)) {
            value = false;
          } else if (value.match(/^\d+$/)) {
            value = parseInt(value, 10);
          } else if (value.match(/^\d*\.\d+$/)) {
            value = parseFloat(value);
          } else if (parseJSON && value[0] === '[' && value[value.length - 1] === ']') {
            try {
              value = JSON.parse(value);
            } catch (error) {
              // Ignore parsing errors
            }
          } else if (parseJSON && value[0] === '{' && value[value.length - 1] === '}') {
            try {
              value = JSON.parse(value);
            } catch (error) {
              // Ignore parsing errors
            }
          }
        }
      } else if (Array.isArray(value)) {
        value = value.map(item => this.normalizeValue(item, stripQuotes, parseJSON));
      } else if (typeof value === 'object' && value !== null) {
        for (const [key, item] of Object.entries(value)) {
          value[key] = this.normalizeValue(item, stripQuotes, parseJSON);
        }
      }
    }
    return value;

}

static formatOptions(method, options) {
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

static formatError(path, error, params = null) {
let paramRender = '';
if (params) {
paramRender = JSON.stringify(params, null, 2);
}

    return `[${Array.isArray(path) ? path.join('/') : path}](${paramRender}) ${error.toString()}`;

}

static formatResponseError(response, cipher = null) {
let message = cipher ? cipher.decrypt(response.body).toString('utf-8') : response.statusText;

    try {
      const errorData = JSON.parse(message);
      const errorRender = JSON.stringify(errorData, null, 2);
      return {
        message: `Error ${response.status}: ${response.statusText}: ${errorRender}`,
        data: errorData
      };
    } catch (error) {
      return {
        message: `Error ${response.status}: ${response.statusText}: ${message}`,
        data: message
      };
    }

}
}

## Exception Classes

### Base Exceptions

class ClientError extends Error {
constructor(message) {
super(message);
this.name = 'ClientError';
}
}

class ConnectionError extends ClientError {
constructor(message) {
super(message);
this.name = 'ConnectionError';
}
}

class ParseError extends ClientError {
constructor(message) {
super(message);
this.name = 'ParseError';
}
}

class ResponseError extends ClientError {
constructor(message, code = null, result = null) {
super(message);
this.name = 'ResponseError';
this.code = code;
this.result = result || message;
}
}

class CommandParseError extends Error {
constructor(message) {
super(message);
this.name = 'CommandParseError';
}
}

## Usage Examples

### Command Client Usage

// Initialize command client
const commandClient = new CommandClient({
host: 'localhost',
port: 5123,
user: 'admin',
token: 'your-token',
encryptionKey: 'your-encryption-key'
});

// Execute a command
const response = await commandClient.execute('module/add', {
remote: 'https://example.com/module',
reference: 'module-reference',
moduleFields: {
name: 'My Module',
version: '1.0.0'
}
});

// Run a task
await commandClient.runTask('module-key', 'task-name', {
param1: 'value1',
param2: 'value2'
});

// Extend with a module
await commandClient.extend('https://example.com/module', 'reference', 'provider', {
field1: 'value1',
field2: 'value2'
});

### Data Client Usage

// Initialize data client
const dataClient = new DataClient({
host: 'localhost',
port: 5323,
user: 'admin',
token: 'your-token',
encryptionKey: 'your-encryption-key'
});

// Create a record
const newRecord = await dataClient.create('users', {
name: 'John Doe',
email: 'john@example.com'
});

// Get a record by ID
const user = await dataClient.get('users', '123');

// Get a record by key
const userByKey = await dataClient.getByKey('users', 'john-doe');

// List records
const users = await dataClient.list('users', {
page: 1,
page_size: 10
});

// Update a record
await dataClient.update('users', '123', {
name: 'Jane Doe'
});

// Delete a record
await dataClient.delete('users', '123');

// Get data in CSV format
const csvData = await dataClient.csv('users');

// Get data values
const values = await dataClient.values('users', 'name');

// Get count
const count = await dataClient.count('users');
