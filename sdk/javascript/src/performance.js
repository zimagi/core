/**
 * Performance monitoring utilities for the Zimagi JavaScript SDK
 */

/**
 * Performance metrics collector
 */
export class PerformanceMonitor {
  /**
   * Create a new performance monitor
   */
  constructor() {
    this.metrics = new Map();
    this.timings = new Map();
  }

  /**
   * Start timing an operation
   * @param {string} operation - Operation name
   * @returns {string} Timing ID
   */
  startTiming(operation) {
    const timingId = `${operation}_${Date.now()}_${Math.random()}`;
    this.timings.set(timingId, {
      operation: operation,
      startTime: performance.now(),
      startTimeStamp: new Date(),
    });
    return timingId;
  }

  /**
   * End timing an operation
   * @param {string} timingId - Timing ID
   * @returns {Object} Timing result
   */
  endTiming(timingId) {
    const timing = this.timings.get(timingId);
    if (!timing) {
      throw new Error(`Timing ID ${timingId} not found`);
    }

    const endTime = performance.now();
    const duration = endTime - timing.startTime;

    const result = {
      operation: timing.operation,
      duration: duration,
      startTime: timing.startTimeStamp,
      endTime: new Date(),
      durationFormatted: `${duration.toFixed(2)}ms`,
    };

    this.timings.delete(timingId);

    // Store metrics
    if (!this.metrics.has(timing.operation)) {
      this.metrics.set(timing.operation, []);
    }
    this.metrics.get(timing.operation).push(result);

    return result;
  }

  /**
   * Get metrics for an operation
   * @param {string} operation - Operation name
   * @returns {Array} Metrics array
   */
  getMetrics(operation) {
    return this.metrics.get(operation) || [];
  }

  /**
   * Get average duration for an operation
   * @param {string} operation - Operation name
   * @returns {number} Average duration in milliseconds
   */
  getAverageDuration(operation) {
    const metrics = this.getMetrics(operation);
    if (metrics.length === 0) return 0;

    const total = metrics.reduce((sum, metric) => sum + metric.duration, 0);
    return total / metrics.length;
  }

  /**
   * Get statistics for an operation
   * @param {string} operation - Operation name
   * @returns {Object} Statistics object
   */
  getStatistics(operation) {
    const metrics = this.getMetrics(operation);
    if (metrics.length === 0) return null;

    const durations = metrics.map((metric) => metric.duration);
    const min = Math.min(...durations);
    const max = Math.max(...durations);
    const avg = this.getAverageDuration(operation);

    return {
      operation: operation,
      count: metrics.length,
      min: min,
      max: max,
      average: avg,
      minFormatted: `${min.toFixed(2)}ms`,
      maxFormatted: `${max.toFixed(2)}ms`,
      averageFormatted: `${avg.toFixed(2)}ms`,
    };
  }

  /**
   * Clear all metrics
   */
  clear() {
    this.metrics.clear();
    this.timings.clear();
  }

  /**
   * Get all statistics
   * @returns {Object} All statistics
   */
  getAllStatistics() {
    const stats = {};
    for (const operation of this.metrics.keys()) {
      stats[operation] = this.getStatistics(operation);
    }
    return stats;
  }
}

// Default performance monitor instance
export const defaultMonitor = new PerformanceMonitor();
