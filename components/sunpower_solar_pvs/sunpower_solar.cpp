#include "sunpower_solar.h"

namespace esphome {
namespace sunpower_solar {

void SunpowerSolar::setup() {
  this->json_data_filter_ = new DynamicJsonDocument(this->json_data_filter_size_);  // NOLINT
  this->json_data_ = new DynamicJsonDocument(this->json_data_size_);                // NOLINT

  JsonObject filter_devices_0 = (*this->json_data_filter_)["devices"].createNestedObject();

  filter_devices_0["SERIAL"] = true;

  for (const auto &device : this->devices_) {
    device.second->setup_json_filter_keys(filter_devices_0);
  }

  if (this->json_data_filter_->overflowed()) {
    ESP_LOGW(TAG, "JSON filter overflowed: set sunpower_solar_pvs->buffer_size->filter to value higher than %zu",
             this->json_data_filter_size_);
    this->mark_failed();
  } else {
    ESP_LOGD(TAG, "JSON filter used %zu of %zu bytes", this->json_data_filter_->memoryUsage(),
             this->json_data_filter_->capacity());
  }

  if (!this->validate_arrays_()) {
    this->mark_failed();
  }
}

void SunpowerSolar::dump_config() { ESP_LOGCONFIG(TAG, "Sunpower Solar:"); }

void SunpowerSolar::process_data(std::vector<char> &data) {
  this->json_data_->clear();

  DeserializationError error = deserializeJson((*this->json_data_), data.data(), data.size(),
                                               DeserializationOption::Filter((*this->json_data_filter_)));

  if (error) {
    ESP_LOGE(TAG, "JSON deserialization failed: %s", error.c_str());
    return;
  }

  ESP_LOGD(TAG, "JSON deserialization used %zu of %zu bytes", this->json_data_->memoryUsage(),
           this->json_data_->capacity());

  JsonObject root = this->json_data_->as<JsonObject>();

  if (!root.containsKey("devices")) {
    ESP_LOGW(TAG, "PVS data does not contain 'devices' key");
    return;
  }

  auto unseen_serials = this->devices_;

  const JsonArray &devices = root["devices"];
  for (const auto &d : devices) {
    if (!d.containsKey("SERIAL")) {
      continue;
    }

    std::string serial = d["SERIAL"];

    ESP_LOGD(TAG, "Data found for device with serial %s", serial.c_str());

    auto search = this->devices_.find(serial);
    if (search == this->devices_.end()) {
      ESP_LOGW(TAG, "Serial '%s' not present in configuration", serial.c_str());
      continue;
    }

    search->second->process_data(d);
    unseen_serials.erase(serial);
#ifdef USE_BINARY_SENSOR
    if (search->second->error_condition != nullptr) {
      search->second->error_condition_no_data = false;
    }
#endif
  }

  for (const auto &device : unseen_serials) {
    ESP_LOGW(TAG, "No data found for serial %s", device.first.c_str());
    device.second->no_data();
#ifdef USE_BINARY_SENSOR
    if (device.second->error_condition != nullptr) {
      device.second->error_condition_no_data = true;
      device.second->error_condition->publish_state(true);
    }
#endif
  }

  // this must be done after setting sensors to 'no data', if any were
  this->publish_arrays_();

#ifdef USE_SENSOR
  // this must be done after all devices have been processed
  this->pvs_->publish_synthetic_sensors();
#endif
}

}  // namespace sunpower_solar
}  // namespace esphome
