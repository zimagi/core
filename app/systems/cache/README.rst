=====================================================
README for Directory: app/systems/cache
=====================================================

Directory Overview
------------------

**Purpose**
   This directory is responsible for implementing caching mechanisms within the Zimagi application. It provides middleware components that integrate with Django's caching framework to optimize performance by storing and retrieving responses and other data.

**Key Functionality**
   *   **Response Caching:** Caches HTTP responses to reduce redundant processing for frequently accessed endpoints.
   *   **Cache Invalidation/Update:** Manages the updating and invalidation of cached responses based on request characteristics.
   *   **User-Specific Caching:** Differentiates cached content based on user authentication to ensure data privacy and correctness.
   *   **Cache Hit/Miss Tracking:** Provides mechanisms to track whether a response was served from the cache or generated dynamically.

Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed for Python 3.8+ environments, specifically within a Django framework application. It operates within the Docker containerized environment as defined by the project's `docker-compose` configurations.

**Local Dependencies**
   *   `django.conf.settings`: Utilized for accessing application-wide settings, including cache configurations and user-related constants.
   *   `django.core.cache.caches`: Provides access to Django's configured cache instances.
   *   `django.utils.cache`: Offers utilities for managing HTTP cache headers and response patching.
   *   `django.utils.deprecation.MiddlewareMixin`: The base class for Django's new-style middleware.
   *   `systems.models.base.run_transaction`: Used for executing database operations within a transaction.
   *   `systems.models.index.Model`: Provides access to the application's model facade for interacting with database models, specifically for cache entry tracking.
   *   `hashlib`: Python's standard library for secure hashes, used here for generating unique cache keys.

File Structure and Descriptions
-------------------------------

**app/systems/cache/middleware.py**
     **Role:** This file defines the core Django middleware classes responsible for handling caching logic for incoming requests and outgoing responses.
     **Detailed Description:** It contains two primary middleware classes: `UpdateCacheMiddleware` and `FetchCacheMiddleware`. `FetchCacheMiddleware` intercepts incoming requests to check if a cached response exists for the given request. If a cached response is found, it is returned immediately, improving performance. If not, the request proceeds, and `UpdateCacheMiddleware` then intercepts the outgoing response. This middleware is responsible for determining if the response should be cached, setting appropriate HTTP cache headers, and storing the response in the configured cache for future requests. It also includes logic to track cache requests in the database and to generate unique cache keys based on the request URL, method, and authenticated user.
     **Relationship:** This file is central to the application's caching strategy, working in conjunction with Django's core request/response cycle and the configured cache backend. It interacts with `systems.models.base` and `systems.models.index` to record cache usage statistics.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  An incoming HTTP request first passes through `FetchCacheMiddleware`.
   2.  `FetchCacheMiddleware` attempts to retrieve a response from the cache based on a generated key (derived from the request method, URL, and user).
   3.  If a cached response is found, it is immediately returned, bypassing further processing.
   4.  If no cached response is found, the request proceeds to the view.
   5.  After the view processes the request and generates a response, the response passes through `UpdateCacheMiddleware`.
   6.  `UpdateCacheMiddleware` determines if the response is cacheable (e.g., not streaming, successful status code, not marked as private).
   7.  If cacheable, the response is stored in the cache with an appropriate timeout.
   8.  Both middleware classes interact with the `systems.models.index.Model` to update cache statistics in the database.

**External Interfaces**
   *   **Django Cache Backend:** The middleware directly interacts with Django's configured cache backend (e.g., Redis, Memcached) to store and retrieve HTTP responses. The specific backend is determined by `settings.CACHE_MIDDLEWARE_ALIAS`.
   *   **Database:** The `UpdateCacheMiddleware` interacts with the application's database (via `systems.models.index.Model` and `systems.models.base.run_transaction`) to record cache hit/miss statistics and other cache-related metadata.
   *   **HTTP Clients:** The `FetchCacheMiddleware` and `UpdateCacheMiddleware` modify HTTP headers (e.g., `Cache-Control`, `Object-Cache`) which are then interpreted by HTTP clients and proxies.
