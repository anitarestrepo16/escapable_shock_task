import serial.tools.list_ports
import serial

def find_arduino_port():
	'''
	If there's only one USB-to-serial port available, this function will 
	return the port address for it. Otherwise, returns None.
	'''
	candidate_ports = []
	ports = serial.tools.list_ports.comports()
	for port in ports:
		if port.product == 'USB2.0-Serial':
			candidate_ports.append(port)
	if len(candidate_ports) == 1:
		return port.device # only return if unique 
	else:
		return None

class PulseGenerator:
	'''
	Controller for generating voltage pulse trains using 
	an Arduino with a MCP4725 breakout board.

	Notes
	------
	A2 on Arduino connect to GND on MCP4725,
	A3 connects to Vcc (i.e. power),
	A4 connects to SDA, and A5 connects to SCL. 

	DAC output is on GND/OUT of the MCP4725, which can be connected 
	to an external device (e.g. stimulator).
	'''

	MAX = int('1'*12, 2) # maximum write value for 12 bit DAC

	def __init__(self, operating_voltage = 5., port = None, baudrate = 9600, timeout = 1):
		'''
		Arguments
		----------
		operating_voltage : float
			The operating voltage of the arduino, which is the maximum voltage
			for pulse generation. For an Arduino Nano, this would be 5.
			IF THIS IS INCORRECT, OUTPUT VOLTAGES WILL BE WRONG!
		port : str, default: None
			Port address for Arduino. If None, and there is only one 
			USB-to-serial option available, will just use that.
		baudrate : int 
			For serial connection; just needs to match arduino code
		timeout : int 
			For serial connection
		'''
		if port is None:
			port = find_arduino_port()
		if port is None:
			raise Exception(
				'Either no or multiple USB-to-serial devices found! Specify arduino port address manually.'
				)
		self.arduino = serial.Serial(
			port = port, baudrate = baudrate, timeout = timeout
			)
		self.operating_voltage = operating_voltage

	def write(self, value):
		'''
		communicates an integer value to arduino over serial 
		'''
		assert(value in range(self.MAX + 1)) # check is valid 
		self.arduino.write(f'<{value}>'.encode('utf-8'))

	def pulse(self, voltage):
		'''
		Arduino will generate a pulse train of specified voltage.
		Duration and timing of pulses are specified in arduino code.
		'''
		# check if possible 
		assert(voltage > 0)
		assert(voltage <= self.operating_voltage)
		# convert to integer value expected by DAC
		value = round((voltage / self.operating_voltage) * self.MAX)
		self.write(value)

	def __del__(self):
		self.arduino.close()
