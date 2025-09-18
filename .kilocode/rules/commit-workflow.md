## Brief overview
These rules establish the commit workflow for the MetaExpert project, specifically focusing on when to create commits and when to push changes to the remote repository.

## Commit Creation
- Create a commit after each successfully completed task with an appropriate descriptive message
- Use conventional commit messages following the format: `<type>(<scope>): <subject>`
- Include detailed commit descriptions when necessary to explain the changes
- Follow semantic versioning principles when determining version number increments

## Push Workflow
- Do NOT automatically push commits to the remote repository after each commit
- Push changes manually after completing a significant number of tasks or at logical checkpoints
- Push before switching branches or ending a work session
- Push when sharing work with other team members or preparing for code review

## Commit Message Conventions
- Types include: feat, fix, chore, docs, style, refactor, perf, test
- Scope is optional but recommended (e.g., config, template, examples)
- Subject should be concise and written in imperative mood
- Example: `feat(template): add new RSI indicator parameters`

## Branch Management
- Create feature branches for all new development work
- Use descriptive branch names following the pattern: `feature/description` or `fix/issue`
- Keep feature branches up to date with the main branch through regular merges or rebases
- Delete feature branches after they have been merged to main

## Code Review Process
- All changes should be reviewed before merging to main branch
- Use pull requests for code review process
- Ensure commit messages follow conventions before merging
- Verify version numbers are correctly updated when applicable