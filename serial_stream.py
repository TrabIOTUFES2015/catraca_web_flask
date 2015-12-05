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

class SerialStream( Stream ):
    """ A stream using the pyserial interface """
    def __init__( self, **kw ):
        """ Default constructor
        Creates and opens a serial port
        **kw - keyword arguments to pass into a pySerial serial port
        """
        Stream.__init__( self )
        self.port = Serial( **kw )
        #self.port.open() # Seems to cause "permission denied" with PySerial 2.x
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
            msg = self.read(100)           
            
            if msg:            
                msg = ''.join(i for i in msg if ord(i)<128)
                # print "servico:" + self.msg
                msgId += 1
                obj = {'id': msgId, 'msg': msg }
                
                # print "startService:" + str(self.leitura)

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
        self.port.flush()
    def read( self, count ):
        """ Read up to count bytes 
        count - maximum number of bytes to read
        throws TimeoutException if read returns empty or None
        """
        buf = ''
        try:
            buf = self.port.read( count )
        except SerialException:
            self.port.close()
            self.port.open()

        return buf
            
    def write( self, buf ):
        """ Write buf to the port 
        buf - string or list of bytes
        """
        if isinstance( buf, list ):
            buf = ''.join( [chr( c ) for c in buf] )
        self.port.write( buf )
    def get_read_timeout( self ):
        """ Get the read timeout """
        return self.port.timeout 
    def set_read_timeout( self, value ):
        """ Set the read timeout """
        self.port.timeout = value
    def get_write_timeout( self ):
        """ Get the write timeout """
        return self.port.writeTimeout 
    def set_write_timeout( self, value ):
        """ Set the write timeout """
        self.port.writeTimeout = value
    def close(self):
        self.port.close()