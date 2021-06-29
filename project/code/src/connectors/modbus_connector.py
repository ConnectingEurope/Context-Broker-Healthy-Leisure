from pyModbusTCP.client import ModbusClient

def read_modbus_address(server_ip, address):
	c = ModbusClient(host=server_ip, auto_open=True, auto_close=True)
	list_read_data = c.read_holding_registers(address)
	read_data = list_read_data[0]
	print("Adress: {0} // Value: {1}".format(address, read_data))

	return read_data
