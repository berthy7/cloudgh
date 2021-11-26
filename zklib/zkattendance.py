from struct import pack, unpack
from datetime import datetime, date
import codecs
from zklib.zkconst import *


def getSizeAttendance(self):
    """Checks a returned packet to see if it returned CMD_PREPARE_DATA,
    indicating that data packets are to be sent

    Returns the amount of bytes that are going to be sent"""
    command = unpack('HHHH', self.data_recv[:8])[0]
    if command == CMD_PREPARE_DATA:
        size = unpack('I', self.data_recv[8:12])[0]
        return size
    else:
        return False


def reverseHex(hexstr):
    tmp = b''
    for i in iter(reversed(range(len(hexstr) // 2))):
        tmp += hexstr[i * 2:(i * 2) + 2]

    return tmp

def zkgetattendancebt(self, device):
    """Start a connection with the time clock"""
    command = CMD_ATTLOG_RRQ
    command_string = b''
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)

    self.data_recv, addr = self.zkclient.recvfrom(1024)

    if getSizeAttendance(self):
        bytes = getSizeAttendance(self)
        while bytes > 0:
            data_recv, addr = self.zkclient.recvfrom(1032)
            self.attendancedata.append(data_recv)
            bytes -= 1024
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        data_recv = self.zkclient.recvfrom(8)

    attendance = []
    if len(self.attendancedata) > 0:
        # The first 4 bytes don't seem to be related to the user
        for x in iter(range(len(self.attendancedata))):
            if x > 0:
                self.attendancedata[x] = self.attendancedata[x][8:]

        attendancedata = b''.join(self.attendancedata)

        attendancedata = attendancedata[zkcheckdevicerange(device):]

        sw = 0

        while len(attendancedata) > zkcheckdevicemax(device):
            if sw == 1:
                cero = b'\x00'
                attendancedata = b''.join([cero, attendancedata])

            uid, state, timestamp, space = unpack(zkcheckdevicemask(device), attendancedata.ljust(zkcheckdevicemax(device))[:zkcheckdevicemax(device)])

            xxx = b''.join([uid, state])

            a, b, c, d = unpack('1s1s1s6s', xxx.ljust(zkcheckdevicemax(device))[:zkcheckdevicemax(device)])

            codigo = b''.join([c, b])

            uid = zkdecodeuserid(device, codigo)
            if isinstance(uid, str):
                uid = int(uid.split('\x00')[0])
            if state == b'':
                state = b'\x00'
            attendance.append((uid, int(codecs.encode(state, 'hex_codec'), 16), decode_time(int(reverseHex(codecs.encode(timestamp, 'hex_codec')), 16))))
            attendancedata = attendancedata[zkcheckdevicemax(device):]

            sw = 1
        if sw == 1:
            cero = b'\x00'
            attendancedata = b''.join([cero, attendancedata])
        uid, state, timestamp, space = unpack(zkcheckdevicemask(device), attendancedata.ljust(zkcheckdevicemax(device))[:zkcheckdevicemax(device)])

        xxx = b''.join([uid, state])

        a, b, c, d = unpack('1s1s1s6s', xxx.ljust(zkcheckdevicemax(device))[:zkcheckdevicemax(device)])

        codigo = b''.join([c, b])

        uid = zkdecodeuserid(device, codigo)

        sw = 1

        #uid = zkdecodeuserid(device, uid)
        if uid != 32:
            if isinstance(uid, str):
                uid = int(uid.split('\x00')[0])
            if state == b'':
                state = b'\x00'
            attendance.append((uid, int(codecs.encode(state, 'hex_codec'), 16),
                               decode_time(int(reverseHex(codecs.encode(timestamp, 'hex_codec')), 16))))
            attendancedata = attendancedata[zkcheckdevicemax(device):]
    return attendance


def zkgetattendance(self, device):
    """Start a connection with the time clock"""
    command = CMD_ATTLOG_RRQ
    command_string = b''
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
                            reply_id, command_string)
    self.zkclient.sendto(buf, self.address)
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)

        if getSizeAttendance(self):
            bytes = getSizeAttendance(self)
            while bytes > 0:
                data_recv, addr = self.zkclient.recvfrom(1032)
                self.attendancedata.append(data_recv)
                bytes -= 1024
            self.session_id = unpack('HHHH', self.data_recv[:8])[2]
            data_recv = self.zkclient.recvfrom(8)

        attendance = []
        if len(self.attendancedata) > 0:
            # The first 4 bytes don't seem to be related to the user
            for x in iter(range(len(self.attendancedata))):
                if x > 0:
                    self.attendancedata[x] = self.attendancedata[x][8:]

            attendancedata = b''.join(self.attendancedata)

            attendancedata = attendancedata[zkcheckdevicerange(device):]

            while len(attendancedata) > zkcheckdevicemax(device):

                uid, state, timestamp, space = unpack(zkcheckdevicemask(device),
                                                      attendancedata.ljust(zkcheckdevicemax(device))[
                                                      :zkcheckdevicemax(device)])

                uid = zkdecodeuserid(device, uid)
                if isinstance(uid, str):
                    uid = int(uid.split('\x00')[0])
                if state == b'':
                    state = b'\x00'
                attendance.append((uid, int(codecs.encode(state, 'hex_codec'), 16),
                                   decode_time(int(reverseHex(codecs.encode(timestamp, 'hex_codec')), 16))))
                attendancedata = attendancedata[zkcheckdevicemax(device):]
            uid, state, timestamp, space = unpack(zkcheckdevicemask(device),
                                                  attendancedata.ljust(zkcheckdevicemax(device))[
                                                  :zkcheckdevicemax(device)])
            uid = zkdecodeuserid(device, uid)
            if uid != 32:
                if isinstance(uid, str):
                    uid = int(uid.split('\x00')[0])
                if state == b'':
                    state = b'\x00'
                attendance.append((uid, int(codecs.encode(state, 'hex_codec'), 16),
                                   decode_time(int(reverseHex(codecs.encode(timestamp, 'hex_codec')), 16))))
                attendancedata = attendancedata[zkcheckdevicemax(device):]
        return attendance
    except Exception as e:
        print(str(e))
        return False

# def zkgetattendance(self, device):
#     """Start a connection with the time clock"""
#     try:
#         command = CMD_ATTLOG_RRQ
#         command_string = b''
#         chksum = 0
#         session_id = self.session_id
#         reply_id = unpack('HHHH', self.data_recv[:8])[3]
#         buf = self.createHeader(command, chksum, session_id,
#                                 reply_id, command_string)
#         self.zkclient.sendto(buf, self.address)
#
#         self.data_recv, addr = self.zkclient.recvfrom(1024)
#         if getSizeAttendance(self):
#             bytes = getSizeAttendance(self)
#             while bytes > 0:
#                 data_recv, addr = self.zkclient.recvfrom(1032)
#                 self.attendancedata.append(data_recv)
#                 bytes -= 1024
#             self.session_id = unpack('HHHH', self.data_recv[:8])[2]
#             data_recv = self.zkclient.recvfrom(8)
#
#         attendance = []
#         if len(self.attendancedata) > 0:
#             # The first 4 bytes don't seem to be related to the user
#             for x in iter(range(len(self.attendancedata))):
#                 if x > 0:
#                     self.attendancedata[x] = self.attendancedata[x][8:]
#
#             attendancedata = b''.join(self.attendancedata)
#
#             attendancedata = attendancedata[zkcheckdevicerange(device):]
#
#             while len(attendancedata) > zkcheckdevicemax(device):
#
#                 uid, state, timestamp, space = unpack(zkcheckdevicemask(device),
#                                                       attendancedata.ljust(zkcheckdevicemax(device))[
#                                                       :zkcheckdevicemax(device)])
#
#                 xxx = b''.join([uid, state])
#
#                 a, b, c, d = unpack('1s1s1s13s', xxx.ljust(zkcheckdevicemax(device))[:zkcheckdevicemax(device)])
#
#                 codigo = b''.join([c, b])
#
#                 uid = zkdecodeuserid(device, codigo)
#                 if isinstance(uid, str):
#                     uid = int(uid.split('\x00')[0])
#                 if state == b'':
#                     state = b'\x00'
#                 attendance.append((uid, int(codecs.encode(state, 'hex_codec'), 16),
#                                    decode_time(int(reverseHex(codecs.encode(timestamp, 'hex_codec')), 16))))
#                 attendancedata = attendancedata[zkcheckdevicemax(device):]
#             uid, state, timestamp, space = unpack(zkcheckdevicemask(device),
#                                                   attendancedata.ljust(zkcheckdevicemax(device))[
#                                                   :zkcheckdevicemax(device)])
#             uid = zkdecodeuserid(device, uid)
#             if uid != 32:
#                 if isinstance(uid, str):
#                     uid = int(uid.split('\x00')[0])
#                 if state == b'':
#                     state = b'\x00'
#                 attendance.append((uid, int(codecs.encode(state, 'hex_codec'), 16),
#                                    decode_time(int(reverseHex(codecs.encode(timestamp, 'hex_codec')), 16))))
#                 attendancedata = attendancedata[zkcheckdevicemax(device):]
#         return attendance
#     except Exception as e:
#         print("Error en zkgetattendance: "+str(e))
#         return False

def zkdecodeuserid(device, userid):
     switcher ={
        'LP400/ID\x00': userid.decode('utf-8', 'ignore'),
        'MA300\x00': int(codecs.encode(userid, 'hex_codec').decode(), 16),
        'MA300-BT\x00': int(codecs.encode(userid, 'hex_codec').decode(), 16),
        'U580/ID\x00': int(reverseHex(codecs.encode(userid, 'hex_codec')), 16),
        'uFace800/ID\x00': userid.decode('utf-8', 'ignore')
     }
     return switcher.get(device, userid.decode('utf-8', 'ignore'))


def zkcheckdevicerange(device):
    switcher ={
        'LP400/ID\x00': 14,
        'MA300\x00': 11,
        'MA300-BT\x00': 11,
        'U580/ID\x00': 12,
        'uFace800/ID\x00': 14
    }
    return switcher.get(device, 14)


def zkcheckdevicemax(device):
    switcher = {
        'LP400/ID\x00': 40,
        'MA300\x00': 16,
        'MA300-BT\x00': 9,
        'U580/ID\x00': 16,
        'uFace800/ID\x00': 40
    }
    return switcher.get(device, 40)


def zkcheckdevicemask(device):
    switcher = {
        'LP400/ID\x00': '24s1s4s11s',
        'MA300\x00': '2s3s4s7s',
        'MA300-BT\x00': '2s3s4s0s',
        'U580/ID\x00': '4s0s4s8s',
        'uFace800/ID\x00': '24s1s4s11s'
    }
    return switcher.get(device, '24s1s4s11s')

def zkclearattendance(self):
    """Start a connection with the time clock"""
    command = CMD_CLEAR_ATTLOG
    command_string = b''
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
                            reply_id, command_string)
    self.zkclient.sendto(buf, self.address)
    # print buf.encode("hex")
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        return self.data_recv[8:]
    except:
        return False
