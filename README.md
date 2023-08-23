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
inelegant workarond, but it is necessary until such time as ESPHome
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
the [examples directory](examples).

In the output above you can see that the transfer took 9 seconds, and
the resulting JSON document was 31,195 bytes long. For that system,
`rx_buffer_size` should be set to 34000, and `buffer_size->data`
should be set to 10000 if all sensors are enabled.

Once the system is running you can monitor the logs (with
`logger->level` set to `debug`) to see how much of the JSON data buffer
is being used; if a large portion is unused, reconfigure for a lower
size, but be prepared to increase it again if you enable more
sensors. If the JSON data buffer is not large enough, a warning will
be emitted in the logs.

## Configuration

logger level
http_request

### Minimal

### Full Featured

## Roadmap

device support
dual network support

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
