# MetaExpert CLI Module

## Core Architecture

```text
src/metaexpert/cli/
├── __init__.py         # Public API exports
├── app.py              # Main Typer application
├── commands/           # Command handlers (one file per command)
│   ├── new.py
│   ├── run.py
│   ├── stop.py
│   ├── list.py
│   ├── logs.py
│   └── backtest.py
├── core/               # Core functionality
│   ├── config.py       # CLI configuration with Pydantic
│   ├── exceptions.py   # CLI-specific exceptions
│   └── output.py       # Rich-based output formatting
├── process/            # Process lifecycle management
│   ├── manager.py      # ProcessManager class
│   └── pid_lock.py     # Cross-platform PID locking
├── templates/          # Jinja2 template system
│   ├── generator.py    # TemplateGenerator class
│   └── files/          # Template files (.j2)
└── utils/              # Utilities
    ├── validators.py   # Input validation
    ├── formatters.py   # Output formatting
    └── helpers.py      # General helpers
```
