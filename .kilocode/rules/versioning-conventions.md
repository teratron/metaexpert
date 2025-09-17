## Brief overview
These rules establish the commit message conventions and versioning standards for the MetaExpert project, following semantic versioning (SemVer) principles.

## Commit Message Conventions
- Use conventional commit messages following the format: `<type>(<scope>): <subject>`
- Types include: feat, fix, chore, docs, style, refactor, perf, test
- Scope is optional but recommended (e.g., config, template, examples)
- Subject should be concise and written in imperative mood
- Example: `feat(template): add new RSI indicator parameters`

## Semantic Versioning (SemVer)
- Follow SemVer specification: MAJOR.MINOR.PATCH
- MAJOR version when making incompatible API changes
- MINOR version when adding functionality in a backward compatible manner
- PATCH version when making backward compatible bug fixes
- Version numbers should be updated in pyproject.toml files when appropriate

## Git Workflow Standards
- Create feature branches for all new development work
- Use descriptive branch names following the pattern: `feature/description` or `fix/issue`
- Create git tags for significant releases following SemVer
- Write clear, concise commit messages that explain the "what" and "why" of changes
- Squash commits when appropriate to maintain clean history

## Release Management
- Tag releases with version numbers (e.g., v1.2.3)
- Create release notes for each tagged version
- Update version numbers consistently across all relevant pyproject.toml files
- Follow SemVer when determining version number increments

## Code Review and Merge Standards
- All changes should be reviewed before merging to main branch
- Use pull requests for code review process
- Ensure commit messages follow conventions before merging
- Verify version numbers are correctly updated when applicable