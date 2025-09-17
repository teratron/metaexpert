## Brief overview
These rules provide guidelines for developing the MetaExpert trading bot project, specifically focusing on dependency management, coding conventions, and development workflow preferences.

## Dependency Management
- Use only the `uv` package manager for all dependency management tasks
- Avoid using `uv pip ...` commands when possible
- Do not use requirements.txt or setup.py files
- Prefer using pyproject.toml with dependency groups for managing project dependencies
- Use workspace features in pyproject.toml for multi-package projects

## Communication style
- Communicate in English for code and technical documentation
- Use Russian for explanations and chat responses
- Be concise and direct in communications
- Focus on technical accuracy rather than conversational niceties

## Development workflow
- Create git tags for significant milestones before starting new work
- Use feature branches for development work
- Follow the existing project structure and template patterns
- Update examples to match the main template structure
- Ensure all examples include proper documentation (README.md files)

## Coding best practices
- Use python-dotenv for environment variable management instead of python-dotenv-vault
- Standardize dotenv usage with `from dotenv import load_dotenv` and `_ = load_dotenv()`
- Use consistent version specifications across all pyproject.toml files
- Follow the existing code structure and commenting style in the template.py file
- Remove unnecessary comment stubs from example implementations
- Use proper type hints and documentation strings

## Project context
- The project is a Python-based expert trading system for cryptocurrency trading
- Supports multiple exchanges (Binance, Bybit)
- Uses event-driven architecture with various handlers (init, deinit, tick, bar, timer, etc.)
- Examples should demonstrate real-world usage patterns with environment variable integration
- All configuration should be externalized using .env files

## Other guidelines
- Always check for existing implementations before making changes
- Prefer making multiple related changes in a single apply_diff operation
- Create comprehensive README.md files for all major components and examples
- Ensure dependencies are properly specified with version constraints