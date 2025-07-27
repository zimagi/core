# Environment Configuration Directory

## Overview

The `env` directory contains environment variable configuration files that are loaded into Docker Compose manifests. These files define the runtime configuration for various Zimagi services and components, controlling everything from application settings to security credentials.

This directory plays a critical architectural role by centralizing all environment-specific configurations, making it easy to manage different deployment scenarios (development, testing, production) while maintaining security through separation of public and secret configurations.

The files in this directory are used by:
- Docker Compose during service initialization
- The Zimagi application at runtime
- Build systems for environment-specific deployments
- Developers for local development setup

## Directory Contents

| File/Directory | Purpose | Format |
|----------------|---------|--------|
| public.default | Default public environment variables for all environments | Environment file |
| public.api.encrypted | Public environment variables for encrypted API configurations | Environment file |
| secret | Secret environment variables including keys, passwords, and tokens | Environment file |
| secret.example | Template for creating secret environment files | Environment file |
| generated | Runtime-generated environment variables (user IDs, passwords, API keys) | Shell export statements |
| public.api | Public environment variables for API configurations | Environment file |

## File Descriptions

### public.default
Contains common public environment variables used across all Zimagi services. This includes database configurations, parallel processing settings, debug flags, logging levels, and server worker configurations. This file serves as the base configuration that other public environment files typically extend.

### public.api.encrypted
Defines public environment variables specifically for encrypted API configurations. This includes settings that enable command API and data API encryption, page caching configurations, and Flower (Celery monitoring) settings. The "encrypted" suffix indicates this configuration is used when encryption is enabled.

### secret
Holds sensitive environment variables including secret keys, passwords, API tokens, and GitHub credentials. This file contains actual secret values and should never be committed to version control. It includes configurations for email services, GitHub integration, default modules, client caching, and AI service API keys.

### secret.example
A template file showing the structure and required variables for the secret environment file without including actual secret values. Developers use this as a reference to create their own secret file with real credentials.

### generated
Contains environment variables that are programmatically generated during the build or initialization process. This includes user IDs, group IDs, administrative tokens, API keys, and service passwords. These values are typically created dynamically to ensure uniqueness and security.

### public.api
Defines public environment variables for standard (non-encrypted) API configurations. This file mirrors the structure of public.api.encrypted but with encryption disabled, providing a configuration for development or testing environments where encryption is not required.

## Cross-Referencing

The `env` directory integrates with several other parts of the Zimagi project:

- **docker directory**: Docker build processes and deployment scripts use these environment configurations
- **reactor directory**: The Reactor Kubernetes development platform references these configurations
- **Top-level zimagi script**: The main executable loads these environment files during Docker container initialization
- **app directory**: Application code accesses these environment variables at runtime
- **.gitignore**: Controls which environment files are excluded from version control

## Key Concepts and Patterns

### Naming Conventions
- Files are named with descriptive prefixes indicating their purpose (public, secret, generated)
- The ".encrypted" suffix indicates configurations for encrypted environments
- The ".example" suffix indicates template files

### File Organization
Environment configurations are organized by:
- Security level (public vs secret)
- Service context (default, API-specific)
- Generation method (static vs generated)

### Configuration Standards
- All environment variables are prefixed with "ZIMAGI_" for application-specific settings
- Service-specific variables use descriptive prefixes (FLOWER_, OPENROUTER_, DEEPINFRA_, etc.)
- Boolean values use lowercase "true"/"false"
- List values use JSON array format

### Security Patterns
- Public configurations are committed to version control
- Secret configurations are excluded from version control via .gitignore
- Generated configurations are created at runtime/build time
- Sensitive values are never stored in plain text in committed files

## Version Control and Git Handling

As specified in the project's `.gitignore` file, certain environment files are excluded from version control for security reasons:

- `env/secret` - Contains actual secret values and should never be committed
- `env/generated` - Contains dynamically generated values that should be created per deployment

The following files are tracked in version control:
- `public.default` - Safe base configuration
- `public.api.encrypted` - Safe encrypted API configuration
- `public.api` - Safe standard API configuration
- `secret.example` - Template for developers

Developers should copy `secret.example` to `secret` and populate it with actual values for their local environment.

## Developer Notes and Usage

### Setup Process
1. Copy `secret.example` to `secret` and fill in actual values
2. Ensure `generated` file is created by the initialization process
3. Select appropriate public configuration based on deployment needs

### Environment Selection
The environment is selected through the `COMPOSE_ENVIRONMENT` and `COMPOSE_PROFILE` environment variables, which determine which public configuration files are loaded.

### Security Considerations
- Never commit actual secret values to version control
- Rotate generated passwords and keys regularly
- Ensure proper file permissions on secret files (typically 600)
- Use the generated file for dynamic secrets to maintain consistency across services

### AI Development Guidance
When generating or modifying environment configurations:
- Maintain the prefix naming convention for variables
- Follow the existing structure for boolean and list values
- Ensure secret values are never included in generated outputs
- Respect the separation between public, secret, and generated configurations
- Document any new variables with clear, descriptive names
