#include "seesawrotaryencoder.h"
#include "esphome/core/log.h"

namespace esphome {
namespace seesaw {

static const char *const TAG = "seesaw.encoder";

void SeesawRotaryEncoder::setup()
{
  ESP_LOGCONFIG(TAG, "Setting up Seesaw rotary encoder...");
  this->parent_->enable_encoder(this->number_);
  int32_t position = 0;
  if (!this->parent_->get_encoder_position(this->number_, &position))
  {
    position = 0;
  }
  if (position < this->min_value_)
  {
    position = this->min_value_;
  }
  if (position > this->max_value_)
  {
    position = this->max_value_;
  }
  this->value_ = position;
  this->publish_state(this->value_);
}

/*
 * Position-only encoder sampling path:
 * read absolute position every poll interval and publish changes directly.
 * This avoids dependence on DELTA reads, which can fail on some Seesaw setups.
 */
void SeesawRotaryEncoder::loop()
{
  const uint32_t now = millis();
  if ((now - this->last_poll_ms_) < this->poll_interval_ms_)
  {
    return;
  }
  this->last_poll_ms_ = now;

  int32_t position = 0;
  if (!this->parent_->get_encoder_position(this->number_, &position))
  {
    return;
  }

  if (position < this->min_value_)
  {
    position = this->min_value_;
  }
  if (position > this->max_value_)
  {
    position = this->max_value_;
  }
  if (position == this->value_)
  {
    return;
  }
  this->value_ = position;
  this->publish_state(this->value_);
}

}  // namespace seesaw
}  // namespace esphome
