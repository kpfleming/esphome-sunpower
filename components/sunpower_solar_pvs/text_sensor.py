import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import (
    CONF_NAME,
    ENTITY_CATEGORY_DIAGNOSTIC,
)
from . import (
    CONF_CONSUMPTION_METER,
    CONF_CONSUMPTION_METER_ID,
    CONF_PRODUCTION_METER,
    CONF_PRODUCTION_METER_ID,
    CONF_PVS_ID,
    CONF_SUNPOWER_SOLAR_ID,
    ConsumptionMeter,
    PVS,
    ProductionMeter,
    SunpowerSolar,
)

CONF_HARDWARE_VERSION = "hardware_version"
CONF_SOFTWARE_VERSION = "software_version"

HARDWARE_VERSION_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_HARDWARE_VERSION): cv.maybe_simple_value(
            text_sensor.text_sensor_schema(
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            key=CONF_NAME,
        ),
    }
)

SOFTWARE_VERSION_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SOFTWARE_VERSION): cv.maybe_simple_value(
            text_sensor.text_sensor_schema(
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            key=CONF_NAME,
        ),
    }
)

PVS_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_PVS_ID): cv.use_id(PVS),
        }
    )
    .extend(HARDWARE_VERSION_SCHEMA)
    .extend(SOFTWARE_VERSION_SCHEMA)
)

CONSUMPTION_METER_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_CONSUMPTION_METER_ID): cv.use_id(ConsumptionMeter),
        }
    )
    .extend(HARDWARE_VERSION_SCHEMA)
    .extend(SOFTWARE_VERSION_SCHEMA)
)

PRODUCTION_METER_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_PRODUCTION_METER_ID): cv.use_id(ProductionMeter),
        }
    )
    .extend(HARDWARE_VERSION_SCHEMA)
    .extend(SOFTWARE_VERSION_SCHEMA)
)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_SUNPOWER_SOLAR_ID): cv.use_id(SunpowerSolar),
            cv.Optional(CONF_CONSUMPTION_METER): CONSUMPTION_METER_SCHEMA,
            cv.Optional(CONF_PRODUCTION_METER): PRODUCTION_METER_SCHEMA,
        }
    )
    .extend(PVS_SCHEMA)
    .extend(cv.COMPONENT_SCHEMA)
)


async def hardware_version_to_code(var, config):
    if conf := config.get(CONF_HARDWARE_VERSION):
        sens = await text_sensor.new_text_sensor(conf)
        cg.add(var.set_hardware_version(sens))


async def software_version_to_code(var, config):
    if conf := config.get(CONF_SOFTWARE_VERSION):
        sens = await text_sensor.new_text_sensor(conf)
        cg.add(var.set_software_version(sens))


async def to_code(config):
    pvs = await cg.get_variable(config[CONF_PVS_ID])
    await hardware_version_to_code(pvs, config)
    await software_version_to_code(pvs, config)

    if consumption := config.get(CONF_CONSUMPTION_METER):
        cm = await cg.get_variable(consumption[CONF_CONSUMPTION_METER_ID])
        await hardware_version_to_code(cm, consumption)
        await software_version_to_code(cm, consumption)

    if production := config.get(CONF_PRODUCTION_METER):
        pm = await cg.get_variable(production[CONF_PRODUCTION_METER_ID])
        await hardware_version_to_code(pm, production)
        await software_version_to_code(pm, production)
