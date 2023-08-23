import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_CURRENT,
    CONF_NAME,
    CONF_POWER,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_AMPERE,
    UNIT_KILOWATT,
    UNIT_KILOWATT_HOURS,
)
from esphome.components.sunpower_solar_pvs import (
    CONF_LIFETIME_ENERGY,
)
from . import CONF_ARRAY_ID, Array

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ARRAY_ID): cv.use_id(Array),
        cv.Optional(CONF_CURRENT): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_POWER): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT,
                accuracy_decimals=4,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_LIFETIME_ENERGY): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            key=CONF_NAME,
        ),
    }
)


async def to_code(config):
    array = await cg.get_variable(config[CONF_ARRAY_ID])

    for sensor_type in [
        CONF_CURRENT,
        CONF_LIFETIME_ENERGY,
        CONF_POWER,
    ]:
        if conf := config.get(sensor_type):
            sens = await sensor.new_sensor(conf)
            cg.add(getattr(array, f"set_{sensor_type}")(sens))
