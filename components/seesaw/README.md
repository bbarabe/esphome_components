# Seesaw component

This component provides support for the Adafruit Seesaw platform.  Define a `seesaw` component then add components for each function you want to use.

Currently, the supported functions are the rotary encoder, pins, temperature, touch, adc, and neopixel LEDs.

Example:
```yaml
seesaw:
  - id: ss_id

sensor:
  - platform: seesaw
    id: encoder
    type: encoder
    name: "Seesaw encoder"
    number: 1  # optional, defaults to 0
  - platform: seesaw
    id: temp
    type: temperature
  - platform: seesaw
    id: touch
    type: touch
    pin: 5
  - platform: seesaw
    seesaw_id: ss_id
    id: slider
    type: adc
    pin: 14

binary_sensor:
  - platform: gpio
    id: button
    name: "Seesaw encoder button"
    pin:
      seesaw: ss_id
      number: 2
      mode: input_pullup
      inverted: true

light:
  - platform: seesaw
    id: pixel
    name: "Seesaw neopixel LED"
    pin: 14
    num_leds: 4
```

