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
JSON filter and JSON data buffer sizes have been specified, since the
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

## full.yml

```yaml
esphome:
  name: pvs-full
  friendly_name: Full PVS Monitor

esp32:
  board: esp32dev
  framework:
    type: esp-idf
    sdkconfig_options:
      CONFIG_ESP_TASK_WDT_TIMEOUT_S: "15"

wifi:
  networks:
    - ssid: example-network
      password: network-password

api:
```

This section fulfills basic ESPHome requirements: node information,
board selection, and WiFi/API connectivity. The only relevant item
here is `CONFIG_ESP_TASK_WDT_TIMEOUT_S`, which is necessary due to the
issues described in the [PVS Data
Collection](README.md#pvs-data-collection) section.

```yaml
external_components:
  - source: github://pr#3256
    components: [ http_request ]
  - source: github://kpfleming/esphome-sunpower@v1
```

This configuration requires two external components; esphome-sunpower,
and the modified version of `http_request` as noted in the
[Configuration](README.md#configuration) section. Unlike the minimal
example it enables all components in the esphome-sunpower
package.

```yaml
packages:
  solar: !include
    file: packages/sunpower_solar_pvs.yml
    vars:
      pvs_serial: ZT215185000549A0754
      consumption_meter_serial: PVS6M21510754c
      production_meter_serial: PVS6M21510754p
```

This section configures esphome-sunpower to accept data from the PVS,
using the [sunpower_solar_pvs.yml](#sunpower_solar_pvsyml) package.

```yaml
  panel_A01: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A01
      serial: E00122208054945
  panel_A02: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A02
      serial: E00122208048594
  panel_A03: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A03
      serial: E00122208026527
  panel_A04: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A04
      serial: E00122208055109
  panel_A05: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A05
      serial: E00122208056185
  panel_A06: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A06
      serial: E00122208055824
  panel_A07: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A07
      serial: E00122208056231
  panel_A08: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A08
      serial: E00122208048581
  panel_A09: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A09
      serial: E00122208007432
  panel_A10: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A10
      serial: E00122208055167
  panel_A11: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A11
      serial: E00122208053964
  panel_A12: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: A12
      serial: E00122208055132
  panel_B01: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: B01
      serial: E00122149010334
  panel_B02: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: B02
      serial: E00122149010456
  panel_B03: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: B03
      serial: E00122149011266
  panel_B04: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: B04
      serial: E00122149011275
  panel_B05: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: B05
      serial: E00122148074610
  panel_B06: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: B06
      serial: E00122149011975
  panel_B07: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: B07
      serial: E00122149011268
  panel_B08: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: B08
      serial: E00122149019431
  panel_B09: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: B09
      serial: E00122149010367
  panel_B10: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: B10
      serial: E00122149022131
  panel_C01: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: C01
      serial: E00122208047681
  panel_C02: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: C02
      serial: E00122208051475
  panel_C03: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: C03
      serial: E00122149016130
  panel_C04: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: C04
      serial: E00122149008705
  panel_C05: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: C05
      serial: E00122149014900
  panel_C06: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: C06
      serial: E00122149012405
  panel_C07: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: C07
      serial: E00122149015711
  panel_C08: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: C08
      serial: E00122149016647
  panel_D01: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: D01
      serial: E00122208051661
  panel_D02: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: D02
      serial: E00122208051548
  panel_D03: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: D03
      serial: E00122208055105
  panel_D04: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: D04
      serial: E00122208053577
  panel_D05: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: D05
      serial: E00122208007603
  panel_E01: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: E01
      serial: E00122208054182
  panel_E02: !include
    file: packages/sunpower_solar_panel.yml
    vars:
      panel: E02
      serial: E00122208054404
```

This section configures esphome-sunpower to accept data for all of the
panels attached to the PVS, using the
[sunpower_solar_panel.yml](#sunpower_solar_panelyml) package.

```yaml
  array_A: !include
    file: packages/sunpower_solar_array.yml
    vars:
      array: A
  array_B: !include
    file: packages/sunpower_solar_array.yml
    vars:
      array: B
  array_C: !include
    file: packages/sunpower_solar_array.yml
    vars:
      array: C
  array_D: !include
    file: packages/sunpower_solar_array.yml
    vars:
      array: D
  array_E: !include
    file: packages/sunpower_solar_array.yml
    vars:
      array: E
```

This section configures esphome-sunpower to aggregate panel data into
five arrays, using the
[sunpower_solar_array.yml](#sunpower_solar_arrayyml) package.

```yaml
sunpower_solar_array:
  - id: array_A
    name: Array A
    panels:
      - panel_A01
      - panel_A02
      - panel_A03
      - panel_A04
      - panel_A05
      - panel_A06
      - panel_A07
      - panel_A08
      - panel_A09
      - panel_A10
      - panel_A11
      - panel_A12

  - id: array_B
    name: Array B
    panels:
      - panel_B01
      - panel_B02
      - panel_B03
      - panel_B04
      - panel_B05
      - panel_B06
      - panel_B07
      - panel_B08
      - panel_B09
      - panel_B10

  - id: array_C
    name: Array C
    panels:
      - panel_C01
      - panel_C02
      - panel_C03
      - panel_C04
      - panel_C05
      - panel_C06
      - panel_C07
      - panel_C08

  - id: array_D
    name: Array D
    panels:
      - panel_D01
      - panel_D02
      - panel_D03
      - panel_D04
      - panel_D05

  - id: array_E
    name: Array E
    panels:
      - panel_E01
      - panel_E02
```

This section identifies the panels which should be aggregated into
each of the five arrays.

```yaml
http_request:
  useragent: esphome/pvs
  rx_buffer_size: 35000
```

This section configures the `http_request` component; see the [PVS
Data Collection](README.md#pvs-data-collection) section for details
about `rx_buffer_size`.

```yaml
time:
  - platform: homeassistant
    timezone: EST5EDT,M3.2.0,M11.1.0
    on_time:
      - seconds: 45
        minutes: '*'
        then:
          - http_request.get:
              url: http://<PVS>/cgi-bin/dl_cgi?Command=DeviceList
              capture_response: true
              on_response:
                then:
                  - delay: 3s
                  - lambda: id(solar).process_data(response.data);
```

This final section configures a `time` component so that ESPHome can
periodically pull data from the PVS and push it to
esphome-sunpower. The example uses the `homeassistant` time platform,
but you can use any time platform you wish.

The `on_time` trigger is used to poll the PVS every minute (at 45
seconds into the minute), capture the response, wait three seconds
(for other activities in ESPHome, which were blocked during the HTTP
request, to be processed), and then supply the response to
esphome-sunpower for parsing and sensor publication.
