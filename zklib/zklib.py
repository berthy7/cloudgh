from socket import *
import sys
import select
import errno
import time

from struct import pack, unpack
from datetime import datetime, date

from zklib.zkconnect import *
from zklib.zkversion import *
from zklib.zkos import *
from zklib.zkextendfmt import *
from zklib.zkextendoplog import *
from zklib.zkplatform import *
from zklib.zkworkcode import *
from zklib.zkssr import *
from zklib.zkpin import *
from zklib.zkface import *
from zklib.zkserialnumber import *
from zklib.zkdevice import *
from zklib.zkuser import *
from zklib.zkattendance import *
from zklib.zktime import *

class ZKLib:
    
    def __init__(self, ip, port):
        self.address = (ip, port)
        self.zkclient = socket(AF_INET, SOCK_DGRAM)
        self.zkclient.settimeout(3)
        self.session_id = 0
        self.userdata = []
        self.attendancedata = []
    
    def createChkSum(self, p):
        """This function calculates the chksum of the packet to be sent to the 
        time clock

        Copied from zkemsdk.c"""
        l = len(p)
        chksum = 0
        while l > 1:
            chksum += unpack('H', pack('BB', p[0], p[1]))[0]
            
            p = p[2:]
            if chksum > USHRT_MAX:
                chksum -= USHRT_MAX
            l -= 2

        if l:
            chksum = chksum + p[-1]
            
        while chksum > USHRT_MAX:
            chksum -= USHRT_MAX
        
        chksum = ~chksum
        
        while chksum < 0:
            chksum += USHRT_MAX
        
        return pack('H', chksum)

    def createHeader(self, command, chksum, session_id, reply_id, 
                                command_string):
        """This function puts a the parts that make up a packet together and 
        packs them into a byte string"""
        buf = pack('HHHH', command, chksum,
            session_id, reply_id) + command_string
        
        buf = unpack('8B'+'%sB' % len(command_string), buf)
        
        chksum = unpack('H', self.createChkSum(buf))[0]
        #print unpack('H', self.createChkSum(buf))
        reply_id += 1
        if reply_id >= USHRT_MAX:
            reply_id -= USHRT_MAX

        buf = pack('HHHH', command, chksum, session_id, reply_id)
        return buf + command_string

    def checkValid(self, reply):
        """Checks a returned packet to see if it returned CMD_ACK_OK,
        indicating success"""
        command = unpack('HHHH', reply[:8])[0]
        if command != 2000:
            command = 2000
        if command == CMD_ACK_OK:
            return True
        else:
            return False
            
    def connect(self):
        return zkconnect(self)
            
    def disconnect(self):
        return zkdisconnect(self)
        
    def version(self):
        return zkversion(self)
        
    def osversion(self):
        return zkos(self)
        
    def extendFormat(self):
        return zkextendfmt(self)
    
    def extendOPLog(self, index=0):
        return zkextendoplog(self, index)
    
    def platform(self):
        return zkplatform(self)
    
    def fmVersion(self):
        return zkplatformVersion(self)
        
    def workCode(self):
        return zkworkcode(self)
        
    def ssr(self):
        return zkssr(self)
    
    def pinWidth(self):
        return zkpinwidth(self)
    
    def faceFunctionOn(self):
        return zkfaceon(self)
    
    def serialNumber(self):
        return zkserialnumber(self)
    
    def deviceName(self):
        return zkdevicename(self)
        
    def disableDevice(self):
        return zkdisabledevice(self)
    
    def enableDevice(self):
        return zkenabledevice(self)
        
    def getUser(self):
        device = zkdevicename(self)
        return zkgetuser(self, device.decode())
        
    def setUser(self, uid, userid, name, password, role):
        return zksetuser(self, uid, userid, name, password, role)
        
    def clearUser(self):
        return zkclearuser(self)
    
    def clearAdmin(self):
        return zkclearadmin(self)

    def getAttendance(self):
        device = zkdevicename(self)
        print(device.decode())
        return zkgetattendance(self, device.decode())

    # def getAttendance(self):
    #     device = zkdevicename(self)
    #     if device ==b'MA300-BT\x00':
    #         print("Ma300 BT")
    #         return zkgetattendancebt(self, device.decode())
    #     else:
    #         print(device.decode())
    #         return zkgetattendance(self, device.decode())

    def clearAttendance(self):
        return zkclearattendance(self)
        
    def setTime(self, t):
        return zksettime(self, t)
    
    def getTime(self):
        return zkgettime(self)
