/**
 * Exception classes for the Zimagi JavaScript SDK
 */

/**
 * Base exception class for all Zimagi client errors
 */
export class ClientError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ClientError';
  }
}

/**
 * Exception for connection errors
 */
export class ConnectionError extends ClientError {
  constructor(message) {
    super(message);
    this.name = 'ConnectionError';
  }
}

/**
 * Exception for parsing errors
 */
export class ParseError extends ClientError {
  constructor(message) {
    super(message);
    this.name = 'ParseError';
  }
}

/**
 * Exception for response errors
 */
export class ResponseError extends ClientError {
  constructor(message, code = null, result = null) {
    super(message);
    this.name = 'ResponseError';
    this.code = code;
    this.result = result || message;
  }
}

/**
 * Exception for command parsing errors
 */
export class CommandParseError extends Error {
  constructor(message) {
    super(message);
    this.name = 'CommandParseError';
  }
}
