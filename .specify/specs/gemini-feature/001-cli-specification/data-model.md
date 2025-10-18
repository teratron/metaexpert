# Data Model: CLI Feature

This document formalizes the data structures identified in the feature specification for the Command-Line Interface.

## 1. ExpertProject

Represents a user-created trading bot project directory.

- **Type**: Directory
- **Contents**:
    - `main.py`: The user's strategy code.
    - `pyproject.toml`: Project configuration and dependencies.
    - `.env`: Environment variables, including sensitive API keys.
    - `README.md`: Project documentation.
    - `.gitignore`: Git ignore file.

## 2. GlobalConfig

Defines the schema for the global, non-sensitive configuration file.

- **Storage**: JSON file located at `~/.metaexpert/config.json`.
- **Schema**:
    ```json
    {
      "author": "string",
      "default_exchange": "string",
      "log_level": "string (e.g., INFO, DEBUG)"
    }
    ```

## 3. PIDFile

Defines the structure for the process ID file used to track a running expert.

- **Storage**: A file named after the expert instance (e.g., `my-bot.pid`) located in a central directory like `~/.metaexpert/pids/`.
- **Contents**: The raw process ID (PID) of the running expert process as a plain text integer.

## 4. LogDirectory

Defines the central location for storing all expert log files.

- **Storage**: A central directory located at `~/.metaexpert/logs/`.
- **Contents**: Contains log files, typically named after the expert instance (e.g., `my-bot.log`).
