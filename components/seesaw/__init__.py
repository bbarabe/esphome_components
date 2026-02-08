import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import i2c
from esphome.const import (
    CONF_ID,
    CONF_INPUT,
    CONF_INVERTED,
    CONF_NUMBER,
    CONF_MODE,
    CONF_OUTPUT,
    CONF_PULLUP,
)
from esphome.core import coroutine

CODEOWNERS = ["@ssieb"]
MULTI_CONF = True

seesaw_ns = cg.esphome_ns.namespace("seesaw")
Seesaw = seesaw_ns.class_("Seesaw", i2c.I2CDevice, cg.Component)
SeesawGPIOPin = seesaw_ns.class_("SeesawGPIOPin", cg.GPIOPin)

CONF_SEESAW = "seesaw"
CONF_LOG_ERRORS = "log_errors"
CONF_LOG_ERROR_INTERVAL = "log_error_interval_ms"

CONFIG_SCHEMA = cv.COMPONENT_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(Seesaw),
        cv.Optional(CONF_LOG_ERRORS, default=False): cv.boolean,
        cv.Optional(CONF_LOG_ERROR_INTERVAL, default="1s"): cv.positive_time_period_milliseconds,
    }
).extend(i2c.i2c_device_schema(0x49))

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)
    cg.add(var.set_log_errors(config[CONF_LOG_ERRORS], config[CONF_LOG_ERROR_INTERVAL]))


def validate_mode(value):
    if not (value[CONF_INPUT] ^ value[CONF_OUTPUT]):
        raise cv.Invalid("Mode must be either input or output")
    if value[CONF_PULLUP] and not value[CONF_INPUT]:
        raise cv.Invalid("Pullup only available with input")
    return value


SEESAW_PIN_SCHEMA = cv.All(
    {
        cv.GenerateID(): cv.declare_id(SeesawGPIOPin),
        cv.Required(CONF_SEESAW): cv.use_id(Seesaw),
        cv.Required(CONF_NUMBER): cv.int_range(min=0, max=15),
        cv.Optional(CONF_MODE, default={}): cv.All(
            {
                cv.Optional(CONF_INPUT, default=False): cv.boolean,
                cv.Optional(CONF_PULLUP, default=False): cv.boolean,
                cv.Optional(CONF_OUTPUT, default=False): cv.boolean,
            },
            validate_mode,
        ),
        cv.Optional(CONF_INVERTED, default=False): cv.boolean,
    }
)


@pins.PIN_SCHEMA_REGISTRY.register(CONF_SEESAW, SEESAW_PIN_SCHEMA)
async def seesaw_pin_to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    parent = await cg.get_variable(config[CONF_SEESAW])

    cg.add(var.set_parent(parent))

    num = config[CONF_NUMBER]
    cg.add(var.set_pin(num))
    cg.add(var.set_inverted(config[CONF_INVERTED]))
    cg.add(var.set_flags(pins.gpio_flags_expr(config[CONF_MODE])))
    return var
