import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_ACTIVE_POWER,
    CONF_APPARENT_POWER,
    CONF_CURRENT,
    CONF_NAME,
    CONF_POWER_FACTOR,
    CONF_REACTIVE_POWER,
    CONF_VOLTAGE,
    DEVICE_CLASS_APPARENT_POWER,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_POWER_FACTOR,
    DEVICE_CLASS_REACTIVE_POWER,
    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_AMPERE,
    UNIT_KILOWATT,
    UNIT_KILOWATT_HOURS,
    UNIT_PERCENT,
    UNIT_VOLT,
    UNIT_VOLT_AMPS,
    UNIT_VOLT_AMPS_REACTIVE,
)
from . import (
    CONF_CONSUMPTION_METER,
    CONF_CONSUMPTION_METER_ID,
    CONF_LIFETIME_ENERGY,
    CONF_PRODUCTION_METER,
    CONF_PRODUCTION_METER_ID,
    CONF_PVS_ID,
    ConsumptionMeter,
    PVS,
    ProductionMeter,
)

CONF_ENERGY_FROM_GRID = "energy_from_grid"
CONF_ENERGY_TO_GRID = "energy_to_grid"
CONF_PHASE_A = "phase_a"
CONF_PHASE_B = "phase_b"
CONF_POWER_FROM_GRID = "power_from_grid"
CONF_POWER_TO_GRID = "power_to_grid"

PVS_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_PVS_ID): cv.use_id(PVS),
        cv.Optional(CONF_ENERGY_FROM_GRID): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_ENERGY_TO_GRID): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_POWER_FROM_GRID): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT,
                accuracy_decimals=4,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_POWER_TO_GRID): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT,
                accuracy_decimals=4,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
    }
)

CONSUMPTION_METER_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_CONSUMPTION_METER_ID): cv.use_id(ConsumptionMeter),
        cv.Optional(CONF_VOLTAGE): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_ACTIVE_POWER): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT,
                accuracy_decimals=4,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_APPARENT_POWER): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT_AMPS,
                accuracy_decimals=4,
                device_class=DEVICE_CLASS_APPARENT_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_REACTIVE_POWER): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT_AMPS_REACTIVE,
                accuracy_decimals=4,
                device_class=DEVICE_CLASS_REACTIVE_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_POWER_FACTOR): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_POWER_FACTOR,
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
        cv.Optional(CONF_PHASE_A): cv.Schema(
            {
                cv.Optional(CONF_CURRENT): cv.maybe_simple_value(
                    sensor.sensor_schema(
                        unit_of_measurement=UNIT_AMPERE,
                        accuracy_decimals=2,
                        device_class=DEVICE_CLASS_CURRENT,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    key=CONF_NAME,
                ),
                cv.Optional(CONF_VOLTAGE): cv.maybe_simple_value(
                    sensor.sensor_schema(
                        unit_of_measurement=UNIT_VOLT,
                        accuracy_decimals=2,
                        device_class=DEVICE_CLASS_VOLTAGE,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    key=CONF_NAME,
                ),
                cv.Optional(CONF_ACTIVE_POWER): cv.maybe_simple_value(
                    sensor.sensor_schema(
                        unit_of_measurement=UNIT_KILOWATT,
                        accuracy_decimals=4,
                        device_class=DEVICE_CLASS_POWER,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    key=CONF_NAME,
                ),
            }
        ),
        cv.Optional(CONF_PHASE_B): cv.Schema(
            {
                cv.Optional(CONF_CURRENT): cv.maybe_simple_value(
                    sensor.sensor_schema(
                        unit_of_measurement=UNIT_AMPERE,
                        accuracy_decimals=2,
                        device_class=DEVICE_CLASS_CURRENT,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    key=CONF_NAME,
                ),
                cv.Optional(CONF_VOLTAGE): cv.maybe_simple_value(
                    sensor.sensor_schema(
                        unit_of_measurement=UNIT_VOLT,
                        accuracy_decimals=2,
                        device_class=DEVICE_CLASS_VOLTAGE,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    key=CONF_NAME,
                ),
                cv.Optional(CONF_ACTIVE_POWER): cv.maybe_simple_value(
                    sensor.sensor_schema(
                        unit_of_measurement=UNIT_KILOWATT,
                        accuracy_decimals=4,
                        device_class=DEVICE_CLASS_POWER,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    key=CONF_NAME,
                ),
            }
        ),
    }
)

PRODUCTION_METER_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_PRODUCTION_METER_ID): cv.use_id(ProductionMeter),
        cv.Optional(CONF_CURRENT): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_VOLTAGE): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_ACTIVE_POWER): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT,
                accuracy_decimals=4,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_APPARENT_POWER): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT_AMPS,
                accuracy_decimals=4,
                device_class=DEVICE_CLASS_APPARENT_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_REACTIVE_POWER): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT_AMPS_REACTIVE,
                accuracy_decimals=4,
                device_class=DEVICE_CLASS_REACTIVE_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_POWER_FACTOR): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_POWER_FACTOR,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_LIFETIME_ENERGY): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=4,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            key=CONF_NAME,
        ),
    }
)


def validate_config(conf):
    need_energy_sensors = (CONF_ENERGY_FROM_GRID in conf) or (
        CONF_ENERGY_TO_GRID in conf
    )
    if need_energy_sensors:
        if (CONF_CONSUMPTION_METER not in conf) or (
            CONF_LIFETIME_ENERGY not in conf[CONF_CONSUMPTION_METER]
        ):
            raise cv.Invalid(
                f"The '{CONF_LIFETIME_ENERGY}' sensor must be enabled in '{CONF_CONSUMPTION_METER}' to use either '{CONF_ENERGY_FROM_GRID}' or '{CONF_ENERGY_TO_GRID}'"
            )

        if (CONF_PRODUCTION_METER not in conf) or (
            CONF_LIFETIME_ENERGY not in conf[CONF_PRODUCTION_METER]
        ):
            raise cv.Invalid(
                f"The '{CONF_LIFETIME_ENERGY}' sensor must be enabled in '{CONF_PRODUCTION_METER}' to use either '{CONF_ENERGY_FROM_GRID}' or '{CONF_ENERGY_TO_GRID}'"
            )

    need_power_sensors = (CONF_POWER_FROM_GRID in conf) or (CONF_POWER_TO_GRID in conf)
    if need_power_sensors:
        if (CONF_CONSUMPTION_METER not in conf) or (
            CONF_ACTIVE_POWER not in conf[CONF_CONSUMPTION_METER]
        ):
            raise cv.Invalid(
                f"The '{CONF_ACTIVE_POWER}' sensor must be enabled in '{CONF_CONSUMPTION_METER}' to use either '{CONF_POWER_FROM_GRID}' or '{CONF_POWER_TO_GRID}'"
            )

        if (CONF_PRODUCTION_METER not in conf) or (
            CONF_ACTIVE_POWER not in conf[CONF_PRODUCTION_METER]
        ):
            raise cv.Invalid(
                f"The '{CONF_ACTIVE_POWER}' sensor must be enabled in '{CONF_PRODUCTION_METER}' to use either '{CONF_POWER_FROM_GRID}' or '{CONF_POWER_TO_GRID}'"
            )

    return conf


CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.Optional(CONF_CONSUMPTION_METER): CONSUMPTION_METER_SCHEMA,
            cv.Optional(CONF_PRODUCTION_METER): PRODUCTION_METER_SCHEMA,
        }
    )
    .extend(PVS_SCHEMA)
    .extend(cv.COMPONENT_SCHEMA),
    validate_config,
)


async def to_code(config):
    pvs = await cg.get_variable(config[CONF_PVS_ID])

    for sensor_type in [
        CONF_ENERGY_FROM_GRID,
        CONF_ENERGY_TO_GRID,
        CONF_POWER_FROM_GRID,
        CONF_POWER_TO_GRID,
    ]:
        if conf := config.get(sensor_type):
            sens = await sensor.new_sensor(conf)
            cg.add(getattr(pvs, f"set_{sensor_type}")(sens))

    if consumption := config.get(CONF_CONSUMPTION_METER):
        cm = await cg.get_variable(consumption[CONF_CONSUMPTION_METER_ID])

        for sensor_type in [
            CONF_ACTIVE_POWER,
            CONF_APPARENT_POWER,
            CONF_CURRENT,
            CONF_LIFETIME_ENERGY,
            CONF_POWER_FACTOR,
            CONF_REACTIVE_POWER,
            CONF_VOLTAGE,
        ]:
            if conf := consumption.get(sensor_type):
                sens = await sensor.new_sensor(conf)
                cg.add(getattr(cm, f"set_{sensor_type}")(sens))

        for phase_type in [CONF_PHASE_A, CONF_PHASE_B]:
            if phase := consumption.get(phase_type):
                for sensor_type in [
                    CONF_ACTIVE_POWER,
                    CONF_CURRENT,
                    CONF_VOLTAGE,
                ]:
                    if conf := phase.get(sensor_type):
                        sens = await sensor.new_sensor(conf)
                        cg.add(getattr(cm, f"set_{phase_type}_{sensor_type}")(sens))

    if production := config.get(CONF_PRODUCTION_METER):
        pm = await cg.get_variable(production[CONF_PRODUCTION_METER_ID])

        for sensor_type in [
            CONF_ACTIVE_POWER,
            CONF_APPARENT_POWER,
            CONF_CURRENT,
            CONF_LIFETIME_ENERGY,
            CONF_POWER_FACTOR,
            CONF_REACTIVE_POWER,
            CONF_VOLTAGE,
        ]:
            if conf := production.get(sensor_type):
                sens = await sensor.new_sensor(conf)
                cg.add(getattr(pm, f"set_{sensor_type}")(sens))
