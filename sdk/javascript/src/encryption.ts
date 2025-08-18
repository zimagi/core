/**
 * Encryption utilities for the Zimagi JavaScript SDK
 */

import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

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
  batchSize: number;
  key: Buffer;

  /**
   * Create a new AES cipher
   * @param {string} key - Encryption key
   */
  constructor(key: string) {
    this.binaryMarker = '<<<<-->BINARY<-->>>>';
    this.batchSize = 16; // AES block size
    this.key = Buffer.from(key, 'utf-8');
  }

  /**
   * Encrypt a message
   * @param {string} message - Message to encrypt
   * @returns {string} Encrypted message
   */
  encrypt(message: string | Buffer): string {
    const iv = randomBytes(this.batchSize);
    const cipher = createCipheriv('aes-256-ctr', this.key, iv);

    let processedMessage: string;
    if (Buffer.isBuffer(message)) {
      processedMessage = this.binaryMarker + message.toString('hex');
    } else {
      processedMessage = message;
    }

    const encrypted = Buffer.concat([
      cipher.update(Buffer.from(processedMessage, 'utf-8')),
      cipher.final(),
    ]);
    return Buffer.concat([iv, encrypted]).toString('base64');
  }

  /**
   * Decrypt a message
   * @param {string} ciphertext - Message to decrypt
   * @param {boolean} decode - Whether to decode
   * @returns {string} Decrypted message
   */
  decrypt(ciphertext: string, decode = true): string | Buffer {
    const decodedCiphertext = Buffer.from(ciphertext, 'base64');
    const iv = decodedCiphertext.subarray(0, this.batchSize);
    const encrypted = decodedCiphertext.subarray(this.batchSize);

    const decipher = createDecipheriv('aes-256-ctr', this.key, iv);

    const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);

    if (decode) {
      const decryptedString = decrypted.toString('utf-8');
      if (decryptedString.startsWith(this.binaryMarker)) {
        return Buffer.from(decryptedString.substring(this.binaryMarker.length), 'hex');
      }
      return decryptedString;
    }
    return decrypted;
  }
}
