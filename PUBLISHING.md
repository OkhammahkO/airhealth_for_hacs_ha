# Publishing Guide

Quick guide to publish the AirHealth integration to HACS.

## Prerequisites

All required files are in place:
- ✅ README.md, LICENSE, CHANGELOG.md
- ✅ hacs.json, manifest.json
- ✅ Integration code in custom_components/airhealth/
- ✅ Tests and CI/CD workflows

## Publish Steps

### 1. Create Git Tag

```bash
# Verify version in manifest.json is 0.2.0
cat custom_components/airhealth/manifest.json | grep version

# Create tag
git tag -a v0.2.0 -m "Release v0.2.0 - Initial HACS release"

# Push tag
git push origin v0.2.0
```

### 2. Create GitHub Release

The release workflow will automatically create a GitHub release when you push the tag.

Alternatively, create manually:
1. Go to https://github.com/OkhammahkO/prj-airhealth/releases/new
2. Select tag: `v0.2.0`
3. Title: `v0.2.0 - Initial HACS Release`
4. Copy description from CHANGELOG.md
5. Publish

### 3. Test HACS Installation

1. In Home Assistant → HACS → Integrations
2. Click ⋮ → Custom repositories
3. Add: `https://github.com/OkhammahkO/prj-airhealth`
4. Category: Integration
5. Install and test

### 4. Submit to HACS (Optional)

To add to HACS default repository:

1. Fork https://github.com/hacs/default
2. Edit `integration` file
3. Add: `OkhammahkO/prj-airhealth`
4. Create pull request

## Future Releases

For version updates:

1. Update `manifest.json` version
2. Update `CHANGELOG.md`
3. Commit changes
4. Create tag: `git tag -a v0.x.x -m "Release v0.x.x"`
5. Push: `git push origin v0.x.x`

HACS automatically detects new releases.

## Troubleshooting

**HACS doesn't see the integration:**
- Verify hacs.json is valid
- Check repository is public
- Ensure release tag exists

**Installation fails:**
- Validate manifest.json
- Check Home Assistant version compatibility
- Review HACS/HA logs

## Resources

- [HACS Docs](https://hacs.xyz/docs/publish/integration)
- [HA Developer Docs](https://developers.home-assistant.io/)
