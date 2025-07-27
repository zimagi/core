# Zimagi CircleCI Directory

## Overview

The `.circleci` directory contains all Continuous Integration/Continuous Deployment (CI/CD) configuration files for the Zimagi platform. This directory defines the automated workflows that build, test, and deploy Zimagi components through CircleCI, ensuring code quality, reliability, and consistent delivery of the platform.

This directory plays a critical architectural role by automating the software delivery process, enabling:
- Automated testing of code changes across multiple environments
- Container image building and deployment to Docker registries
- Python package deployment to PyPI
- Documentation generation and deployment
- Helm chart version updates for Kubernetes deployments

The CI/CD system is primarily used by:
- **Developers** for validating code changes before merging
- **DevOps engineers** managing deployment pipelines
- **Quality assurance engineers** ensuring platform stability
- **AI models** understanding deployment processes and generating CI/CD configurations

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| config.yml | Main CircleCI configuration file defining all jobs, workflows, and deployment pipelines | YAML |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the root project directory which contains top-level project files
- **Docker Integration**: Works with `docker` directory for container image building and deployment
- **Package Integration**: Connects to `package` directory for Python SDK deployment
- **Documentation System**: Integrates with `docs` directory for documentation deployment
- **Application Code**: Tests and validates code from the `app` directory
- **Reactor Platform**: Builds and tests components from the `reactor` directory

The `.circleci` directory serves as the automation layer that ensures consistent testing and deployment of all Zimagi components, connecting to Docker build systems in `docker`, package management in `package`, and application code in `app`.

## Key Concepts, Conventions, and Patterns

### CI/CD Architecture

The CircleCI configuration implements a workflow-based approach to continuous integration and deployment:

- **Job-Based Execution**: Individual units of work that perform specific tasks (testing, building, deploying)
- **Workflow Orchestration**: Coordinated sequences of jobs that define complete CI/CD pipelines
- **Parallel Execution**: Multiple jobs running concurrently to reduce pipeline execution time
- **Conditional Execution**: Jobs that run based on filters (branches, tags) for appropriate deployment targets

### Naming Conventions

- Jobs use descriptive names with verb-noun patterns (e.g., `test-api-commands`, `deploy-pip`)
- Workflows follow domain-specific naming (e.g., `deploy`)
- Configuration keys use lowercase with underscores for separation
- Docker image deployment jobs include platform architecture information (amd64, arm64)

### File Organization

Files are organized by functional domain following these patterns:

- **Main Configuration**: Located in `config.yml` containing all job and workflow definitions
- **Job Grouping**: Jobs organized by functional area (testing, deployment, documentation)
- **Workflow Definition**: Single workflow that orchestrates all deployment activities

### Domain-Specific Patterns

- Testing jobs use standardized machine images and execution environments
- Deployment jobs follow consistent patterns for Docker image and Python package publishing
- All jobs include proper logging and error reporting mechanisms
- Jobs implement conditional execution based on branch and tag filters

## Developer Notes and Usage Tips

### Integration Requirements

The CircleCI configuration requires:

- CircleCI account with access to the Zimagi repository
- Proper Docker Hub credentials for image deployment
- PyPI credentials for Python package deployment
- GitHub SSH keys for documentation and helm chart deployments
- Access to Docker daemon for building images

### Usage Patterns

- Configuration changes are validated through CircleCI's config processing
- Jobs are triggered automatically on push events to GitHub
- Deployment jobs require tagged releases for versioned deployments
- Testing jobs run on all branches to ensure code quality

### Dependencies

- CircleCI for workflow execution
- Docker for container image building
- Python for package deployment
- Git for documentation and helm chart updates
- SSH keys for GitHub deployments

### AI Development Guidance

When generating or modifying CircleCI configurations:

1. Maintain consistency with existing job and workflow patterns
2. Follow established naming conventions for jobs and workflows
3. Implement proper error handling and logging in all jobs
4. Use appropriate machine types for different job requirements
5. Follow the pattern of providing both continuous integration and deployment workflows
6. Ensure jobs properly integrate with Docker containerization and deployment systems
7. Maintain consistency with branch and tag filtering for appropriate execution contexts
8. Respect the separation between testing, building, and deployment job types
9. Follow security best practices for credential management
10. Use appropriate resource classes for different job types (standard vs ARM builds)
