# AirHealth Custom Component for Home Assistant

This custom component integrates AirHealth data into Home Assistant. It provides sensors for grass pollen, other allergens, air quality, and woodsmoke levels in Australia.

## Installation

### HACS (Home Assistant Community Store)

1.  Go to HACS -> Integrations.
2.  Click on the 3 dots in the top right corner and select "Custom repositories".
3.  Add the URL to your repository and select "Integration" as the category.
4.  Click "ADD".
5.  The AirHealth integration should now be visible. Click "INSTALL".
6.  Restart Home Assistant.

## Configuration

1.  Go to Settings -> Devices & Services.
2.  Click "Add Integration" and search for "AirHealth".
3.  Enter your API Key and SAL code.
4.  Click "Submit".

The component will automatically create sensors for all available data.
