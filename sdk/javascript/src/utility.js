/**
 * Utility functions for the Zimagi JavaScript SDK
 */

/**
 * Generate service URL from protocol, host, and port
 * @param {string} protocol - HTTP protocol (http/https)
 * @param {string} host - Host name
 * @param {number} port - Port number
 * @returns {string} Service URL
 */
export function getServiceURL(protocol, host, port) {
  return `${protocol}://${host}:${port}/`;
}

/**
 * Normalize value by converting string representations to proper types
 * @param {*} value - Value to normalize
 * @param {boolean} stripQuotes - Whether to strip quotes from strings
 * @param {boolean} parseJSON - Whether to parse JSON strings
 * @returns {*} Normalized value
 */
export function normalizeValue(value, stripQuotes = false, parseJSON = false) {
  if (value !== null && value !== undefined) {
    if (typeof value === 'string') {
      if (stripQuotes) {
        value = value.replace(/^["']|["']$/g, '');
      }

      if (value) {
        if (/^(NONE|None|none|NULL|Null|null)$/.test(value)) {
          value = null;
        } else if (/^(TRUE|True|true)$/.test(value)) {
          value = true;
        } else if (/^(FALSE|False|false)$/.test(value)) {
          value = false;
        } else if (/^\d+$/.test(value)) {
          value = parseInt(value, 10);
        } else if (/^\d*\.\d+$/.test(value)) {
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
      return value.map((item) => normalizeValue(item, stripQuotes, parseJSON));
    } else if (typeof value === 'object' && value !== null) {
      const normalized = {};
      for (const [key, item] of Object.entries(value)) {
        normalized[key] = normalizeValue(item, stripQuotes, parseJSON);
      }
      return normalized;
    }
  }
  return value;
}

/**
 * Format options for HTTP requests
 * @param {string} method - HTTP method
 * @param {Object} options - Options object
 * @returns {Object} Formatted options
 */
export function formatOptions(method, options) {
  if (options === null) {
    options = {};
  }

  const formatted = { ...options };
  for (const [key, value] of Object.entries(formatted)) {
    if (typeof value === 'object' && value !== null) {
      if (Array.isArray(value) && method === 'GET') {
        formatted[key] = value.join(',');
      } else {
        formatted[key] = JSON.stringify(value);
      }
    }
  }

  return formatted;
}

/**
 * Format error message for debugging
 * @param {string|Array} path - API path
 * @param {Error} error - Error object
 * @param {Object} params - Request parameters
 * @returns {string} Formatted error message
 */
export function formatError(path, error, params = null) {
  let paramRender = '';
  if (params) {
    paramRender = JSON.stringify(params, null, 2);
  }

  return `[${Array.isArray(path) ? path.join('/') : path}](${paramRender}) ${error.toString()}`;
}
