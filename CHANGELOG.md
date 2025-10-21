# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.html).

## [Unreleased]

## [0.3.3] - 2025-10-21

### Changed
- Updated MetaLogger to inherit from structlog.stdlib.BoundLogger instead of logging.Logger
- Removed unused formatter.py file from logger module
- Added rule to treat warnings as errors in test-driven workflow

### Added
- New development principles rule file
- New rule for treating warnings as errors in test-driven workflow

### Fixed
- Various code improvements following SOLID, DRY, KISS, and YAGNI principles