## Brief overview
These rules establish that the template.py file is a protected core component of the MetaExpert project that should not be modified during development work.

## Template File Protection
- The `src/metaexpert/template.py` file is the foundational template for all trading experts in the MetaExpert system
- This file must NOT be modified under any circumstances as it serves as the base template for user-generated strategies
- All development work should use this template as a reference but never directly modify it
- Examples and user strategies should be created by copying and modifying this template, not by changing the original
- Any updates to the template structure or parameters should be done with extreme caution and proper review

## Development Approach
- When creating new examples or strategies, always copy the template rather than modifying it
- Use the template as a reference for structure and parameter names when working on other parts of the system
- If changes are needed to the template structure, create a separate discussion/issue rather than direct modification
- All examples in the `examples/` directory should follow the structure established in the template

## Implementation Guidelines
- The template represents the canonical structure for MetaExpert-based trading strategies
- Event handlers, configuration sections, and parameter organization in the template should be preserved in all derived works
- When extending functionality, add to examples rather than modifying the template
- The template should remain a clean, minimal starting point for new users