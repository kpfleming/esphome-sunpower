#pragma once

#include "sunpower_solar.h"
#include <array>
#include <functional>

#ifdef USE_TEXT_SENSOR

namespace esphome {
namespace sunpower_solar {

template<typename T> struct TextSensorMap {
  text_sensor::TextSensor *T::*sensor;
  const char *config_label;
  const char *key;
  bool clear_on_no_data;
  optional<std::function<std::string(std::string)>> transform;
};

template<typename T, std::size_t N>
void dump_config_for_sensors(T &device, const std::array<TextSensorMap<T>, N> &sensor_map) {
  for (const auto &item : sensor_map) {
    LOG_TEXT_SENSOR("    ", item.config_label, device.*(item.sensor));
  }
}

template<typename T, std::size_t N>
void add_filter_keys_for_sensors(T &device, const std::array<TextSensorMap<T>, N> &sensor_map,
                                 const JsonObject &filter) {
  for (const auto &item : sensor_map) {
    if (device.*(item.sensor) == nullptr) {
      continue;
    }

    filter[item.key] = true;
  }
}

template<typename T, std::size_t N>
void clear_no_data_sensors(T &device, const std::array<TextSensorMap<T>, N> &sensor_map) {
  for (const auto &item : sensor_map) {
    if (!item.clear_on_no_data) {
      continue;
    }
    if (device.*(item.sensor) == nullptr) {
      continue;
    }
    (device.*(item.sensor))->publish_state("");
  }
}

template<typename T, std::size_t N>
void publish_sensors(T &device, const std::array<TextSensorMap<T>, N> &sensor_map, const JsonObject &data) {
  for (const auto &item : sensor_map) {
    if (device.*(item.sensor) == nullptr) {
      continue;
    }

    if (!data.containsKey(item.key)) {
      ESP_LOGW(TAG, "Cannot update sensor '%s' because key '%s' is missing from data",
               (device.*(item.sensor))->get_name().c_str(), item.key);
      return;
    }

    std::string val = data[item.key];
    if (item.transform.has_value()) {
      (device.*(item.sensor))->publish_state(item.transform.value()(val));
    } else {
      (device.*(item.sensor))->publish_state(val);
    }
  }
}

}  // namespace sunpower_solar
}  // namespace esphome

#endif
