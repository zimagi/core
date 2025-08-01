/**
 * Authentication system for the Zimagi JavaScript SDK
 */

/**
 * Client token authentication handler
 */
export class ClientTokenAuthentication {
  /**
   * Create a new authentication handler
   * @param {string} user - Username
   * @param {string} token - Authentication token
   * @param {Object} client - Client instance
   */
  constructor(user, token, client = null) {
    this.client = client;
    this.user = user;
    this.token = token;
    this.encrypted = false;
  }

  /**
   * Apply authentication to request headers
   * @param {Object} headers - Request headers
   * @returns {Object} Updated headers
   */
  apply(headers) {
    if (!this.encrypted && this.client.cipher) {
      this.token = this.client.cipher.encrypt(this.token).toString('utf-8');
      this.encrypted = true;
    }

    headers['Authorization'] = `Token ${this.user} ${this.token}`;
    return headers;
  }
}
