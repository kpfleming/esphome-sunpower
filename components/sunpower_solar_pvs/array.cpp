#include "sunpower_solar.h"
#include <numeric>

namespace esphome {
namespace sunpower_solar {

void SunpowerSolar::publish_arrays_() {
#ifdef USE_SENSOR
  for (auto *array : this->arrays_) {
    if (array->current != nullptr) {
      float sum = std::accumulate(array->panels.begin(), array->panels.end(), 0.0f,
                                  [](float acc, Panel *panel) { return acc + panel->current->state; });
      array->current->publish_state(sum);
    }

    if (array->power != nullptr) {
      float sum = std::accumulate(array->panels.begin(), array->panels.end(), 0.0f,
                                  [](float acc, Panel *panel) { return acc + panel->power->state; });
      array->power->publish_state(sum);
    }

    if (array->lifetime_energy != nullptr) {
      float sum = std::accumulate(array->panels.begin(), array->panels.end(), 0.0f,
                                  [](float acc, Panel *panel) { return acc + panel->lifetime_energy->state; });
      array->lifetime_energy->publish_state(sum);
    }
  }
#endif
}

}  // namespace sunpower_solar
}  // namespace esphome
