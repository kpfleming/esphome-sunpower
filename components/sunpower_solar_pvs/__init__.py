import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import (
    CONF_BUFFER_SIZE,
    CONF_DATA,
    CONF_FILTER,
    CONF_ID,
)

CODEOWNERS = ["@kpfleming"]

CONF_CONSUMPTION_METER = "consumption_meter"
CONF_CONSUMPTION_METER_ID = "consumption_meter_id"
CONF_LIFETIME_ENERGY = "lifetime_energy"
CONF_SERIAL = "serial"
CONF_PRODUCTION_METER = "production_meter"
CONF_PRODUCTION_METER_ID = "production_meter_id"
CONF_PVS_ID = "pvs_id"
CONF_SUNPOWER_SOLAR_ID = "sunpower_solar_id"

sunpower_solar_ns = cg.esphome_ns.namespace("sunpower_solar")
SunpowerSolar = sunpower_solar_ns.class_("SunpowerSolar", cg.Component)
ConsumptionMeter = sunpower_solar_ns.struct("ConsumptionMeter")
ProductionMeter = sunpower_solar_ns.struct("ProductionMeter")
PVS = sunpower_solar_ns.struct("PVS")

PVS_SCHEMA = cv.Schema(
    {
        cv.GenerateID(key=CONF_PVS_ID): cv.declare_id(PVS),
        cv.Required(CONF_SERIAL): cv.string_strict,
    }
)

CONSUMPTION_METER_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(ConsumptionMeter),
        cv.Required(CONF_SERIAL): cv.string_strict,
    }
)

PRODUCTION_METER_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(ProductionMeter),
        cv.Required(CONF_SERIAL): cv.string_strict,
    }
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(SunpowerSolar),
        cv.Optional(CONF_CONSUMPTION_METER): CONSUMPTION_METER_SCHEMA,
        cv.Optional(CONF_PRODUCTION_METER): PRODUCTION_METER_SCHEMA,
        cv.Optional(CONF_BUFFER_SIZE): cv.Schema(
            {
                cv.Optional(CONF_FILTER, default=1024): cv.int_range(
                    min=1024, max=4096
                ),
                cv.Optional(CONF_DATA, default=2048): cv.int_range(min=2048, max=32768),
            }
        ),
    }
).extend(PVS_SCHEMA)


async def to_code(config):
    cg.add_library("bblanchon/ArduinoJson", "6.18.5")

    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    pvs = cg.new_Pvariable(config[CONF_PVS_ID])
    cg.add(pvs.set_serial(config[CONF_SERIAL]))
    cg.add(var.add_device(pvs))
    cg.add(var.set_pvs(pvs))

    if consumption := config.get(CONF_CONSUMPTION_METER):
        cm = cg.new_Pvariable(consumption[CONF_ID])
        cg.add(pvs.set_consumption_meter(cm))
        cg.add(cm.set_serial(consumption[CONF_SERIAL]))
        cg.add(var.add_device(cm))

    if production := config.get(CONF_PRODUCTION_METER):
        pm = cg.new_Pvariable(production[CONF_ID])
        cg.add(pvs.set_production_meter(pm))
        cg.add(pm.set_serial(production[CONF_SERIAL]))
        cg.add(var.add_device(pm))

    if CONF_BUFFER_SIZE in config:
        cg.add(var.set_json_data_filter_size(config[CONF_BUFFER_SIZE][CONF_FILTER]))
        cg.add(var.set_json_data_size(config[CONF_BUFFER_SIZE][CONF_DATA]))
