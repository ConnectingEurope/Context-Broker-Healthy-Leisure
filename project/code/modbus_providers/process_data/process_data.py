import core.air_quality_observed_general as aqo
import connectors.modbus_connector as modbus
import connectors.format_data as format_data
import config.config as cnf

config = cnf.Config()

SENSORS_INFO = config.sensor_info
MODBUS_IP = config.modbus_ip_server

def process_sensor(index_sensor, service_name, date_observed, execute_local_host):
    dict_data = {}

    for key in SENSORS_INFO[index_sensor]["modbus"]:
        address_modbus = SENSORS_INFO[index_sensor]["modbus"][key]
        modbus_result = modbus.read_modbus_address(MODBUS_IP, address_modbus)
        sensor_data = format_data.format_modbus_data(key, modbus_result)

        if sensor_data != "":
            dict_data[key] = sensor_data
        else:
            print("Error parsing key: {0}".format(key))

    print(dict_data)
    if execute_local_host:
        aqo.execute_air_quality_observed_local(service_name, date_observed, index_sensor, dict_data)
    else:
        aqo.execute_air_quality_observed(service_name, date_observed, index_sensor, dict_data)

    