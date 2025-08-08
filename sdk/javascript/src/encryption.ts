/**
 * Encryption utilities for the Zimagi JavaScript SDK
 */

import CryptoJS from 'crypto-js';

/**
 * Base cipher class
 */
export class Cipher {
  /**
   * Get appropriate cipher implementation
   * @param {string|null} key - Encryption key
   * @returns {Object} Cipher instance
   */
  static get(key: string | null = null): NullCipher | AESCipher {
    return key ? new AESCipher(key) : new NullCipher();
  }
}

/**
 * Null cipher that doesn't encrypt data
 */
export class NullCipher {
  key: string | null;

  /**
   * Create a new null cipher
   * @param {string|null} key - Encryption key
   */
  constructor(key: string | null = null) {
    this.key = key;
  }

  /**
   * Encrypt a message (no-op)
   * @param {string} message - Message to encrypt
   * @returns {string} Encrypted message
   */
  encrypt(message: string): string {
    return String(message);
  }

  /**
   * Decrypt a message (no-op)
   * @param {string} ciphertext - Message to decrypt
   * @param {boolean} _decode - Whether to decode
   * @returns {string} Decrypted message
   */
  decrypt(ciphertext: string, _decode: boolean = true): string {
    return ciphertext;
  }
}

/**
 * AES cipher implementation
 */
export class AESCipher {
  binaryMarker: string;
  key: string;

  /**
   * Create a new AES cipher
   * @param {string} key - Encryption key
   */
  constructor(key: string) {
    this.binaryMarker = '<<<<-->BINARY<-->>>>';
    this.key = key;
  }

  /**
   * Encrypt a message
   * @param {string} message - Message to encrypt
   * @returns {string} Encrypted message
   */
  encrypt(message: string): string {
    // AES encryption implementation using crypto-js
    return CryptoJS.AES.encrypt(String(message), this.key).toString();
  }

  /**
   * Decrypt a message
   * @param {string} ciphertext - Message to decrypt
   * @param {boolean} _decode - Whether to decode
   * @returns {string} Decrypted message
   */
  decrypt(ciphertext: string, _decode: boolean = true): string {
    // AES decryption implementation using crypto-js
    const bytes = CryptoJS.AES.decrypt(ciphertext, this.key);
    return bytes.toString(CryptoJS.enc.Utf8);
  }
}
