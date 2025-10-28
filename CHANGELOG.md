# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.html).

## [0.3.4] - 2025-10-21

### Fixed

- Updated logging module integration across the project
- Replaced direct 'print' statements with 'MetaLogger' calls
- Enhanced consistency and flexibility of logging configuration

## [Unreleased]

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

- Updated MetaLogger to inherit from `structlog.stdlib.BoundLogger` instead of logging.Logger
- Removed unused formatter.py file from logger module
- Added rule to treat warnings as errors in test-driven workflow

### Added

- New development principles rule file
- New rule for treating warnings as errors in test-driven workflow

### Fixed

- Various code improvements following SOLID, DRY, KISS, and YAGNI principles
