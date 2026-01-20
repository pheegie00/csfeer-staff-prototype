# GitHub Copilot Instructions for CSFeer Project

## Project Overview

This is a Django application using USWDS (U.S. Web Design System) for all UI components and styling.

## Critical Guidelines

### USWDS Components & Styling

**ALWAYS follow these principles when working with HTML, CSS, or UI components:**

1. **Check USWDS first**: Before creating any custom HTML/CSS, verify if USWDS provides a suitable component at https://designsystem.digital.gov/components/overview/

2. **Use USWDS utilities**: Leverage built-in utility classes for typography, spacing, colors, and layout instead of custom CSS

3. **Reference the pattern library**: Check http://ui.csfeer:8000/pattern-library/ for project-specific components before building new ones

4. **Avoid custom CSS**: Only create custom styles when USWDS doesn't provide the needed functionality

5. **Read the guidelines**: Always reference [docs/USWDS_GUIDELINES.md](../docs/USWDS_GUIDELINES.md) for detailed examples and workflow

### Build Process

- After SCSS changes: Run `npm run build`
- Static files use symlinks, so `collectstatic` is NOT needed during development

### Python Execution

- Always use `uv run` to execute Python code (e.g., `uv run python manage.py runserver`)
- This ensures proper virtual environment and dependency management

### Code Standards

- Follow Django best practices
- Keep business logic in Python, not templates
- Use type hints in Python code
- Write tests for new features
- Do NOT use emojis in code, comments, or documentation

## Key Resources

- [USWDS Guidelines](../docs/USWDS_GUIDELINES.md) - Component and styling best practices
- [E2E Testing Guide](../docs/E2E_TESTING.md) - Testing documentation
- [USWDS Components](https://designsystem.digital.gov/components/overview/)
- [USWDS Utilities](https://designsystem.digital.gov/utilities/)

## When in Doubt

Ask: "Does USWDS already solve this?" - The answer is usually yes.
