#include "sunpower_solar.h"
#include "binary_sensor_map.h"
#include "sensor_map.h"
#include "text_sensor_map.h"

namespace esphome {
namespace sunpower_solar {

#ifdef USE_BINARY_SENSOR
const std::array<BinarySensorMap<ConsumptionMeter>, 1> CONSUMPTION_METER_BINARY_SENSOR_MAP = {
    {{&ConsumptionMeter::error_condition, "error_condition", "STATE", "error"}}};
#endif

#ifdef USE_SENSOR
const std::array<SensorMap<ConsumptionMeter>, 12> CONSUMPTION_METER_SENSOR_MAP = {
    {{&ConsumptionMeter::active_power, "active_power", "p_3phsum_kw", true, nullopt},
     {&ConsumptionMeter::apparent_power, "apparent_power", "s_3phsum_kva", true,
      std::function<float(float)>([](float val) -> float { return val * 1000.0f; })},
     {&ConsumptionMeter::lifetime_energy, "lifetime_energy", "net_ltea_3phsum_kwh", false, nullopt},
     {&ConsumptionMeter::power_factor, "power_factor", "tot_pf_rto", true,
      std::function<float(float)>([](float val) { return val * 100.0f; })},
     {&ConsumptionMeter::reactive_power, "reactive_power", "q_3phsum_kvar", true,
      std::function<float(float)>([](float val) { return val * 1000.0f; })},
     {&ConsumptionMeter::voltage, "voltage", "v12_v", true, nullopt},
     {&ConsumptionMeter::phase_a_active_power, "phase_a active_power", "p1_kw", true, nullopt},
     {&ConsumptionMeter::phase_a_current, "phase_a current", "i1_a", true, nullopt},
     {&ConsumptionMeter::phase_a_voltage, "phase_a voltage", "v1n_v", true, nullopt},
     {&ConsumptionMeter::phase_b_active_power, "phase_b active_power", "p2_kw", true, nullopt},
     {&ConsumptionMeter::phase_b_current, "phase_b current", "i2_a", true, nullopt},
     {&ConsumptionMeter::phase_b_voltage, "phase_b voltage", "v2n_v", true, nullopt}}};
#endif

#ifdef USE_TEXT_SENSOR
const std::array<TextSensorMap<ConsumptionMeter>, 1> CONSUMPTION_METER_TEXT_SENSOR_MAP = {
    {{&PVS::software_version, "software_version", "SWVER", false, nullopt}}};
#endif

void ConsumptionMeter::dump_config() {
  ESP_LOGCONFIG(TAG, "  Consumption Meter %s:", this->serial.c_str());

#ifdef USE_BINARY_SENSOR
  dump_config_for_sensors(*this, CONSUMPTION_METER_BINARY_SENSOR_MAP);
#endif

#ifdef USE_SENSOR
  dump_config_for_sensors(*this, CONSUMPTION_METER_SENSOR_MAP);
#endif

#ifdef USE_TEXT_SENSOR
  dump_config_for_sensors(*this, CONSUMPTION_METER_TEXT_SENSOR_MAP);
#endif
}

void ConsumptionMeter::setup_json_filter_keys(JsonObject &filter) {
#ifdef USE_BINARY_SENSOR
  add_filter_keys_for_sensors(*this, CONSUMPTION_METER_BINARY_SENSOR_MAP, filter);
#endif
#ifdef USE_SENSOR
  add_filter_keys_for_sensors(*this, CONSUMPTION_METER_SENSOR_MAP, filter);
#endif
#ifdef USE_TEXT_SENSOR
  add_filter_keys_for_sensors(*this, CONSUMPTION_METER_SENSOR_MAP, filter);
#endif
}

void ConsumptionMeter::no_data() {
#ifdef USE_SENSOR
  clear_no_data_sensors(*this, CONSUMPTION_METER_SENSOR_MAP);
#endif
#ifdef USE_TEXT_SENSOR
  clear_no_data_sensors(*this, CONSUMPTION_METER_TEXT_SENSOR_MAP);
#endif
}

void ConsumptionMeter::process_data(const JsonObject &data) {
#ifdef USE_BINARY_SENSOR
  publish_sensors(*this, CONSUMPTION_METER_BINARY_SENSOR_MAP, data);
#endif
#ifdef USE_SENSOR
  publish_sensors(*this, CONSUMPTION_METER_SENSOR_MAP, data);
#endif
#ifdef USE_TEXT_SENSOR
  publish_sensors(*this, CONSUMPTION_METER_TEXT_SENSOR_MAP, data);
#endif
}

}  // namespace sunpower_solar
}  // namespace esphome
