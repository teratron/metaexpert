# Data Model: CLI Generation

This feature does not introduce a persistent data model with storage. Instead, it defines the structure of the output generated on the filesystem.

## Entity: ExpertProject

Represents the generated expert project directory and its contents.

| Attribute | Type | Description |
|---|---|---|
| `name` | `string` | The sanitized, `snake_case` name provided by the user. This is used as the directory name. |
| `directory_path` | `Path` | The absolute path to the newly created expert directory (e.g., `./my_awesome_expert/`). |
| `main_file` | `Path` | The path to the main entry point file within the directory, which is always `main.py`. |
| `class_name` | `string` | The `PascalCase` version of the user-provided name, which is injected into the `main.py` template to define the main expert class. |

## State Transitions

- The `ExpertProject` entity is created by the `metaexpert new <name>` command.
- It is not designed to be updated or deleted by the CLI.
