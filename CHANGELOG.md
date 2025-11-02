# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.html).

## [Unreleased]

## [0.5.0] - 2025-10-30

### Added

- New logger validators module with comprehensive event validation capabilities
- New logger results module for structured logging result handling
- New logger metrics module for performance and usage tracking
- New logger constants module for centralized configuration constants
- Enhanced thread-safe logging setup with proper reconfiguration support
- Improved error handling and fallback mechanisms in logging system

### Fixed

- Critical thread-safety issues in setup_logging function
- Race conditions in logging reconfiguration
- Handler management conflicts with other components
- Missing error handling in logging setup process
- Improved consistency in logging configuration updates

### Changed

- Updated development status from Alpha to Beta in project metadata
- Enhanced logging system architecture for better modularity
- Improved test coverage for logger components

## [0.4.1] - 2025-10-28

### Fixed

- Critical bug in filter_by_log_level function that could potentially cause incorrect log filtering by level

## [0.4.0] - 2025-10-28

### Added

- New configuration presets for logging system (development, production, backtesting)
- Enhanced security filtering to automatically mask sensitive data in logs
- Improved validation for logger configuration parameters
- Context management utilities for correlated logging events
- Performance monitoring capabilities for operation durations

### Fixed

- Critical bugs in logging module
- Improved consistency and flexibility of logging configuration
- Replaced direct 'print' statements with 'MetaLogger' calls across the project

## [0.3.13] - 2025-10-21

### Changed

- Updated MetaLogger to inherit from `structlog.stdlib.Logger` instead of logging.Logger
- Removed unused formatter.py file from logger module
- Added rule to treat warnings as errors in test-driven workflow

### Added

- New development principles rule file
- New rule for treating warnings as errors in test-driven workflow

### Fixed

- Various code improvements following SOLID, DRY, KISS, and YAGNI principles

## [0.3.4] - 2025-10-21

### Fixed

- Updated logging module integration across the project
- Replaced direct 'print' statements with 'MetaLogger' calls
- Enhanced consistency and flexibility of logging configuration
