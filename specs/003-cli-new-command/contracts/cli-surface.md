# CLI Surface Contract

This document defines the command-line surface, which acts as the public API for this feature.

## Command: `new`

Creates a new expert project directory from the template.

### Usage

```sh
metaexpert new <EXPERT_NAME>
```

### Arguments

- **`<EXPERT_NAME>`** (Required)
  - **Type**: `string`
  - **Description**: The name for the new expert. This name will be sanitized to create a directory name (`snake_case`) and a class name (`PascalCase`).
  - **Example**: `"My First Expert"`

### Behavior

- Creates a new directory named after the sanitized `<EXPERT_NAME>`.
- Inside the directory, it creates a `main.py` file, copying the content from `src/metaexpert/template/template.py`.
- It replaces placeholder identifiers within the new `main.py` with the sanitized `PascalCase` version of the expert name.
- Fails with an error if a directory with the target name already exists.
- Fails with an error if `<EXPERT_NAME>` is a reserved Python keyword.

---

## Command: `help`

Displays help information for the CLI or a specific command.

### Usage

```sh
# General Help
metaexpert --help
metaexpert -h

# Command-Specific Help
metaexpert help new
metaexpert new --help
```

### Behavior

- When run without a subcommand, it lists all available commands and their brief descriptions.
- When run with a subcommand, it displays detailed information about that command's arguments, options, and behavior.
