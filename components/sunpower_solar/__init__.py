import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import (
    CONF_BUFFER_SIZE,
    CONF_DATA,
    CONF_FILTER,
    CONF_ID,
    CONF_NAME,
)

CODEOWNERS = ["@kpfleming"]

CONF_ARRAYS = "arrays"
CONF_ARRAY_ID = "array_id"
CONF_CONSUMPTION_METER = "consumption_meter"
CONF_CONSUMPTION_METER_ID = "consumption_meter_id"
CONF_LIFETIME_ENERGY = "lifetime_energy"
CONF_PANELS = "panels"
CONF_PRODUCTION_METER = "production_meter"
CONF_PRODUCTION_METER_ID = "production_meter_id"
CONF_PVS_ID = "pvs_id"
CONF_SERIAL = "serial"
CONF_SUNPOWER_SOLAR_ID = "sunpower_solar_id"

sunpower_solar_ns = cg.esphome_ns.namespace("sunpower_solar")

Array = sunpower_solar_ns.struct("Array")
ConsumptionMeter = sunpower_solar_ns.struct("ConsumptionMeter")
PVS = sunpower_solar_ns.struct("PVS")
Panel = sunpower_solar_ns.struct("Panel")
ProductionMeter = sunpower_solar_ns.struct("ProductionMeter")
SunpowerSolar = sunpower_solar_ns.class_("SunpowerSolar", cg.Component)

ARRAYS_SCHEMA = cv.ensure_list(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(Array),
            cv.Optional(CONF_NAME): cv.string_strict,
        }
    )
)

CONSUMPTION_METER_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(ConsumptionMeter),
        cv.Required(CONF_SERIAL): cv.string_strict,
    }
)

PANELS_SCHEMA = cv.ensure_list(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(Panel),
            cv.Optional(CONF_NAME): cv.string_strict,
            cv.Required(CONF_SERIAL): cv.string_strict,
            cv.Optional(CONF_ARRAY_ID): cv.use_id(Array),
        }
    )
)

PRODUCTION_METER_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(ProductionMeter),
        cv.Required(CONF_SERIAL): cv.string_strict,
    }
)

PVS_SCHEMA = cv.Schema(
    {
        cv.GenerateID(key=CONF_PVS_ID): cv.declare_id(PVS),
        cv.Required(CONF_SERIAL): cv.string_strict,
    }
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(SunpowerSolar),
        cv.Optional(CONF_BUFFER_SIZE): cv.Schema(
            {
                cv.Optional(CONF_FILTER, default=1024): cv.int_range(
                    min=1024, max=4096
                ),
                cv.Optional(CONF_DATA, default=2048): cv.int_range(min=2048, max=32768),
            }
        ),
        cv.Optional(CONF_CONSUMPTION_METER): CONSUMPTION_METER_SCHEMA,
        cv.Optional(CONF_PRODUCTION_METER): PRODUCTION_METER_SCHEMA,
        cv.Optional(CONF_PANELS): PANELS_SCHEMA,
        cv.Optional(CONF_ARRAYS): ARRAYS_SCHEMA,
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

    if CONF_BUFFER_SIZE in config:
        cg.add(var.set_json_data_filter_size(config[CONF_BUFFER_SIZE][CONF_FILTER]))
        cg.add(var.set_json_data_size(config[CONF_BUFFER_SIZE][CONF_DATA]))

    if arrays := config.get(CONF_ARRAYS):
        for array in arrays:
            a = cg.new_Pvariable(array[CONF_ID])
            cg.add(a.set_name(array[CONF_NAME]))
            cg.add(var.add_array(a))

    if consumption := config.get(CONF_CONSUMPTION_METER):
        cm = cg.new_Pvariable(consumption[CONF_ID])
        cg.add(pvs.set_consumption_meter(cm))
        cg.add(cm.set_serial(consumption[CONF_SERIAL]))
        cg.add(var.add_device(cm))

    if panels := config.get(CONF_PANELS):
        for panel in panels:
            p = cg.new_Pvariable(panel[CONF_ID])
            cg.add(p.set_name(panel[CONF_NAME]))
            cg.add(p.set_serial(panel[CONF_SERIAL]))
            cg.add(var.add_device(p))
            if array_id := panel.get(CONF_ARRAY_ID):
                a = await cg.get_variable(array_id)
                cg.add(a.add_panel(p))

    if production := config.get(CONF_PRODUCTION_METER):
        pm = cg.new_Pvariable(production[CONF_ID])
        cg.add(pvs.set_production_meter(pm))
        cg.add(pm.set_serial(production[CONF_SERIAL]))
        cg.add(var.add_device(pm))
