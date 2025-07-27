# Zimagi Cache Systems Directory

## Overview

The `app/systems/cache` directory contains Python modules that implement the caching functionality for the Zimagi platform. These modules provide HTTP-level caching middleware that enables efficient response caching for API endpoints, reducing server load and improving response times for frequently accessed resources.

This directory plays an architectural role by centralizing caching operations and providing a consistent interface for HTTP response caching across the Zimagi platform's API services. The modules here are consumed by:

- **Developers** working on API performance optimization
- **System administrators** managing cache configurations
- **AI models** analyzing and generating performance optimization components

## Directory Contents

### Files

| File          | Purpose                                                                                                | Format |
| ------------- | ------------------------------------------------------------------------------------------------------ | ------ |
| middleware.py | Implements HTTP caching middleware for Django responses with cache key generation and cache management | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/systems` directory which contains integrated systems implementing core application components
- **API Systems**: Connects to `app/systems/api` for API response caching
- **Settings**: Integrates with cache configurations defined in `app/settings` for cache backend and timeout settings
- **Data Models**: Works with the cache data model in `app/data/cache` for cache entry tracking

## Key Concepts and Patterns

### Caching Middleware

The caching system implements HTTP-level response caching through Django middleware:

- **FetchCacheMiddleware**: Intercepts incoming requests to check for cached responses
- **UpdateCacheMiddleware**: Stores outgoing responses in the cache when appropriate
- Cache key generation based on request method, URI, and authorization context
- Support for cache bypass using specific query parameters

### Cache Key Generation

Cache keys are generated using a combination of:

- Request method (GET, POST, etc.)
- Full request URI including query parameters
- Authorization header (or anonymous user identifier)
- Configurable cache key prefix from settings

This ensures that cached responses are properly isolated by user context and request parameters.

### Cache Management

The caching system provides:

- Integration with Django's caching framework
- Configurable cache timeouts through settings
- Cache hit/miss tracking in HTTP response headers
- Automatic cache invalidation through timeout expiration
- Special handling for cacheable response status codes (200, 304)

### Naming Conventions

- Files are named by their functional domain (middleware)
- Class names follow Django middleware conventions (FetchCacheMiddleware, UpdateCacheMiddleware)
- Method names are descriptive and follow Python conventions
- Cache-related settings use ZIMAGI*CACHE*\* prefix

### File Organization

Files are organized by caching functionality:

- HTTP middleware implementation in `middleware.py`

### Domain-Specific Patterns

- All caching operations respect Django's middleware patterns
- Cache entries are tracked in the cache data model for request counting
- Error handling follows Django's exception patterns
- Thread-safe operations through Django's cache backend implementations

## Developer Notes and Usage Tips

### Integration Requirements

These modules require:

- Django framework access for middleware and cache operations
- Proper cache backend configuration in settings
- Cache data model for request tracking
- Redis or other supported cache backend for distributed caching

### Usage Patterns

- Configure cache middleware in Django settings
- Use cache tracking in the cache data model for monitoring
- Set appropriate cache timeouts for different resource types
- Use cache bypass parameters for testing and cache refresh operations

### Dependencies

- Django caching framework
- Redis or other cache backend
- Standard Python libraries for hashing operations
- Cache data model from `app/data/cache`

### AI Development Guidance

When generating or modifying caching systems:

1. Maintain consistency with Django's middleware patterns
2. Ensure proper error handling with domain-specific exception classes
3. Follow established patterns for cache key generation
4. Respect the separation of concerns between caching and business logic
5. Consider performance implications for cache operations
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for cache configuration and settings
