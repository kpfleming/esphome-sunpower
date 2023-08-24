# Full Configuration Example

The [full.yml](examples/full.yml) example enables every sensor
available in esphome-sunpower. As a result it consumes a substantial
amount of flash memory space, and will also generate *too much time*
warnings on every data collection cycle.

This configuration represents a real-world installation with one PVS6
and 37 panels, with the panels arranged in five separate arrays.

## Configuration Style

This configuration makes substantial use of the [Packages as
Templates](https://esphome.io/guides/configuration-types#packages-as-templates)
model available in ESPHome; this is done to reduce redundancy,
increase consistency, and simplify adding/removing sensors from all
panels (or arrays) at once.

All of the packages accept a variable called `node_friendly_name`
which they use as a prefix for sensor names.

## sunpower_solar_pvs.yml

```yaml
sunpower_solar_pvs:
  id: solar
  serial: ${pvs_serial}
  buffer_size:
    filter: 1024
    data: 10000
  consumption_meter:
    serial: ${consumption_meter_serial}
  production_meter:
    serial: ${production_meter_serial}

sensor:
  - platform: sunpower_solar_pvs

    energy_from_grid: ${node_friendly_name} Energy From Grid
    energy_to_grid: ${node_friendly_name} Energy To Grid
    power_from_grid: ${node_friendly_name} Power From Grid
    power_to_grid: ${node_friendly_name} Power To Grid

    consumption_meter:
      voltage: ${node_friendly_name} Consumption Voltage
      active_power: ${node_friendly_name} Consumption Active Power
      apparent_power: ${node_friendly_name} Consumption Apparent Power
      reactive_power: ${node_friendly_name} Consumption Reactive Power
      power_factor: ${node_friendly_name} Consumption Power Factor
      lifetime_energy: ${node_friendly_name} Consumption Lifetime Energy
      phase_a:
        current: ${node_friendly_name} Consumption Phase A Current
        voltage: ${node_friendly_name} Consumption Phase A Voltage
        active_power: ${node_friendly_name} Consumption Phase A Active Power
      phase_b:
        current: ${node_friendly_name} Consumption Phase B Current
        voltage: ${node_friendly_name} Consumption Phase B Voltage
        active_power: ${node_friendly_name} Consumption Phase B Active Power

    production_meter:
      current: ${node_friendly_name} Production Current
      voltage: ${node_friendly_name} Production Voltage
      active_power: ${node_friendly_name} Production Active Power
      apparent_power: ${node_friendly_name} Production Apparent Power
      reactive_power: ${node_friendly_name} Production Reactive Power
      power_factor: ${node_friendly_name} Production Power Factor
      lifetime_energy: ${node_friendly_name} Production Lifetime Energy

binary_sensor:
  - platform: sunpower_solar_pvs

    error_condition: ${node_friendly_name} PVS Error

    consumption_meter:
      error_condition: ${node_friendly_name} Consumption Meter Error

    production_meter:
      error_condition: ${node_friendly_name} Production Meter Error

text_sensor:
  - platform: sunpower_solar_pvs

    hardware_version: ${node_friendly_name} PVS Hardware Version
    software_version: ${node_friendly_name} PVS Software Version

    consumption_meter:
      software_version: ${node_friendly_name} Consumption Meter Software Version

    production_meter:
      software_version: ${node_friendly_name} Production Meter Software Version
```

This package configures esphome-sunpower to accept data from a
PVS, including its consumption meter and production meter. The serial
numbers of all three components are specified using substitution variables.

Since this configuration publishes data for hundreds of sensors, the
JSON filter and JSON data buffer sizes has been specified, since the
default sizes would be insufficient.

## sunpower_solar_panel.yml

```yaml
sunpower_solar_panel:
  - id: panel_${panel}
    name: ${panel}
    serial: ${serial}

sensor:
  - platform: sunpower_solar_panel
    panel_${panel}:
      current: ${node_friendly_name} ${panel} Current
      voltage: ${node_friendly_name} ${panel} Voltage
      power: ${node_friendly_name} ${panel} Active Power
      lifetime_energy: ${node_friendly_name} ${panel} Lifetime Energy
      temperature: ${node_friendly_name} ${panel} Temperature

binary_sensor:
  - platform: sunpower_solar_panel
    panel_${panel}:
      error_condition: ${node_friendly_name} ${panel} Error

text_sensor:
  - platform: sunpower_solar_panel
    panel_${panel}:
      hardware_version: ${node_friendly_name} ${panel} Hardware Version
      software_version: ${node_friendly_name} ${panel} Software Version
```

This package configures esphome-sunpower to map incoming panel data to
the various sensors available for an individual panel. The package
accepts a `panel` variable which provides a human-friendly identity of
the panel, and a `serial` variable which provides the panel's serial
number.

## sunpower_solar_array.yml

```yaml
sensor:
  - platform: sunpower_solar_array
    array_${array}:
      current: ${node_friendly_name} Array ${array} Current
      power: ${node_friendly_name} Array ${array} Active Power
      lifetime_energy: ${node_friendly_name} Array ${array} Lifetime Energy
```

This package configures esphome-sunpower to create sensors for an
array. The package accepts a `array` variable which provides a
human-friendly identity of the array, but does not provide a way to
indicate which panels should be considered part of the array since the
ESPHome substitution mechanism doesn't offer a method to do that. The
mapping of panels to arrays is included in the actual configuration
file below.
