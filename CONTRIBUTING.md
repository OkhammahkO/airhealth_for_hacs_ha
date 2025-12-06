# Contributing to AirHealth Integration

Thank you for considering contributing to the AirHealth Home Assistant integration! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the best outcome for the project and community

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/OkhammahkO/prj-airhealth/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - Home Assistant version and integration version
   - Relevant log entries (set logging to debug if needed)
   - Configuration details (sanitize sensitive data!)

### Suggesting Enhancements

1. Check existing [Issues](https://github.com/OkhammahkO/prj-airhealth/issues) for similar suggestions
2. Create a new issue describing:
   - The enhancement and its benefits
   - Possible implementation approach
   - Any alternatives considered

### Pull Requests

1. **Fork and clone** the repository
2. **Create a branch** for your changes: `git checkout -b feature/your-feature-name`
3. **Make your changes** following the coding standards below
4. **Test your changes** thoroughly
5. **Update documentation** as needed
6. **Commit your changes** with clear, descriptive messages
7. **Push to your fork** and submit a pull request

## Development Setup

### Prerequisites

- Home Assistant development environment
- Python 3.11 or newer
- Git

### Local Development

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/prj-airhealth.git
   cd prj-airhealth
   ```

2. Set up Home Assistant development container (recommended):
   ```bash
   # Follow Home Assistant development setup guide
   # https://developers.home-assistant.io/docs/development_environment
   ```

3. Symlink the integration to your Home Assistant config:
   ```bash
   ln -s /path/to/prj-airhealth/custom_components/airhealth \
         /path/to/homeassistant/config/custom_components/airhealth
   ```

4. Install development dependencies:
   ```bash
   pip install pytest pytest-homeassistant-custom-component ruff mypy
   ```

### Running Tests

```bash
# Run all tests
pytest custom_components/airhealth/tests/

# Run specific test file
pytest custom_components/airhealth/tests/test_sensor.py

# Run with coverage
pytest --cov=custom_components.airhealth custom_components/airhealth/tests/
```

### Code Quality Checks

```bash
# Linting with ruff
ruff check custom_components/airhealth/

# Formatting with ruff
ruff format custom_components/airhealth/

# Type checking with mypy
mypy custom_components/airhealth/
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- Maximum line length: 88 characters (Black/Ruff default)
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes

### Home Assistant Conventions

- Follow [Home Assistant development guidelines](https://developers.home-assistant.io/docs/development_index)
- Use async/await for all I/O operations
- Use `DataUpdateCoordinator` for data fetching
- Implement proper error handling with custom exceptions
- Use `PARALLEL_UPDATES` appropriately for sensor platforms
- Follow entity naming conventions
- Implement proper unique IDs for entities

### Code Structure

```python
"""Module docstring describing purpose."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)


async def async_function(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Function docstring with description.

    Args:
        hass: Home Assistant instance
        config: Configuration dictionary

    Returns:
        True if successful, False otherwise

    Raises:
        ValueError: If config is invalid
    """
    # Implementation here
    pass
```

### Testing Standards

- Write tests for all new features
- Maintain or improve code coverage
- Use pytest fixtures for common setup
- Mock external API calls
- Test error conditions and edge cases
- Use descriptive test names: `test_sensor_updates_on_coordinator_refresh`

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes (formatting, etc.)
- `chore`: Maintenance tasks

Examples:
```
feat(sensor): add humidity sensor support

Implement humidity sensor for environments with humidity data
from the AirHealth API.

Closes #42
```

```
fix(api): handle timeout errors gracefully

Add proper exception handling for API timeout errors and fallback
to cached data when available.

Fixes #38
```

## Documentation

### Update Required Documentation

When making changes, update:

- README.md - Installation, configuration, usage
- CHANGELOG.md - Add entry under [Unreleased]
- Code docstrings - Document functions and classes
- strings.json - Add/update any UI strings
- DECISIONS.md - Document significant architectural choices

### Writing Documentation

- Use clear, concise language
- Include code examples where helpful
- Keep formatting consistent
- Update screenshots if UI changes

## Review Process

1. Automated checks must pass (when CI/CD is implemented)
2. Code review by maintainer(s)
3. Testing by reviewer
4. Approval and merge

## Release Process

Releases are managed by maintainers:

1. Update version in `manifest.json`
2. Update CHANGELOG.md (move [Unreleased] to new version)
3. Create git tag: `git tag -a v0.x.0 -m "Release v0.x.0"`
4. Push tag: `git push origin v0.x.0`
5. Create GitHub release from tag
6. HACS automatically detects new release

## Getting Help

- Check existing [documentation](README.md)
- Search [issues](https://github.com/OkhammahkO/prj-airhealth/issues)
- Ask questions in a new issue with the `question` label
- Review [Home Assistant development docs](https://developers.home-assistant.io/)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this integration better for everyone. We appreciate your time and effort!
