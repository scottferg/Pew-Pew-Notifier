# import serial

port = 0

'''
This needs to hold a persistent state.  Either it's notifying or not.
'''

def notify():
    '''Send value to serial port'''
    # port.write('1');
    print 'NOTIFICATION'

def init():
    '''Connect to the serial port'''
    global port
    # TODO: Make this OS-centric
    # port = serial.Serial('COM3', 9600)
    pass
