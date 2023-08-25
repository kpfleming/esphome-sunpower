#pragma once

#include "sunpower_solar.h"
#include <array>
#include <functional>

#ifdef USE_SENSOR

namespace esphome {
namespace sunpower_solar {

template<typename T> struct SensorMap {
  sensor::Sensor *T::*sensor;
  const char *config_label;
  const char *key;
  bool clear_on_no_data;
  optional<std::function<float(float)>> factor;
};

template<typename T, std::size_t N>
void dump_config_for_sensors(T &device, const std::array<SensorMap<T>, N> &sensor_map) {
  for (const auto &item : sensor_map) {
    LOG_SENSOR("    ", item.config_label, device.*(item.sensor));
  }
}

template<typename T, std::size_t N>
void add_filter_keys_for_sensors(T &device, const std::array<SensorMap<T>, N> &sensor_map, const JsonObject &filter) {
  for (const auto &item : sensor_map) {
    if (device.*(item.sensor) == nullptr) {
      continue;
    }

    filter[item.key] = true;
  }
}

template<typename T, std::size_t N>
void clear_no_data_sensors(T &device, const std::array<SensorMap<T>, N> &sensor_map) {
  for (const auto &item : sensor_map) {
    if (!item.clear_on_no_data) {
      continue;
    }
    if (device.*(item.sensor) == nullptr) {
      continue;
    }
    (device.*(item.sensor))->publish_state(NAN);
  }
}

template<typename T, std::size_t N>
void publish_sensors(T &device, const std::array<SensorMap<T>, N> &sensor_map, const JsonObject &data) {
  for (const auto &item : sensor_map) {
    if (device.*(item.sensor) == nullptr) {
      continue;
    }

    if (!data.containsKey(item.key)) {
      ESP_LOGW(TAG, "Cannot update sensor '%s' because key '%s' is missing from data",
               (device.*(item.sensor))->get_name().c_str(), item.key);
      return;
    }

    float val = data[item.key];
    if (item.factor.has_value()) {
      (device.*(item.sensor))->publish_state(item.factor.value()(val));
    } else {
      (device.*(item.sensor))->publish_state(val);
    }
  }
}

}  // namespace sunpower_solar
}  // namespace esphome

#endif
