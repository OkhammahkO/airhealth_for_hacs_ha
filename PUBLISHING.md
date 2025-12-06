# Publishing Guide for AirHealth Integration

This guide walks through the process of publishing the AirHealth integration to HACS.

## Pre-Publication Checklist

### Required Files ✅

- [x] `README.md` - Installation and usage instructions
- [x] `LICENSE` - MIT License
- [x] `CHANGELOG.md` - Version history
- [x] `hacs.json` - HACS configuration
- [x] `custom_components/airhealth/manifest.json` - Integration metadata
- [x] `custom_components/airhealth/__init__.py` - Integration setup
- [x] All required integration files present

### Documentation ✅

- [x] `CONTRIBUTING.md` - Contribution guidelines
- [x] `DECISIONS.md` - Architectural decision records
- [x] `NOTES.md` - Project status and notes
- [x] Clear installation instructions in README
- [x] Configuration steps documented
- [x] Usage examples provided

### Code Quality ✅

- [x] All JSON files validated
- [x] Ruff configuration (`.ruff.toml`)
- [x] Pre-commit hooks configuration
- [x] Type hints present
- [x] Error handling implemented
- [x] Logging configured

### Testing ✅

- [x] Test suite created (`test_init.py`, `test_sensor.py`, `test_config_flow.py`, `test_api.py`)
- [x] Test fixtures configured (`conftest.py`)
- [x] Test requirements documented (`requirements_test.txt`)
- [x] Coverage configuration in `pyproject.toml`

### CI/CD ✅

- [x] GitHub Actions CI workflow (`.github/workflows/ci.yml`)
- [x] GitHub Actions release workflow (`.github/workflows/release.yml`)
- [x] Automated testing configured
- [x] Code quality checks configured

## Publication Steps

### 1. Final Code Review

```bash
# Verify all files are committed
git status

# Run local validation
python -m json.tool hacs.json
python -m json.tool custom_components/airhealth/manifest.json
python -m json.tool custom_components/airhealth/strings.json
```

### 2. Create Git Tag

```bash
# Ensure you're on the main branch
git checkout main

# Create annotated tag matching manifest.json version
git tag -a v0.2.0 -m "Release v0.2.0 - Initial HACS release"

# Push tag to GitHub
git push origin v0.2.0
```

### 3. Create GitHub Release

1. Go to https://github.com/OkhammahkO/prj-airhealth/releases
2. Click "Draft a new release"
3. Select tag: `v0.2.0`
4. Release title: `v0.2.0 - Initial HACS Release`
5. Copy release notes from CHANGELOG.md
6. Click "Publish release"

The release workflow will automatically run and create the release.

### 4. Test HACS Installation

Before submitting to HACS default repository, test the custom repository installation:

1. In Home Assistant, go to HACS → Integrations
2. Click the three dots (⋮) → Custom repositories
3. Add repository URL: `https://github.com/OkhammahkO/prj-airhealth`
4. Category: Integration
5. Click "Add"
6. Find "AirHealth" and install it
7. Restart Home Assistant
8. Test configuration and functionality

### 5. Submit to HACS (Optional)

To make your integration available in the default HACS repository:

1. Ensure at least one release exists (completed in step 3)
2. Ensure all HACS requirements are met:
   - Repository is public
   - Has a valid `hacs.json`
   - Has a `README.md`
   - Has a `LICENSE`
   - Integration is in `custom_components/` directory
   - Has at least one release tag

3. Fork the HACS default repository:
   - Go to https://github.com/hacs/default
   - Click "Fork"

4. Add your integration to the list:
   - Edit `integration` file
   - Add your repository: `OkhammahkO/prj-airhealth`
   - Commit and push

5. Create a pull request:
   - Title: `Add AirHealth integration`
   - Description: Brief description of the integration
   - Link to repository
   - Confirm all requirements are met

6. Wait for review and approval

## Post-Publication

### Monitor and Respond

- Watch GitHub issues for bug reports
- Respond to user questions
- Monitor HACS compatibility

### Future Updates

When releasing updates:

1. Update version in `manifest.json`
2. Update `CHANGELOG.md` with changes
3. Commit changes
4. Create new git tag: `git tag -a v0.x.x -m "Release v0.x.x"`
5. Push tag: `git push origin v0.x.x`
6. Create GitHub release

HACS will automatically detect new releases.

## HACS Requirements Summary

### Mandatory

- ✅ Repository is public
- ✅ Has a valid `hacs.json` file
- ✅ Has a `README.md` with installation instructions
- ✅ Has a `LICENSE` file
- ✅ Integration code in `custom_components/[domain]/` directory
- ✅ Valid `manifest.json` with all required fields
- ✅ At least one release tag (v0.2.0)

### Recommended

- ✅ GitHub Actions for CI/CD
- ✅ Comprehensive documentation
- ✅ Test suite
- ✅ Code quality tools configured
- ✅ CHANGELOG.md
- ✅ CONTRIBUTING.md
- ✅ Clear commit history

## Version Guidelines

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (v1.0.0): Breaking changes, incompatible API changes
- **MINOR** (v0.2.0): New features, backwards compatible
- **PATCH** (v0.2.1): Bug fixes, backwards compatible

## Support Channels

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and community support
- README: Installation and usage documentation

## Maintenance

### Regular Tasks

- Monitor and respond to issues
- Review and merge pull requests
- Update dependencies as needed
- Test with new Home Assistant releases
- Update documentation

### Quality Standards

- All code changes should include tests
- Maintain or improve code coverage
- Follow Home Assistant development guidelines
- Keep dependencies minimal
- Document all significant changes

## Troubleshooting

### Common Issues

**HACS doesn't detect the integration:**
- Verify `hacs.json` is valid
- Ensure repository is public
- Check that `custom_components/airhealth/` structure is correct
- Verify at least one release tag exists

**Installation fails:**
- Check manifest.json is valid
- Verify all required files are present
- Check Home Assistant version compatibility
- Review HACS logs for errors

**Integration doesn't load:**
- Check Home Assistant logs
- Verify manifest.json requirements
- Test API credentials
- Check coordinator initialization

## Resources

- [HACS Documentation](https://hacs.xyz/docs/publish/integration)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Integration Quality Scale](https://www.home-assistant.io/docs/quality_scale/)
- [Semantic Versioning](https://semver.org/)

## Next Steps After Publishing

1. Monitor initial user feedback
2. Address any critical issues quickly
3. Plan feature enhancements based on user requests
4. Consider applying for Home Assistant core inclusion (long-term goal)
5. Build community around the integration

---

**You're ready to publish!** 🚀

The AirHealth integration is now HACS-ready and can be published following the steps above.
