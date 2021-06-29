import time

import process_data.process_data as execute
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()

AQO_SERVICE = config.aqo_service
LIST_SENSORS_MODBUS = config.list_sensors_modbus

if __name__ == "__main__":
    seconds_to_wait = 5*60 # 5 minutes
    print("START - EXECUTION EVERY {0} seconds.".format(seconds_to_wait))
    execute_local_host = False

    while True:
        for index_sensor in LIST_SENSORS_MODBUS:
            try:
                string_datetime_now, date_datetime_now = generate.datetime_time_tz()

                print("{0} {1} {2}".format(string_datetime_now, index_sensor, AQO_SERVICE))
                execute.process_sensor(index_sensor, AQO_SERVICE, date_datetime_now, execute_local_host)
            except Exception as ex:
                error_text = "Error processing id: {0}. Exception {1}".format(index_sensor, ex)
                print(error_text)

        print("SLEEP {0}".format(seconds_to_wait))
        time.sleep(seconds_to_wait)