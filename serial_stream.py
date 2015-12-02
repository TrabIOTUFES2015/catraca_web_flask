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
    import serial
except:
    print "This module requires the pySerial to be installed \
to use the Serial Stream"


from stream import Stream #, TimeoutException
from threading import Thread

class SerialStream( Stream ):
    """ A stream using the pyserial interface """
    def __init__( self, **kw ):
        """ Default constructor
        Creates and opens a serial port
        **kw - keyword arguments to pass into a pySerial serial port
        """
        Stream.__init__( self )
        self.port = serial.Serial( **kw )
        #self.port.open() # Seems to cause "permission denied" with PySerial 2.x
        self.listObservadores = []         
        t = Thread(target=self.startService)
        t.start()
        self.servico = t



    def startService(self):


        str_list = []
        while True:
            sleep(0.01)
            nextchar = self.read(100)
            if nextchar:
                str_list.append(nextchar)
            else:
                if len(str_list) > 0:
                    # yield 'id:' + str(messageid2) + '\n' + 'data:' + ''.join(str_list) + '\n\n'
                    # messageid2 += 1
                    # str_list = []
                    msg = ''.join(str_list)
                    for obs in self.listObservadores:
                        obs.chegouMsg(msg)

    #obs deve implementar chegouMsg
    def subscribe(self, obs):
        self.listObservadores.append(obs)

    def flush( self ):
        """ Flush the port """
        self.port.flush()
    def read( self, count ):
        """ Read up to count bytes 
        count - maximum number of bytes to read
        throws TimeoutException if read returns empty or None
        """
        buf = self.port.read( count )
        # if len( buf ) == 0:
        #     raise TimeoutException()
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