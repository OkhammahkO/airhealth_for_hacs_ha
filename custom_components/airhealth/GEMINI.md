# HACS Component Development Best Practices

This document outlines best practices for developing HACS components for Home Assistant, focusing on maintainability, scalability, and community contribution.

## 1. Project Start & Planning
- **Enter Planning Mode:** Before initial code or any major refactor, clearly define scope, milestones, risks, and next steps.
- **Update NOTES.md:** At the end of each session, ensure `NOTES.md` is updated with: `completed`, `in-progress`, `next steps`, and any `blockers`.

## 2. Required Documentation & Files
- **`hacs.json`:**  This file is **required** for HACS to recognize your component. It should contain the name of your component and other relevant information.
- **`manifest.json`:**  The Home Assistant manifest file. It must contain the domain, name, documentation link, and code owners.
- **`README.md`:**  Your component's documentation. It should include installation instructions, configuration details, and usage examples.
- **`DECISIONS.md`:** A log of key project decisions.
- **`NOTES.md`:** Captures the current state of work.
- **`GLOSSARY.md`:** Defines domain-specific terms.

## 3. Project Structure
A HACS component has a specific directory structure within the `custom_components` directory:
```
custom_components/
└── <YOUR_DOMAIN>/
    ├── __init__.py
    ├── manifest.json
    ├── config_flow.py
    ├── const.py
    ├── sensor.py  (or switch.py, light.py, etc.)
    ├── services.yaml
    └── translations/
        └── en.json
```
- **`<YOUR_DOMAIN>/`:** The unique domain for your integration.
- **`__init__.py`:**  Handles the setup and shutdown of the integration.
- **`manifest.json`:**  Defines metadata about the integration.
- **`config_flow.py`:** Manages the user configuration flow through the Home Assistant UI.
- **`const.py`:**  Stores constants used throughout the integration.
- **`sensor.py`, `switch.py`, etc.:**  Define the platforms for your integration.
- **`services.yaml`:** Defines custom services for your integration.
- **`translations/`:**  Stores translations for your integration.

## 4. Configuration Pattern
- **Config Flow:** Use Home Assistant's `config_flow` for user configuration. This provides a user-friendly UI for setting up the integration.
- **`voluptuous`:** Use `voluptuous` for data validation in your config flow.
- **No YAML Configuration:** For new integrations, prefer config flow over YAML-based configuration.

## 5. Code Quality
- **Home Assistant Coding Style:** Follow the Home Assistant coding style guidelines.
- **Linters:** Use `ruff` and `isort` to enforce code style.
- **Type Hints:** Use type hints for all functions and methods.
- **Docstrings:** Write docstrings for all public APIs.
- **Centralized Constants:** Use `const.py` for all constants.

## 6. Home Assistant & HACS Best Practices
- **`DataUpdateCoordinator`:** Use the `DataUpdateCoordinator` from `homeassistant.helpers.update_coordinator` for fetching data from APIs or other sources. This centralizes data fetching and reduces duplicate requests.
- **Async Programming:** Home Assistant is built on `asyncio`. All I/O operations (API calls, file access) must be asynchronous.
- **Entity Naming:** Follow the entity naming guidelines.
- **Lifecycle Management:** Implement `async_setup_entry` and `async_unload_entry` for proper setup and cleanup of your integration.
- **Use HA Core Helpers:** Leverage the helper libraries provided by Home Assistant Core whenever possible.

## 7. Testing & Error Handling
- **`pytest-homeassistant-custom-component`:** Use this `pytest` plugin for testing your custom component.
- **Mock `hass`:** Use the `hass` fixture to mock the Home Assistant instance in your tests.
- **Specific Exceptions:** Raise specific exceptions for different error conditions.
- **Logging:** Use the `logging` module for diagnostics.

## 8. Performance & Scalability
- **Efficient Data Fetching:** Use the `DataUpdateCoordinator` to efficiently fetch and update data.
- **Minimize Blocking:** Avoid blocking the Home Assistant event loop at all costs.

## 9. Security & Privacy
- **No Secrets in Code:** Never commit API keys, passwords, or other secrets to your repository. Use `config_flow` to have users enter their own secrets.
- **Input Validation:** Validate all user input.

## 10. CI / Deployment
- **GitHub Actions:** Use GitHub Actions for CI. Your workflow should lint, test, and type-check your code.
- **HACS Release Workflow:** Create a GitHub Actions workflow to automatically create HACS-compatible releases when you push a new tag.
- **Semantic Versioning:** Use semantic versioning for your releases.

## 11. Context Recovery
- **`DECISIONS.md`:** Update `DECISIONS.md` whenever significant architectural or algorithmic changes are made.
- **`NOTES.md` Snapshots:** Use `NOTES.md` to capture snapshots of the current state.
- **PR Impact Notes:** Add brief “impact notes” to Pull Request descriptions.

## 12. Assistant Deliverables
- **Concise Plan:** Start with a short plan and a clear list of files that will be changed.
- **Full Files:** Provide full file contents when possible.
- **Tests & Examples:** Include relevant tests and usage examples.
- **Assumptions & Risks:** Clearly state any assumptions made and potential failure points.