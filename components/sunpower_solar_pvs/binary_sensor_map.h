#pragma once

#include "sunpower_solar.h"
#include <array>
#include <functional>

namespace esphome {
namespace sunpower_solar {

#ifdef USE_BINARY_SENSOR

template<typename T> struct BinarySensorMap {
  binary_sensor::BinarySensor *T::*sensor;
  const char *key;
  std::string true_value;
};

template<typename T, std::size_t N>
void add_filter_keys_for_sensors(T &device, const std::array<BinarySensorMap<T>, N> &sensor_map,
                                 const JsonObject &filter) {
  for (const auto &item : sensor_map) {
    if (device.*(item.sensor) == nullptr) {
      continue;
    }

    filter[item.key] = true;
  }
}

template<typename T, std::size_t N>
void publish_sensors(T &device, const std::array<BinarySensorMap<T>, N> &sensor_map, const JsonObject &data) {
  for (const auto &item : sensor_map) {
    if (device.*(item.sensor) == nullptr) {
      continue;
    }

    if (!data.containsKey(item.key)) {
      ESP_LOGW("XXX", "Cannot update sensor '%s' because key '%s' is missing from data",
               (device.*(item.sensor))->get_name().c_str(), item.key);
      return;
    }

    std::string val = data[item.key];
    (device.*(item.sensor))->publish_state(val == item.true_value);
  }
}

#endif

}  // namespace sunpower_solar
}  // namespace esphome
