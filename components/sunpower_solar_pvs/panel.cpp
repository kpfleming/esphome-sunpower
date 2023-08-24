#include "sunpower_solar.h"
#include "sensor_map.h"
#include "text_sensor_map.h"

namespace esphome {
namespace sunpower_solar {

#ifdef USE_SENSOR
const std::array<SensorMap<Panel>, 5> PANEL_SENSOR_MAP = {{{&Panel::current, "i_3phsum_a", true, nullopt},
                                                           {&Panel::lifetime_energy, "ltea_3phsum_kwh", false, nullopt},
                                                           {&Panel::power, "p_3phsum_kw", true, nullopt},
                                                           {&Panel::temperature, "t_htsnk_degc", true, nullopt},
                                                           {&Panel::voltage, "vln_3phavg_v", true, nullopt}}};
#endif

#ifdef USE_TEXT_SENSOR
const std::array<TextSensorMap<Panel>, 2> PANEL_TEXT_SENSOR_MAP = {
    {{&Panel::hardware_version, "hw_version", false, nullopt}, {&Panel::software_version, "SWVER", false, nullopt}}};
#endif

void Panel::setup_json_filter_keys(JsonObject &filter) {
#ifdef USE_SENSOR
  add_filter_keys_for_sensors(*this, PANEL_SENSOR_MAP, filter);
#endif
#ifdef USE_TEXT_SENSOR
  add_filter_keys_for_sensors(*this, PANEL_TEXT_SENSOR_MAP, filter);
#endif
}

void Panel::no_data() {
#ifdef USE_SENSOR
  clear_no_data_sensors(*this, PANEL_SENSOR_MAP);
#endif
#ifdef USE_TEXT_SENSOR
  clear_no_data_sensors(*this, PANEL_TEXT_SENSOR_MAP);
#endif
}

void Panel::process_data(const JsonObject &data) {
#ifdef USE_BINARY_SENSOR
  if ((this->error_condition != nullptr) && this->error_condition_no_data) {
    this->error_condition->publish_state(false);
  }
#endif
#ifdef USE_SENSOR
  publish_sensors(*this, PANEL_SENSOR_MAP, data);
#endif
#ifdef USE_TEXT_SENSOR
  publish_sensors(*this, PANEL_TEXT_SENSOR_MAP, data);
#endif
}

}  // namespace sunpower_solar
}  // namespace esphome
