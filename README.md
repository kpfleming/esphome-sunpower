# esphome-sunpower

<a href="https://opensource.org"><img height="150" align="left" src="https://opensource.org/files/OSIApprovedCropped.png" alt="Open Source Initiative Approved License logo"></a>
[![License - GNU GPL v3.0+](https://img.shields.io/badge/License-GNU%20GPL%203.0%2b-9400d3.svg)](https://spdx.org/licenses/GPL-3.0-or-later.html)

This repo contains a series of experimental ESPHome components which
gather data from SunPower PV Supervisor (PVS) devices.

Open Source software: [GNU General Public License v3.0 or later](https://spdx.org/licenses/GPL-3.0-or-later.html)

## &nbsp;

## Comparison with other integrations

synthesized sensors
control over sensor data/visibility/names/filters outside of HA
elimination of HA startup time/reduced HA workload on low-power systems
reduction of recorder database growth
array support
lack of devices

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

* `sunpower_solar_pvs->buffer_size->data': this needs to be large
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
`logger_level` set to `debug`) to see how much of the JSON data buffer
is being used; if a large portion is unused, reconfigure for a lower
size, but be prepared to increase it again if you enable more
sensors. If the JSON data buffer is not large enough, a warning will
be emitted in the logs.

## Configuration

### Minimal

### Full Featured

## Roadmap

device support
dual network support

## Issues, Feature Requests, Discussions

If you need to report an issue, or suggest a new feature, please do so
in the 'Issues' area of this repository.

If you'd like to discuss usage of these components, or ask for help
with them (but not with ESPHome itself or PVS connectivity), please do
so in the 'Discussions' area of this repository.

## Chat

If you'd like to chat with the esphome-sunpower community, join us on
[Matrix](https://matrix.to/#/#esphome-sunpower:km6g.us)!

## Credits

This project was inspired by the excellent
[hass-sunpower](https://github.com/krbaker/hass-sunpower) project by
[@krbaker](https://github.com/krbaker).
