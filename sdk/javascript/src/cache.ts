/**
 * Caching system for the Zimagi JavaScript SDK
 */

/**
 * Simple in-memory cache implementation
 */
export class Cache {
  /**
   * Create a new cache
   * @param {number} defaultTTL - Default time-to-live in milliseconds
   */
  defaultTTL: number;
  storage: Map<string, { value: any; expiry: number }>;

  constructor(defaultTTL: number = 3600000) {
    // 1 hour default
    this.defaultTTL = defaultTTL;
    this.storage = new Map();
  }

  /**
   * Set a value in the cache
   * @param {string} key - Cache key
   * @param {*} value - Value to cache
   * @param {number} ttl - Time-to-live in milliseconds
   */
  set(key: string, value: any, ttl: number = this.defaultTTL): void {
    const expiry = Date.now() + ttl;
    this.storage.set(key, {
      value: value,
      expiry: expiry,
    });
  }

  /**
   * Get a value from the cache
   * @param {string} key - Cache key
   * @returns {*} Cached value or null if not found/expired
   */
  get(key: string): any {
    const item = this.storage.get(key);
    if (!item) {
      return null;
    }

    if (Date.now() > item.expiry) {
      this.storage.delete(key);
      return null;
    }

    return item.value;
  }

  /**
   * Check if a key exists in the cache
   * @param {string} key - Cache key
   * @returns {boolean} Whether key exists and is not expired
   */
  has(key: string): boolean {
    return this.get(key) !== null;
  }

  /**
   * Delete a key from the cache
   * @param {string} key - Cache key
   */
  delete(key: string): void {
    this.storage.delete(key);
  }

  /**
   * Clear all expired entries
   */
  clearExpired(): void {
    for (const [key, item] of this.storage.entries()) {
      if (Date.now() > item.expiry) {
        this.storage.delete(key);
      }
    }
  }

  /**
   * Clear all entries
   */
  clear(): void {
    this.storage.clear();
  }

  /**
   * Get cache size
   * @returns {number} Number of entries in cache
   */
  size(): number {
    this.clearExpired();
    return this.storage.size;
  }
}

// Default cache instance
export const defaultCache = new Cache();
