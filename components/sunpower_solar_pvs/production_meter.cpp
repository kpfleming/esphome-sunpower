#include "sunpower_solar.h"
#include "binary_sensor_map.h"
#include "sensor_map.h"
#include "text_sensor_map.h"

namespace esphome {
namespace sunpower_solar {

#ifdef USE_BINARY_SENSOR
const std::array<BinarySensorMap<ProductionMeter>, 1> PRODUCTION_METER_BINARY_SENSOR_MAP = {
    {{&ProductionMeter::error_condition, "STATE", "error"}}};
#endif

#ifdef USE_SENSOR
const std::array<SensorMap<ProductionMeter>, 7> PRODUCTION_METER_SENSOR_MAP = {
    {{&ProductionMeter::active_power, "p_3phsum_kw", true, nullopt},
     {&ProductionMeter::apparent_power, "s_3phsum_kva", true,
      std::function<float(float)>([](float val) -> float { return val * 1000.0f; })},
     {&ProductionMeter::current, "i_a", true, nullopt},
     {&ProductionMeter::lifetime_energy, "net_ltea_3phsum_kwh", false, nullopt},
     {&ProductionMeter::power_factor, "tot_pf_rto", true,
      std::function<float(float)>([](float val) { return val * 100.0f; })},
     {&ProductionMeter::reactive_power, "q_3phsum_kvar", true,
      std::function<float(float)>([](float val) { return val * 1000.0f; })},
     {&ProductionMeter::voltage, "v12_v", true, nullopt}}};
#endif

#ifdef USE_TEXT_SENSOR
const std::array<TextSensorMap<ProductionMeter>, 1> PRODUCTION_METER_TEXT_SENSOR_MAP = {
    {{&PVS::software_version, "SWVER", false, nullopt}}};
#endif

void ProductionMeter::setup_json_filter_keys(JsonObject &filter) {
#ifdef USE_BINARY_SENSOR
  add_filter_keys_for_sensors(*this, PRODUCTION_METER_BINARY_SENSOR_MAP, filter);
#endif
#ifdef USE_SENSOR
  add_filter_keys_for_sensors(*this, PRODUCTION_METER_SENSOR_MAP, filter);
#endif
#ifdef USE_TEXT_SENSOR
  add_filter_keys_for_sensors(*this, PRODUCTION_METER_SENSOR_MAP, filter);
#endif
}

void ProductionMeter::no_data() {
#ifdef USE_SENSOR
  clear_no_data_sensors(*this, PRODUCTION_METER_SENSOR_MAP);
#endif
#ifdef USE_TEXT_SENSOR
  clear_no_data_sensors(*this, PRODUCTION_METER_TEXT_SENSOR_MAP);
#endif
}

void ProductionMeter::process_data(const JsonObject &data) {
#ifdef USE_BINARY_SENSOR
  publish_sensors(*this, PRODUCTION_METER_BINARY_SENSOR_MAP, data);
#endif
#ifdef USE_SENSOR
  publish_sensors(*this, PRODUCTION_METER_SENSOR_MAP, data);
#endif
#ifdef USE_TEXT_SENSOR
  publish_sensors(*this, PRODUCTION_METER_TEXT_SENSOR_MAP, data);
#endif
}

}  // namespace sunpower_solar
}  // namespace esphome
