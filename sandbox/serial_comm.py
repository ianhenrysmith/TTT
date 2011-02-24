#! /usr/bin/python
import serial, commands, time

# 
# board = Arduino()
# board.write("DENVER", "RED")
#

class Arduino:

	def __init__(self):
		self.ready = False
		usbs = commands.getoutput('ls /dev | grep "USB"')
		if not usbs:
  			print "Arduino not hooked up to USB"
  			exit()
		for usb in usbs.split('\n'):
			testSerial = serial.Serial('/dev/%s'%usb, 9600)
			if testSerial.read() is 'A':
				if testSerial.read() is 't':
					if testSerial.read() is 'W':
						self.ready = True
						self.ser = testSerial
		if self.ready is False:
			print "Arduino not hooked up to USB"
  			exit()

	def isReady(self):
		return self.ready
			
	#
	# board.write("DENVER","RED")
	#
	def write(self, city, color):
		if self.ready is True:
			cityPin = Arduino.city(city)
			colorPin = Arduino.color(color)
			# write s222x
			self.ser.write('s')
			self.ser.write(chr(cityPin))
			self.ser.write(chr(colorPin))
			self.ser.write('x')
			print "Wrote %s:%s to %s:%s"%(color,colorPin,city,cityPin)
			return True
		else:
			print "Arduino Init Problem"
			return False 
	
	#	
	# x = Arduino.color("RED")
	#
	@classmethod
	def color(cls, color):
		return {
  			'OFF': 		0,
  			'RED':		1,
  			'GREEN':	2,
  			'BLUE': 	3,
  			'CYAN': 	4,
  			'YELLOW': 	5,
  			'PURPLE': 	6,
  			'WHITE': 	7
		}.get(color, 0)

	#
	# x = Arduino.city("DENVER")
	# returns base pin
	@classmethod
	def city(cls, city):
		return {
  			'DENVER':		22,
  			'BOULDER':		25,
  			'VAIL':			28,
  			'COLORADO SPRINGS': 	31,
  			'FORT COLLINS': 	34,
  			'PUEBLO': 		37,
  			'GRAND JUNCTION': 	40,
  			'LONGMONT': 		43,
  			'DURANGO': 		46,
  			'FORT MORGAN': 		49
		}.get(city, 0)

a = Arduino()
a.write("FORT MORGAN","RED")
time.sleep(.5)
a.write("LONGMONT","RED")
time.sleep(.5)
a.write("FORT MORGAN","BLUE")
time.sleep(.5)
a.write("LONGMONT","BLUE")
time.sleep(.5)
a.write("FORT MORGAN","GREEN")
time.sleep(.5)
a.write("LONGMONT","GREEN")
time.sleep(.5)
