import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    CONF_NAME,
    DEVICE_CLASS_PROBLEM,
    ENTITY_CATEGORY_DIAGNOSTIC,
)
from . import (
    CONF_CONSUMPTION_METER,
    CONF_CONSUMPTION_METER_ID,
    CONF_PANELS,
    CONF_PRODUCTION_METER,
    CONF_PRODUCTION_METER_ID,
    CONF_PVS_ID,
    CONF_SUNPOWER_SOLAR_ID,
    ConsumptionMeter,
    Panel,
    PVS,
    ProductionMeter,
    SunpowerSolar,
)

CONF_ERROR_CONDITION = "error_condition"

ERROR_CONDITION_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_ERROR_CONDITION): cv.maybe_simple_value(
            binary_sensor.binary_sensor_schema(
                device_class=DEVICE_CLASS_PROBLEM,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            key=CONF_NAME,
        ),
    }
)

CONSUMPTION_METER_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_CONSUMPTION_METER_ID): cv.use_id(ConsumptionMeter),
    }
).extend(ERROR_CONDITION_SCHEMA)

PANELS_SCHEMA = cv.Schema(
    {
        cv.use_id(Panel): ERROR_CONDITION_SCHEMA,
    }
)

PRODUCTION_METER_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_PRODUCTION_METER_ID): cv.use_id(ProductionMeter),
    }
).extend(ERROR_CONDITION_SCHEMA)

PVS_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_PVS_ID): cv.use_id(PVS),
    }
).extend(ERROR_CONDITION_SCHEMA)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_SUNPOWER_SOLAR_ID): cv.use_id(SunpowerSolar),
            cv.Optional(CONF_CONSUMPTION_METER): CONSUMPTION_METER_SCHEMA,
            cv.Optional(CONF_PRODUCTION_METER): PRODUCTION_METER_SCHEMA,
            cv.Optional(CONF_PANELS): PANELS_SCHEMA,
        }
    )
    .extend(PVS_SCHEMA)
    .extend(cv.COMPONENT_SCHEMA)
)


async def error_condition_to_code(var, config):
    if conf := config.get(CONF_ERROR_CONDITION):
        sens = await binary_sensor.new_binary_sensor(conf)
        cg.add(var.set_error_condition(sens))


async def to_code(config):
    pvs = await cg.get_variable(config[CONF_PVS_ID])
    await error_condition_to_code(pvs, config)

    if consumption := config.get(CONF_CONSUMPTION_METER):
        cm = await cg.get_variable(consumption[CONF_CONSUMPTION_METER_ID])
        await error_condition_to_code(cm, consumption)

    if panels := config.get(CONF_PANELS):
        for panel_id, panel_conf in panels.items():
            panel = await cg.get_variable(panel_id)
            await error_condition_to_code(panel, panel_conf)

    if production := config.get(CONF_PRODUCTION_METER):
        pm = await cg.get_variable(production[CONF_PRODUCTION_METER_ID])
        await error_condition_to_code(pm, production)
