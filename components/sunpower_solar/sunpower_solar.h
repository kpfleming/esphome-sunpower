#pragma once

#include "esphome/core/defines.h"
#include "esphome/core/component.h"

#ifdef USE_BINARY_SENSOR
#include "esphome/components/binary_sensor/binary_sensor.h"
#endif

#ifdef USE_SENSOR
#include "esphome/components/sensor/sensor.h"
#endif

#ifdef USE_TEXT_SENSOR
#include "esphome/components/text_sensor/text_sensor.h"
#endif

#include <unordered_map>
#include <utility>
#include <vector>

#define ARDUINOJSON_ENABLE_STD_STRING 1  // NOLINT

#define ARDUINOJSON_USE_LONG_LONG 1  // NOLINT

#include <ArduinoJson.h>

namespace esphome {
namespace sunpower_solar {

static const char *const TAG = "sunpower_solar";

class SunpowerSolar;

struct SunpowerDevice {};

struct SunpowerSerialDevice : public SunpowerDevice {
#ifdef USE_BINARY_SENSOR
  void set_error_condition(binary_sensor::BinarySensor *sens) { this->error_condition = sens; }

  bool error_condition_no_data{false};
  binary_sensor::BinarySensor *error_condition{nullptr};
#endif

#ifdef USE_TEXT_SENSOR
  void set_hardware_version(text_sensor::TextSensor *sens) { this->hardware_version = sens; }
  void set_software_version(text_sensor::TextSensor *sens) { this->software_version = sens; }

  text_sensor::TextSensor *hardware_version{nullptr};
  text_sensor::TextSensor *software_version{nullptr};
#endif

  void set_serial(std::string str) { this->serial = std::move(str); }

  std::string serial;

  virtual void no_data() = 0;
  virtual void process_data(const JsonObject &data) = 0;
  virtual void setup_json_filter_keys(JsonObject &filter) = 0;
  virtual void dump_config() = 0;
};

struct ConsumptionMeter : public SunpowerSerialDevice {
#ifdef USE_SENSOR
  void set_active_power(sensor::Sensor *sens) { this->active_power = sens; }
  void set_apparent_power(sensor::Sensor *sens) { this->apparent_power = sens; }
  void set_lifetime_energy(sensor::Sensor *sens) { this->lifetime_energy = sens; }
  void set_power_factor(sensor::Sensor *sens) { this->power_factor = sens; }
  void set_reactive_power(sensor::Sensor *sens) { this->reactive_power = sens; }
  void set_voltage(sensor::Sensor *sens) { this->voltage = sens; }

  void set_phase_a_active_power(sensor::Sensor *sens) { this->phase_a_active_power = sens; }
  void set_phase_a_current(sensor::Sensor *sens) { this->phase_a_current = sens; }
  void set_phase_a_voltage(sensor::Sensor *sens) { this->phase_a_voltage = sens; }

  void set_phase_b_active_power(sensor::Sensor *sens) { this->phase_b_active_power = sens; }
  void set_phase_b_current(sensor::Sensor *sens) { this->phase_b_current = sens; }
  void set_phase_b_voltage(sensor::Sensor *sens) { this->phase_b_voltage = sens; }

  sensor::Sensor *active_power{nullptr};
  sensor::Sensor *apparent_power{nullptr};
  sensor::Sensor *lifetime_energy{nullptr};
  sensor::Sensor *power_factor{nullptr};
  sensor::Sensor *reactive_power{nullptr};
  sensor::Sensor *voltage{nullptr};

  sensor::Sensor *phase_a_active_power{nullptr};
  sensor::Sensor *phase_a_current{nullptr};
  sensor::Sensor *phase_a_voltage{nullptr};

  sensor::Sensor *phase_b_active_power{nullptr};
  sensor::Sensor *phase_b_current{nullptr};
  sensor::Sensor *phase_b_voltage{nullptr};
#endif

  void no_data() override;
  void process_data(const JsonObject &data) override;
  void setup_json_filter_keys(JsonObject &filter) override;
  void dump_config() override;
};

struct ProductionMeter : public SunpowerSerialDevice {
#ifdef USE_SENSOR
  void set_active_power(sensor::Sensor *sens) { this->active_power = sens; }
  void set_apparent_power(sensor::Sensor *sens) { this->apparent_power = sens; }
  void set_current(sensor::Sensor *sens) { this->current = sens; }
  void set_lifetime_energy(sensor::Sensor *sens) { this->lifetime_energy = sens; }
  void set_power_factor(sensor::Sensor *sens) { this->power_factor = sens; }
  void set_reactive_power(sensor::Sensor *sens) { this->reactive_power = sens; }
  void set_voltage(sensor::Sensor *sens) { this->voltage = sens; }

  sensor::Sensor *active_power{nullptr};
  sensor::Sensor *apparent_power{nullptr};
  sensor::Sensor *current{nullptr};
  sensor::Sensor *lifetime_energy{nullptr};
  sensor::Sensor *power_factor{nullptr};
  sensor::Sensor *reactive_power{nullptr};
  sensor::Sensor *voltage{nullptr};
#endif

  void no_data() override;
  void process_data(const JsonObject &data) override;
  void setup_json_filter_keys(JsonObject &filter) override;
  void dump_config() override;
};

struct Panel : public SunpowerSerialDevice {
#ifdef USE_SENSOR
  void set_current(sensor::Sensor *sens) { this->current = sens; }
  void set_lifetime_energy(sensor::Sensor *sens) { this->lifetime_energy = sens; }
  void set_power(sensor::Sensor *sens) { this->power = sens; }
  void set_temperature(sensor::Sensor *sens) { this->temperature = sens; }
  void set_voltage(sensor::Sensor *sens) { this->voltage = sens; }

  sensor::Sensor *current{nullptr};
  sensor::Sensor *lifetime_energy{nullptr};
  sensor::Sensor *power{nullptr};
  sensor::Sensor *temperature{nullptr};
  sensor::Sensor *voltage{nullptr};
#endif

  void no_data() override;
  void process_data(const JsonObject &data) override;
  void setup_json_filter_keys(JsonObject &filter) override;
  void dump_config() override;

  void set_name(std::string str) { this->name = std::move(str); }
  std::string name;
};

struct Array : public SunpowerDevice {
#ifdef USE_SENSOR
  void set_current(sensor::Sensor *sens) { this->current = sens; }
  void set_lifetime_energy(sensor::Sensor *sens) { this->lifetime_energy = sens; }
  void set_power(sensor::Sensor *sens) { this->power = sens; }

  sensor::Sensor *current{nullptr};
  sensor::Sensor *lifetime_energy{nullptr};
  sensor::Sensor *power{nullptr};
#endif

  void dump_config();

  void add_panel(Panel *panel) { this->panels.push_back(panel); }
  std::vector<Panel *> panels;

  void set_name(std::string str) { this->name = std::move(str); }
  std::string name;
};

struct PVS : public SunpowerSerialDevice {
#ifdef USE_SENSOR
  void set_energy_from_grid(sensor::Sensor *sens) { this->energy_from_grid = sens; }
  void set_energy_to_grid(sensor::Sensor *sens) { this->energy_to_grid = sens; }
  void set_power_from_grid(sensor::Sensor *sens) { this->power_from_grid = sens; }
  void set_power_to_grid(sensor::Sensor *sens) { this->power_to_grid = sens; }

  sensor::Sensor *energy_from_grid{nullptr};
  sensor::Sensor *energy_to_grid{nullptr};
  sensor::Sensor *power_from_grid{nullptr};
  sensor::Sensor *power_to_grid{nullptr};

  float total_energy_from_grid{0.0f};
  float total_energy_to_grid{0.0f};
  float last_energy_consumption{0.0f};
  float last_energy_production{0.0f};

#endif

  void publish_synthetic_sensors();

  void set_consumption_meter(ConsumptionMeter *meter) { this->consumption_meter = meter; }
  void set_production_meter(ProductionMeter *meter) { this->production_meter = meter; }

  ConsumptionMeter *consumption_meter{nullptr};
  ProductionMeter *production_meter{nullptr};

  void process_data(const JsonObject &data) override;
  void no_data() override;
  void setup_json_filter_keys(JsonObject &filter) override;
  void dump_config() override;
};

class SunpowerSolar : public Component {
 public:
  void setup() override;

  float get_setup_priority() const override { return setup_priority::LATE; }

  void dump_config() override;

  void set_json_data_filter_size(size_t size) { this->json_data_filter_size_ = size; }
  void set_json_data_size(size_t size) { this->json_data_size_ = size; }

  void set_pvs(PVS *pvs) { this->pvs_ = pvs; }

  void add_device(SunpowerSerialDevice *device) { this->devices_.insert({device->serial, device}); }
  void add_array(Array *array) { this->arrays_.push_back(array); }

  void process_data(std::vector<char> &data);

 protected:
  size_t json_data_filter_size_{1024};
  size_t json_data_size_{2048};

  PVS *pvs_;
  std::vector<Array *> arrays_;
  std::unordered_map<std::string, SunpowerSerialDevice *> devices_;

  bool validate_arrays_();
  void publish_arrays_();

  DynamicJsonDocument *json_data_filter_;
  DynamicJsonDocument *json_data_;
};

}  // namespace sunpower_solar
}  // namespace esphome
