# Contributing

Thanks for your interest in contributing to AirHealth!

## Reporting Issues

- Check existing [issues](https://github.com/OkhammahkO/prj-airhealth/issues) first
- Include Home Assistant version, integration version, and logs
- Sanitize any sensitive data (API keys, SAL codes)

## Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `pytest custom_components/airhealth/tests/`
5. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/prj-airhealth.git

# Install dependencies
pip install -r requirements_test.txt

# Run tests
pytest custom_components/airhealth/tests/
```

## Code Standards

- Follow existing code style
- Add tests for new features
- Update documentation as needed
- Use meaningful commit messages

## Questions?

Open an issue with the `question` label.
