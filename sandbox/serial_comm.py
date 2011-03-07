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
  			'BOULDER':		28,
  			'VAIL':			34,
  			'COLORADO SPRINGS': 	40,
  			'FORT COLLINS': 	46,
  			'PUEBLO': 		23,
  			'GRAND JUNCTION': 	29,
  			'LONGMONT': 		35,
  			'DURANGO': 		41,
  			'FORT MORGAN': 		47
		}.get(city, 0)

a = Arduino()
a.write("DENVER","RED")
a.write("BOULDER","RED")
time.sleep(.5)
#a.write("BOULDER","RED")
#time.sleep(.5)
#a.write("DENVER","BLUE")
#time.sleep(.5)
#a.write("BOULDER","BLUE")
#time.sleep(.5)
#a.write("DENVER","GREEN")
#time.sleep(.5)
#a.write("BOULDER","GREEN")
#time.sleep(.5)
