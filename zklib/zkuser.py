from struct import pack, unpack
from datetime import datetime, date
from zklib.zkdevice import zkdevicename
from zklib.zkconst import *
from zklib.zkattendance import *
import codecs


def getSizeUser(self):
    """Checks a returned packet to see if it returned CMD_PREPARE_DATA,
    indicating that data packets are to be sent

    Returns the amount of bytes that are going to be sent"""
    command = unpack('HHHH', self.data_recv[:8])[0] 
    if command == CMD_PREPARE_DATA:
        size = unpack('I', self.data_recv[8:12])[0]
        return size
    else:
        return False


def zksetuser(self, uid, userid, name, password, role):
    """Start a connection with the time clock"""
    command = CMD_SET_USER
    command_string = pack('sxs8s28ss7sx8s16s', chr( uid ), chr(role), password, name, chr(1), '', userid, '' )
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        return self.data_recv[8:]
    except:
        return False


def zkgetuser(self, device):
    """Start a connection with the time clock"""
    command = CMD_USERTEMP_RRQ
    command_string = b'\x05'
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]
    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        if getSizeUser(self):
            bytes = getSizeUser(self)

            while bytes > 0:
                data_recv, addr = self.zkclient.recvfrom(1032)
                self.userdata.append(data_recv)
                bytes -= 1024

            self.session_id = unpack('HHHH', self.data_recv[:8])[2]
            data_recv = self.zkclient.recvfrom(8)

        users = {}
        if len(self.userdata) > 0:
            # The first 4 bytes don't seem to be related to the user
            for x in iter(range(len(self.userdata))):
                if x > 0:
                    self.userdata[x] = self.userdata[x][8:]

            userdata = b''.join(self.userdata)
            userdata = userdata[zkcheckdevicerange(device):]
            while len(userdata) > zkcheckdevicemax(device):
                uid, role, password, name, target, dd, userid = unpack(zkcheckdevicemask(device),
                                                                       userdata.ljust(zkcheckdevicemax(device))[
                                                                       :zkcheckdevicemax(device)])
                uid = int(codecs.encode(uid, 'hex_codec'), 16)
                # Clean up some messy characters from the user name
                password = password.split(b'\x00', 1)[0]
                password = password.strip(b'\x00|\x01\x10x').decode('utf-8', 'ignore')
                # password = str(reverseHex(codecs.encode(password, 'hex_codec')))
                name = name.split(b'\x00', 1)[0]
                name = name.decode('utf-8', 'ignore')
                userid = zkdecodeuserid(device, userid)
                users[uid] = (str(userid), str(name), int(codecs.encode(role, 'hex_codec'), 16), str(password))
                userdata = userdata[zkcheckdevicemax(device):]
        return users
    except Exception as e:
        print(str(e))
        return False


def zkcheckdevicerange(device):
    return{
        'LP400/ID\x00': 11,
        'MA300\x00': 10
    }[device]


def zkdecodeuserid(device, userid):
    return{
        'LP400/ID\x00': userid.decode('utf-8', 'ignore'),
        'MA300\x00': int(reverseHex(codecs.encode(userid, 'hex_codec')), 16)
    }[device]


def zkcheckdevicemax(device):
    return{
        'LP400/ID\x00': 72,
        'MA300\x00': 28
    }[device]


def zkcheckdevicemask(device):
    return{
        'LP400/ID\x00': b'2s2s24s12sx2s6s23s',
        'MA300\x00': b'3s3s4s8sx5s2s2s'
    }[device]


def zkclearuser(self):
    """Start a connection with the time clock"""
    command = CMD_CLEAR_DATA
    command_string = b''
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)
    #print buf.encode("hex")
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        return self.data_recv[8:]
    except:
        return False


def zkclearadmin(self):
    """Start a connection with the time clock"""
    command = CMD_CLEAR_ADMIN
    command_string = b''
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)
    #print buf.encode("hex")
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        return self.data_recv[8:]
    except:
        return False
