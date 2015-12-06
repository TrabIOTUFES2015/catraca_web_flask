"""
This is a Python version of the ForestMoon Dynamixel library originally
written in C# by Scott Ferguson.
The Python version was created by Patrick Goebel (mailto:patrick@pirobot.org)
for the Pi Robot Project which lives at http://www.pirobot.org.
The original license for the C# version is as follows:
This software was written and developed by Scott Ferguson.
The current version can be found at http://www.forestmoon.com/Software/.
This free software is distributed under the GNU General Public License.
See http://www.gnu.org/licenses/gpl.html for details.
This license restricts your usage of the software in derivative works.
* * * * * 
An implementation of the Steam interface using pyserial
"""

try:
    # PySerial Module
    from serial import Serial, SerialException
except:
    print "This module requires the pySerial to be installed \
to use the Serial Stream"


from stream import Stream #, TimeoutException
from threading import Thread
import time
from collections import deque
from tos import AM, Serial as SerialTOS

def serialStreamProcessorHook(packet):
    if not packet or packet.type != 100:
        return
    else:
        s = "".join([chr(i) for i in packet.data]).strip('\0')
        # lines = s.split('\n')
        # for line in lines:
        #     if line: print "PRINTF:", line
        return s
        

class SerialStream( Stream ):
    """ A stream using the pyserial interface """
    # def __init__( self, **kw ):
    #     """ Default constructor
    #     Creates and opens a serial port
    #     **kw - keyword arguments to pass into a pySerial serial port
    #     """
    def __init__(self, port, baudrate):
        # Stream.__init__( self )
        # self.am = Serial( **kw )
        #self.am.open() # Seems to cause "permission denied" with PySerial 2.x
        self.am = AM(SerialTOS(port, baudrate), serialStreamProcessorHook)
        self.handlersList = []         
        t = Thread(target=self.startService)
        t.setDaemon(True)
        t.start()
        # t.join(5)
        self.servico = t
        self.msg = ''
        self.msgId = 1
        self.leitura = deque(maxlen=4)



    def startService(self):
        msgId = 0
        str_list = []
        print 'iniciando servico'
        while True:
            time.sleep(0.02)
            msgRead = self.read()     

            
            if msgRead:          
                msgs = msgRead.split('\n')   
                for msg in msgs:
                    if (msg):
                        # msg = ''.join(i for i in msg if ord(i)<128)
                        # print "servico:" + self.msg
                        msgId += 1
                        obj = {'id': msgId, 'msg': msg }
                        
                        print "startService:" + msg

                        if (obj not in self.leitura):
                            self.leitura.append(obj)

                        for handler in self.handlersList:
                            handler(self.msgId, self.msg)

    #obs deve implementar chegouMsg
    def subscribe(self, handler):
        if handler not in self.handlersList:
            self.handlersList.append(handler)

    def last_msg(self):        
        obj = None
        if self.leitura:
            # print "last_msg:" + str(self.leitura)
            obj = self.leitura[-1]
 #       print obj
        return obj

    def flush( self ):
        """ Flush the port """
        self.am.flush()
    def read(self):
        """ Read up to count bytes 
        count - maximum number of bytes to read
        throws TimeoutException if read returns empty or None
        """
        buf = self.am.read()
        print 'Read: ', buf
        return buf
            
    def write( self, buf ):
        """ Write buf to the port 
        buf - string or list of bytes
        """
        if isinstance( buf, list ):
            buf = ''.join( [chr( c ) for c in buf] )
        self.am.write( buf )
    def get_read_timeout( self ):
        """ Get the read timeout """
        return self.am.timeout 
    def set_read_timeout( self, value ):
        """ Set the read timeout """
        self.am.timeout = value
    def get_write_timeout( self ):
        """ Get the write timeout """
        return self.am.writeTimeout 
    def set_write_timeout( self, value ):
        """ Set the write timeout """
        self.am.writeTimeout = value
    def close(self):
        self.am.close()