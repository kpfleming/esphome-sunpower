#include "sunpower_solar.h"
#include <numeric>

namespace esphome {
namespace sunpower_solar {

void Array::dump_config() {
  ESP_LOGCONFIG(TAG, "  Array %s:", this->name.c_str());

#ifdef USE_SENSOR
  LOG_SENSOR("    ", "current", this->current);
  LOG_SENSOR("    ", "power", this->power);
  LOG_SENSOR("    ", "lifetime_energy", this->lifetime_energy);
#endif

  ESP_LOGCONFIG(TAG, "    Panels:");
  for (auto *panel : this->panels) {
    ESP_LOGCONFIG(TAG, "      %s", panel->name.c_str());
  }
}

bool SunpowerSolar::validate_arrays_() {
#ifdef USE_SENSOR
  for (auto *array : this->arrays_) {
    if (array->current != nullptr) {
      for (auto *panel : array->panels) {
        if (panel->current == nullptr) {
          ESP_LOGE(TAG, "Array '%s' has 'current' sensor enabled but panel '%s' does not.", array->name.c_str(),
                   panel->name.c_str());
          return false;
        }
      }
    }

    if (array->power != nullptr) {
      for (auto *panel : array->panels) {
        if (panel->power == nullptr) {
          ESP_LOGE(TAG, "Array '%s' has 'power' sensor enabled but panel '%s' does not.", array->name.c_str(),
                   panel->name.c_str());
          return false;
        }
      }
    }

    if (array->lifetime_energy != nullptr) {
      for (auto *panel : array->panels) {
        if (panel->lifetime_energy == nullptr) {
          ESP_LOGE(TAG, "Array '%s' has 'lifetime_energy' sensor enabled but panel '%s' does not.", array->name.c_str(),
                   panel->name.c_str());
          return false;
        }
      }
    }
  }
#endif

  return true;
}

void SunpowerSolar::publish_arrays_() {
#ifdef USE_SENSOR
  for (auto *array : this->arrays_) {
    if (array->current != nullptr) {
      float sum = std::accumulate(array->panels.begin(), array->panels.end(), 0.0f,
                                  [](float acc, Panel *panel) { return acc + panel->current->raw_state; });
      array->current->publish_state(sum);
    }

    if (array->power != nullptr) {
      float sum = std::accumulate(array->panels.begin(), array->panels.end(), 0.0f,
                                  [](float acc, Panel *panel) { return acc + panel->power->raw_state; });
      array->power->publish_state(sum);
    }

    if (array->lifetime_energy != nullptr) {
      float sum = std::accumulate(array->panels.begin(), array->panels.end(), 0.0f,
                                  [](float acc, Panel *panel) { return acc + panel->lifetime_energy->raw_state; });
      array->lifetime_energy->publish_state(sum);
    }
  }
#endif
}

}  // namespace sunpower_solar
}  // namespace esphome
