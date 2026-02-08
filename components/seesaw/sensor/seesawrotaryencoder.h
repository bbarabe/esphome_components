#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "../seesaw.h"

namespace esphome {
namespace seesaw {

class SeesawRotaryEncoder : public sensor::Sensor, public Component {
 public:
  void setup() override;
  void loop() override;

  void set_parent(Seesaw *parent) { parent_ = parent; }
  void set_number(uint8_t number) { number_ = number; }
  void set_min_value(int32_t min_value) { this->min_value_ = min_value; }
  void set_max_value(int32_t max_value) { this->max_value_ = max_value; }
  void set_poll_interval_ms(
    uint32_t poll_interval_ms) // Minimum milliseconds between encoder reads.
  {
    this->poll_interval_ms_ = poll_interval_ms > 0 ? poll_interval_ms : 1u;
  }

 protected:
  Seesaw *parent_;
  uint8_t number_{0};
  int32_t value_{0};
  int32_t min_value_{INT32_MIN};
  int32_t max_value_{INT32_MAX};
  uint32_t poll_interval_ms_{20}; // Minimum interval between I2C reads.
  uint32_t last_poll_ms_{0}; // Timestamp of last encoder read.
};

}  // namespace seesaw
}  // namespace esphome
