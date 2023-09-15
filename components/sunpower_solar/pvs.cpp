#include "sunpower_solar.h"
#include "binary_sensor_map.h"
#include "sensor_map.h"
#include "text_sensor_map.h"

namespace esphome {
namespace sunpower_solar {

#ifdef USE_BINARY_SENSOR
const std::array<BinarySensorMap<PVS>, 1> PVS_BINARY_SENSOR_MAP = {
    {{&PVS::error_condition, "error_condition", "STATE", "error"}}};
#endif

#ifdef USE_TEXT_SENSOR
const std::array<TextSensorMap<PVS>, 2> PVS_TEXT_SENSOR_MAP = {
    {{&PVS::hardware_version, "hardware_version", "HWVER", false, nullopt},
     {&PVS::software_version, "software_version", "SWVER", false, nullopt}}};
#endif

void PVS::dump_config() {
  ESP_LOGCONFIG(TAG, "  PVS %s:", this->serial.c_str());

#ifdef USE_BINARY_SENSOR
  dump_config_for_sensors(*this, PVS_BINARY_SENSOR_MAP);
#endif

#ifdef USE_SENSOR
  LOG_SENSOR("    ", "energy_from_grid", this->energy_from_grid);
  LOG_SENSOR("    ", "energy_to_grid", this->energy_to_grid);
  LOG_SENSOR("    ", "power_from_grid", this->power_from_grid);
  LOG_SENSOR("    ", "power_to_grid", this->power_to_grid);
#endif

#ifdef USE_TEXT_SENSOR
  dump_config_for_sensors(*this, PVS_TEXT_SENSOR_MAP);
#endif
}

void PVS::setup_json_filter_keys(JsonObject &filter) {
#ifdef USE_BINARY_SENSOR
  add_filter_keys_for_sensors(*this, PVS_BINARY_SENSOR_MAP, filter);
#endif
#ifdef USE_TEXT_SENSOR
  add_filter_keys_for_sensors(*this, PVS_TEXT_SENSOR_MAP, filter);
#endif
}

void PVS::no_data() {
#ifdef USE_TEXT_SENSOR
  clear_no_data_sensors(*this, PVS_TEXT_SENSOR_MAP);
#endif
}

void PVS::process_data(const JsonObject &data) {
#ifdef USE_BINARY_SENSOR
  publish_sensors(*this, PVS_BINARY_SENSOR_MAP, data);
#endif
#ifdef USE_TEXT_SENSOR
  publish_sensors(*this, PVS_TEXT_SENSOR_MAP, data);
#endif
}

void PVS::publish_synthetic_sensors() {
#ifdef USE_SENSOR
  if ((this->power_from_grid != nullptr) or (this->power_to_grid != nullptr)) {
    float net_power =
        this->consumption_meter->active_power->get_raw_state() - this->production_meter->active_power->get_raw_state();

    if (this->power_from_grid != nullptr) {
      this->power_from_grid->publish_state(net_power > 0.0f ? net_power : 0.0f);
    }

    if (this->power_to_grid != nullptr) {
      this->power_to_grid->publish_state(net_power < 0.0f ? std::abs(net_power) : 0.0f);
    }
  }

  if ((this->energy_from_grid != nullptr) or (this->energy_to_grid != nullptr)) {
    if ((this->last_energy_consumption > 0.0f) or (this->last_energy_production > 0.0f)) {
      float energy_consumption = this->consumption_meter->lifetime_energy->get_raw_state() - this->last_energy_consumption;
      float energy_production = this->production_meter->lifetime_energy->get_raw_state() - this->last_energy_production;
      float net_energy = energy_consumption - energy_production;

      if (net_energy > 0.0f) {
        this->total_energy_from_grid += net_energy;
      } else if (net_energy < 0.0f) {
        this->total_energy_to_grid += std::abs(net_energy);
      }
    }

    if (this->energy_from_grid != nullptr) {
      this->energy_from_grid->publish_state(this->total_energy_from_grid);
    }

    if (this->energy_to_grid != nullptr) {
      this->energy_to_grid->publish_state(this->total_energy_to_grid);
    }

    this->last_energy_consumption = this->consumption_meter->lifetime_energy->get_raw_state();
    this->last_energy_production = this->production_meter->lifetime_energy->get_raw_state();
  }
#endif
}

}  // namespace sunpower_solar
}  // namespace esphome
