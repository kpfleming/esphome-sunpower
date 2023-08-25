# esphome-sunpower

<a href="https://opensource.org"><img height="150" align="left" src="https://opensource.org/files/OSIApprovedCropped.png" alt="Open Source Initiative Approved License logo"></a>
[![License - GNU GPL v3.0+](https://img.shields.io/badge/License-GNU%20GPL%203.0%2b-9400d3.svg)](https://spdx.org/licenses/GPL-3.0-or-later.html)

This repo contains a series of experimental ESPHome components which
gather data from SunPower PV Supervisor (PVS) devices.

Open Source software: [GNU General Public License v3.0 or later](https://spdx.org/licenses/GPL-3.0-or-later.html)

## &nbsp;

## Comparison with other integrations

The most commonly used other integration is
[hass-sunpower](https://github.com/krbaker/hass-sunpower), so this
comparison focuses on the differences between it and esphome-sunpower.

### Advantages

#### Synthesized 'from grid' and 'to grid' sensors

hass-sunpower reports the 'kWh from Grid' and 'kWh to Grid' sensors
from the PVS, when they are available. Unfortunately they are not
always available, and so to improve consistency esphome-sunpower
synthesizes its own sensors. Users can choose to use them or not, as
their needs dictate. In addition, the PVS only provides *energy*
sensors of this type, but esphome-sunpower also provides *power*
sensors.

#### Explicit control over sensor visibility and names

ESPHome configurations require explicit enablement of every sensor to
be reported to HA (opt-in), which is a different design from Home
Assistant integrations which typically don't offer such controls. Home
Assistant itself provides the ability to 'hide' and even 'disable'
sensors being reported by an integration, but this does not remove
them from the overall system configuration.

Home Assistant also allows users to override sensor names, but these
overrides are lost if the integration is ever deleted from the Home
Assistant configuration and re-added. ESPHome's usage of a separate
configuration system means that the user's defined sensor names will
always be used, even if the ESPHome device is deleted from the Home
Assistant configuration and re-added (or added to another Home
Assistant instance).

#### Support for aggregating panels into arrays

Some SunPower customers have panels in arrays (strings), on separate
roof surfaces and oriented in different directions. esphome-sunpower
provides the ability to aggregate current, power, and energy sensors
from the panels in each array and present these to HA as 'array'
sensors.

#### Ability to manipulate sensor data before it is delivered to Home Assistant

While it is unlikely to be needed frequently, some users may wish to
manipulate PVS sensor data before displaying it in Home Assistant
dashboards. Using hass-sunpower, those modifications must be done by
creating `template sensors` in Home Assistant, and then hiding the
original sensor. With esphome-sunpower, various types of data
filtering and manipulation can be performed directly in the ESPHome
configuration, with only the resulting data delivered to Home
Assistant (and no 'extra' sensors).

#### Reduction of startup time and workload in Home Assistant

Because the PVS responds to API queries so slowly (see the [PVS Data
Collection](#pvs-data-collection) section below), users of
hass-sunpower are warned during Home Assistant startup that the
'integration is taking too long to startup', even though there is
nothing wrong. This also results in delays for data being delivered to
dashboards. Using esphome-sunpower, the data collection is happening
outside of Home Assistant, and is immediately available the moment
that Home Assistant connects to the ESPHome device. Even with more
than 100 sensors in the esphome-sunpower configuration, delivery of
the most current data for those sensors to Home Assistant happens
almost instantly during startup.

#### Reduction of Home Assistant 'Recorder' database growth

Because the esphome-sunpower user controls the number and type of
sensors to be reported to Home Assistant, they have complete control
over the growth of the Recorder database. Hiding sensors in Home
Assistant doesn't stop them from being stored in the database, so
hass-sunpowers users are often storing much more data than they
actually need.

#### Direct publication of data to InfluxDB

Some PVS users store their long-term solar data in InfluxDB; using
hass-sunpower means that this data must go into Home Assistant before
being pushed to InfluxDB. esphome-sunpower users can make use of
InfluxDB components for ESPHome itself, ensuring that the data always
flows to InfluxDB without needing Home Assistant's help.

### Disadvantages

#### Lack of 'device' support

ESPHome does not currently support the Home Assistant Device Registry
in a way which allows components to associate entities (sensors, etc.)
with multiple devices. As a result all of the sensors enabled in an
esphome-sunpower configuration will appear under a single device in
Home Assistant. There is a proposal to enhance ESPHome to provide
support for this, though, see the [Roadmap](#roadmap) section below.

#### Requires additional hardware

Until ESPHome supports multiple network connections in a single device
(allowing the ESP32 device to be installed in the PVS cabinet, see the
[Roadmap](#roadmap) section below), esphome-sunpower users need *both*
a device in the PVS cabinet to provide connectivity to the PVS `LAN`
port *and* an ESP32 device to collect and process the data.

## Requirements

* One or more SunPower PVS 6 (may also work with PVS 5).
* An ESP32-based device; note that this has only been tested with the
  original ESP32 (dual-core Tensilica 240MHz CPU, 520KB SRAM) with at
  least 4MB of flash memory attached. The other ESP32 variants are
  likely to be usable, depending on the complexity of the PVS networks
  being monitored and the number of individual sensors enabled in the
  configuration. The device should be dedicated to PVS
  monitoring. Since there are no GPIOs used, any ESP32 board will
  work.
* Network connectivity between the ESP32, the PVS, and Home Assistant,
  on a *single* network connection; if dual network connectivity
  becomes available in a future ESPHome release, this requirement
  would be eliminated and the ESP32 device could be installed in the
  PVS cabinet in place of any other device used for the _LAN_ network
  connection. If you don't already have connectivity to the PVS, you
  should review the [long
  topic](https://community.home-assistant.io/t/options-for-sunpower-solar-integration/289621)
  on the Home Assistant Discourse forum to learn about your options.

## PVS Data Collection

Throughout the examples in this documentation, you will see a `<PVS>`
placeholder; in your actual configuration you will need to replace
this with the IP address you've made available to reach the PVS (or
the DNS name, if you've setup DNS for it and your ESP32 is able to use
DNS.)

The PVS responds to the data collection API request quite slowly; in a
configuration with 37 panels, the response takes between 9 and 10
seconds in most cases. As a result, the example configurations include
an override for the ESP-IDF 'watchdog timer' to ensure that the ESP32
won't be restarted while waiting for the response. This is a rather
inelegant workaround, but it is necessary until such time as ESPHome
can issue HTTP requests and wait for responses in an asynchronous
manner. If your PVS takes longer than 10 seconds to respond, you may
need to increase the watchdog timeout correspondingly (be sure to
leave a few seconds buffer in case there are any network traffic
problems which might increase the response time).

You will need to determine two buffer sizes to be used in the ESPHome
configuration:

* `http_request->rx_buffer_size`: this needs to be large enough to
  hold the entire response from the PVS (see below).

* `sunpower_solar_pvs->buffer_size->data`: this needs to be large
  enough to hold the portion of the JSON data from the PVS that is
  used to populate the sensors. In a configuration with _all_ sensors
  enabled it needs to be about 25% of the `rx_buffer_size`, but if
  fewer sensors are enabled it can be reduced.

To determine the buffer sizes required for your configuration and
confirm that you have PVS connectivity, you can use `curl`:

```shell
$ curl -o pvs-data.json http://<PVS>/cgi-bin/dl_cgi?Command=DeviceList
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 31195  100 31195    0     0   3385      0  0:00:09  0:00:09 --:--:--  7789
```

The resulting `pvs-data.json` file should look similar to the one in
the [examples directory](examples). You will need this file in order
to build your configuration, since it contains the serial numbers of
all of the SunPower devices.

In the output above you can see that the transfer took 9 seconds, and
the resulting JSON document was 31,195 bytes long. For that system,
`rx_buffer_size` should be set to 34000, and `buffer_size->data`
should be set to 10000 if all sensors are enabled.

Once the system is running you can monitor the logs (with
`logger->level` set to `debug`) to see how much of the JSON data buffer
is being used; if a large portion is unused, reconfigure for a lower
size, but be prepared to increase it again if you enable more
sensors. If the JSON data buffer is not large enough, an error will
be emitted in the logs and no sensor data will be published.

## Configuration

The ESPHome 'logger' defaults to `debug` level; while this can be
useful for troubleshooting ESPHome configurations, it also means that
sensor data publication can be slowed down substantially. If you have
the level set to `debug`, and you enable more than 7 or 8 sensors in
total in the esphome-sunpower component, then you will see a warning
in the ESPHome log every time esphome-sunpower publishes data. The
warning will indicate that component `sunpower_solar_pvs` too *too
much time* to do its work, but if as suggested previously you've
dedicated an ESP32 board for this task, then you can safely ignore the
warning as no other important ESPHome activities will be missed.

You will see the same type of warning for the `http_request`
component, since it will block ESPHome activities for many seconds
while it waits for a response from the PVS.

This component relies on a not-yet-merged version of the ESPHome
`http_request` component; that version is compatible with the ESP-IDF
framework, and also improves the way that HTTP responses are made
available to automations. Those improvements allow esphome-sunpower to
avoid copying the entire response while parsing it, which would
dramatically increase overall RAM requirements.

### Minimal

This section is a walkthrough of [minimal.yml](examples/minimal.yml)
from the `examples` directory. It is the most basic configuration
needed to support the Home Assistant 'Energy Dashboard' (which
requires three sensors).

```yaml
esphome:
  name: pvs-minimal
  friendly_name: Minimal PVS Monitor

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
issues described in the [PVS Data Collection](pvs-data-collection)
section.

```yaml
external_components:
  - source: github://pr#3256
    components: [ http_request ]
  - source: github://kpfleming/esphome-sunpower@v2
```

This configuration requires two external components; esphome-sunpower,
and the modified version of `http_request` as noted in the
[Configuration](#configuration) section.

```yaml
sunpower_solar:
  id: solar
  serial: PVS1
  consumption_meter:
    serial: CM1
  production_meter:
    serial: PM1
```

This section configures esphome-sunpower to accept data from the
PVS, including its consumption meter and production meter. The serial
numbers of all three components must be specified, and they can be
obtained from the JSON data file gathered while following the steps in
[PVS Data Collection](pvs-data-collection).

Since this configuration only publishes data for three sensors, the
default values for the esphome-sunpower buffer sizes are sufficient,
and they are not included in the example configuration.

```yaml
sensor:
  - platform: sunpower_solar

    energy_from_grid: Energy From Grid
    energy_to_grid: Energy To Grid

    consumption_meter:
      lifetime_energy:
        name: Energy Consumed
        internal: true

    production_meter:
      lifetime_energy: Energy Produced
```

This section configures the three sensors required by the Energy Dashboard:

* Energy From Grid

* Energy To Grid

* Energy Produced

In addition an `Energy Consumed` sensor is configured but marked as
`internal` so it will not be published to Home Assistant. It is
required for the `Energy From Grid` and `Energy To Grid` sensor
calculations.

```yaml
http_request:
  useragent: esphome/pvs
  rx_buffer_size: 35000
```

This section configures the `http_request` component; see the [PVS
Data Collection](pvs-data-collection) section for details about
`rx_buffer_size`.

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

### Full Featured

See [FULL_CONFIGURATION](FULL_CONFIGURATION.md).

## Roadmap

### Device Support

The author of these components also plans to work on 'connected
device' support for ESPHome, which would resolve one of the major
differences between this integration and hass-sunpower. If you are
interested, you can follow the [feature-requests
issue](https://github.com/esphome/feature-requests/issues/1335).

### Dual Network Support

There is an open [feature-requests
issue](https://github.com/esphome/feature-requests/issues/2102) on
this topic; the author of these components may try to tackle that one
too at some point in the near future!

## Issues, Feature Requests, Discussions

If you need to report an issue, or suggest a new feature, please do so
in the
['Issues'](https://github.com/kpfleming/esphome-sunpower/issues) area
of this repository.

If you'd like to discuss usage of these components, or ask for help
with them (but not with ESPHome itself or PVS connectivity), please do
so in the
['Discussions'](https://github.com/kpfleming/esphome-sunpower/discussions)
area of this repository.

## Chat

If you'd like to chat with the esphome-sunpower community, join us on
[Matrix](https://matrix.to/#/#esphome-sunpower:km6g.us)!

## Credits

This project was inspired by the excellent
[hass-sunpower](https://github.com/krbaker/hass-sunpower) project by
[@krbaker](https://github.com/krbaker).
