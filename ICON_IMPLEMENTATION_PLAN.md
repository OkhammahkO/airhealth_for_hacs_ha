# Icon Implementation Plan

## Overview
Add colored circle icons (🟢🟡🟠🔴) to sensor states and attributes to provide visual level indicators.

## Icon Mapping

### Level Icons
- 🟢 `Low` / `None`
- 🟡 `Moderate`
- 🟠 `High`
- 🔴 `Extreme`

## Implementation Strategy

### 1. Add Helper Function (const.py)
Create a utility function to map levels to icons:

```python
def get_level_icon(level: str) -> str:
    """Return colored circle icon for level."""
    level_icons = {
        "Low": "🟢",
        "None": "🟢",
        "Moderate": "🟡",
        "High": "🟠",
        "Extreme": "🔴",
    }
    return level_icons.get(level, "⚪")
```

### 2. Modify Sensor Class (sensor.py)

#### Option A: Icon in State (Simple)
Prepend icon to the native_value:
```python
@property
def native_value(self) -> StateType:
    """Return the state with icon."""
    level = self._get_level()  # Extract level
    if level:
        icon = get_level_icon(level)
        return f"{icon} {level}"
    return level
```

**Pros:** Visible in sensor badge, entity cards
**Cons:** Changes state format (not just "Low", but "🟢 Low")

#### Option B: Icon in Attributes Only (Recommended)
Keep state as-is, add `level_icon` to attributes:
```python
@property
def extra_state_attributes(self) -> dict[str, Any]:
    """Return attributes with level icon."""
    attributes = super().extra_state_attributes()

    # Add level icon for main sensor
    level = self.native_value
    if level:
        attributes["level_icon"] = get_level_icon(level)

    # Add icons to allergen breakdown
    if "allergens" in attributes and attributes["allergens"]:
        for allergen in attributes["allergens"]:
            allergen["level_icon"] = get_level_icon(allergen.get("level"))

    return attributes
```

**Pros:** Doesn't change state format, cleaner for automations
**Cons:** Requires template to display in UI

### 3. Enhanced Attributes Structure

#### Before:
```yaml
sensor.airhealth_other_allergens_day1:
  date: 2025-12-07
  allergens:
    - name: Plantain
      level: High
    - name: Birch
      level: Moderate
```

#### After:
```yaml
sensor.airhealth_other_allergens_day1:
  state: Extreme
  date: 2025-12-07
  level_icon: 🔴
  allergens:
    - name: Plantain
      level: High
      level_icon: 🟠
    - name: Birch
      level: Moderate
      level_icon: 🟡
```

## Mock-up Results

### Sensor States (Option A - Icon in State)
```
sensor.airhealth_grass_day0: "🟠 High"
sensor.airhealth_grass_day1: "🟡 Moderate"
sensor.airhealth_grass_day2: "🟢 Low"

sensor.airhealth_other_allergens_day0: "🔴 Extreme"
sensor.airhealth_other_allergens_day1: "🟠 High"

sensor.airhealth_air_quality_day0: "🟢 Low"
sensor.airhealth_woodsmoke_day0: "🟡 Moderate"
```

### Sensor Attributes (Option B - Icon in Attributes)
```yaml
# Grass Pollen Sensor
sensor.airhealth_grass_day0:
  state: High
  date: 2025-12-06
  level_icon: 🟠

# Other Allergens Sensor with Breakdown
sensor.airhealth_other_allergens_day1:
  state: Extreme
  date: 2025-12-07
  level_icon: 🔴
  allergens:
    - name: Plantain
      level: High
      level_icon: 🟠
    - name: Birch
      level: Moderate
      level_icon: 🟡
    - name: Olive
      level: Low
      level_icon: 🟢

# Air Quality Sensor
sensor.airhealth_air_quality_day0:
  state: Low
  date: 2025-12-06
  level_icon: 🟢
  woodsmoke_level: Moderate
  supporting_data:
    pm25: 12.5
    pm10: 20.3
```

## Lovelace Display

### Using Templates (Option B)
```yaml
type: entities
entities:
  - entity: sensor.airhealth_grass_day0
    name: Grass Pollen
    secondary_info: last-changed
    card_mod:
      style: |
        :host {
          --card-mod-icon: "{{ state_attr('sensor.airhealth_grass_day0', 'level_icon') }}";
        }

  # Or use template sensor
  - type: custom:template-entity-row
    entity: sensor.airhealth_other_allergens_day0
    name: >
      {{ state_attr('sensor.airhealth_other_allergens_day0', 'level_icon') }} Other Allergens
    state: "{{ states('sensor.airhealth_other_allergens_day0') }}"
```

### Allergen Breakdown Card
```yaml
type: markdown
content: >
  ## Other Allergens - {{ state_attr('sensor.airhealth_other_allergens_day0', 'date') }}

  **Overall: {{ state_attr('sensor.airhealth_other_allergens_day0', 'level_icon') }} {{ states('sensor.airhealth_other_allergens_day0') }}**

  {% for allergen in state_attr('sensor.airhealth_other_allergens_day0', 'allergens') %}
  - {{ allergen.level_icon }} **{{ allergen.name }}**: {{ allergen.level }}
  {% endfor %}
```

**Renders as:**
```
## Other Allergens - 2025-12-07

Overall: 🔴 Extreme

- 🟠 Plantain: High
- 🟡 Birch: Moderate
- 🟢 Olive: Low
```

## Recommendation

**Use Option B (Icons in Attributes)** because:
1. ✅ Keeps state clean for automations/scripts
2. ✅ Allows both simple display and detailed breakdowns
3. ✅ More flexible for UI customization
4. ✅ Follows Home Assistant conventions
5. ✅ Easy to template in Lovelace

## Implementation Steps

1. Add `get_level_icon()` function to `const.py`
2. Modify `extra_state_attributes()` in `sensor.py` to add `level_icon`
3. Add icons to allergen breakdown items
4. Update tests to verify new attributes
5. Create example Lovelace cards showing icon usage
6. Update README with attribute documentation

## File Changes Required

- `custom_components/airhealth/const.py` - Add helper function
- `custom_components/airhealth/sensor.py` - Modify attributes
- `lovelace-card-example.yaml` - Add icon display examples
- `custom_components/airhealth/tests/test_sensor.py` - Add attribute tests
- `README.md` - Document new attributes

## Migration Notes

- **Backward compatible**: Existing automations continue to work
- **State format unchanged**: Only adds new attributes
- **No breaking changes**: Pure enhancement

---

Ready to implement? This approach gives maximum flexibility while maintaining clean sensor states.
