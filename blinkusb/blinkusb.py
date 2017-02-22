
import usb.core
import time
import sys
import select

class blinkusb:

    def __init__(self):
        self.TOGGLE_LED1 = 0
        self.SET_DUTY = 1
        self.GET_DUTY = 2
        self.MOTOR_ON = 3
        self.MOTOR_OFF = 4
        self.MOTOR_REV = 5
        self.ANG_READ = 6
        self.TOR_READ = 7
        self.dev = usb.core.find(idVendor = 0x6666, idProduct = 0x0003)
        if self.dev is None:
            raise ValueError('no USB device found matching idVendor = 0x6666 and idProduct = 0x0003')
        self.dev.set_configuration()

    def close(self):
        self.dev = None

    # def toggle_led1(self):
    #     try:
    #         self.dev.ctrl_transfer(0x40, self.TOGGLE_LED1)
    #     except usb.core.USBError:
    #         print "Could not send TOGGLE_LED1 vendor request."

    def set_duty(self, duty):
        try:
            self.dev.ctrl_transfer(0x40, self.SET_DUTY, int(duty))
        except usb.core.USBError:
            print "Could not send SET_DUTY vendor request."

    def get_duty(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.GET_DUTY, 0, 0, 2)
        except usb.core.USBError:
            print "Could not send GET_DUTY vendor request."
        else:
            return int(ret[0])+int(ret[1])*256

    def motor_on(self):
        try:
            self.dev.ctrl_transfer(0x40, self.MOTOR_ON)
        except usb.core.USBError:
            print "Could not send MOTOR_ON vendor request."

    def motor_off(self):
        try:
            self.dev.ctrl_transfer(0x40, self.MOTOR_OFF)
        except usb.core.USBError:
            print "Could not send MOTOR_OFF vendor request."

    def motor_rev(self):
        try:
            self.dev.ctrl_transfer(0x40, self.MOTOR_REV)
        except usb.core.USBError:
            print "Could not send MOTOR_REV vendor request."

    def ang_read(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.ANG_READ, 0, 0, 2)
        except usb.core.USBError:
            print "Could not send ANG_READ vendor request."
        else:
            return int(ret[0])+int(ret[1])*256

    def tor_read(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.TOR_READ, 0, 0, 2)
        except usb.core.USBError:
            print "Could not send TOR_READ vendor request."
        else:
            val = (int(ret[0])+256*(int(ret[1])))/(2**16-1.0)
            vout = val*3.3
            current = (vout-(0.5*3.3))/(10*75e-3)
            tor_real = (15.8e-3)*current
            return tor_real

    def spring(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.TOR_READ, 0, 0, 2)
        except usb.core.USBError:
            print "Could not send SPRING vendor request."
        else:
            while True:
                cur_pos = self.ang_read()
                rel_pos = cur_pos - 8000 # get pos and neg vals for pos
                # print ("LSB is " + str(int(ret[0])))
                # print ("MSB is " + str(int(ret[1])))
                tor_real = self.tor_read()
                # tor_ideal = 0.4e-3
                tor_ideal = cur_pos*0.01
                # diff = tor_ideal - tor_real
                if (rel_pos > 0):
                    self.motor_on()
                    self.set_duty(tor_ideal)
                    self.motor_off()
                elif (rel_pos < 0):
                    self.motor_rev()
                    self.set_duty(tor_ideal)
                    self.motor_off()
                else:
                    self.motor_off()
                if self.heardEnter():
                    break

    def heardEnter(self):
        i,o,e = select.select([sys.stdin],[],[],0.0001)
        for s in i:
            if s == sys.stdin:
                input = sys.stdin.readline()
                return True
        return False        # select module isn't compatible with windows

    def wall(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.TOR_READ, 0, 0, 2)
        except usb.core.USBError:
            print "Could not send WALL vendor request."
        else:
            while True:
                tor_real = self.tor_read()
                # print tor_real
                # return tor_real
                tor_ideal = 0.4e-3 # max torque
                cur_pos = self.ang_read()
                diff = abs(tor_ideal - tor_real)
                if (cur_pos > 14000):
                    print "I should be on (CC)"
                    self.motor_rev()
                    self.set_duty(diff)
                elif (cur_pos < 3000):
                    print "I should be on (C)"
                    self.motor_on()
                    self.set_duty(diff)
                else:
                    print "I should be off"
                    self.motor_off()
                if self.heardEnter():
                    break

    def damper(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.TOR_READ, 0, 0, 2)
        except usb.core.USBError:
            print "Could not send DAMPER vendor request."
        else:
            # while True:
            tor_real = self.tor_read()
            tor_ideal = 1.0e-4 # max torque
            # part = tor_real/tor_ideal
            diff = tor_ideal - tor_real
            val = (tor_ideal/tor_real)
            if (tor_real < 3e-4):
                print tor_real
                self.motor_rev()
                self.set_duty(val)
                self.motor_off()
            # return tor_real
            # cur_pos = self.ang_read()
            # time.sleep(0.05)
            # next_pos = self.ang_read()
            # diff_pos = cur_pos - next_pos
            # if (diff < 0):
            #     print "minus"
            #     self.motor_on()
            #     self.set_duty(tor_real)
            #     self.motor_off()
            elif (tor_real > 3e-4):
                print "off"
                self.motor_off()
            return tor_real
            # else:
            #     self.motor_off()
                # if self.heardEnter():
                #     break
    
    def texture(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.TOR_READ, 0, 0, 2)
        except usb.core.USBError:
            print "Could not send TEXTURE vendor request."
        else:
            while True:
                tor_real = self.tor_read()
                # print tor_real
                # return tor_real
                tor_ideal = 0.4e-3 # max torque
                cur_pos = self.ang_read()
                diff = abs(tor_ideal - tor_real)
            # make it slip
                if (cur_pos > 15000):
                    self.motor_rev()
                    self.set_duty(0x4000)
                    self.motor_off()
                elif (cur_pos < 2000):
                    self.motor_rev()
                    self.set_duty(0x4000)
                    self.motor_off()
            # make it stick
                elif (3000 < cur_pos < 3500):
                    self.motor_on()
                    self.set_duty(0x4000)
                    self.motor_off()
                elif (10000 < cur_pos < 10500):
                    self.motor_on()
                    self.set_duty(0x4000)
                    self.motor_off()
                else:
                    self.motor_off()
                if self.heardEnter():
                    break

if __name__ == '__main__':
    action = blinkusb()
    action.motor_off()
    result = []
    t_res = []
    # while True:
    for t in range(0,100):
        action.damper()
# #         self.motor_off()
        result.append(action.ang_read())
        t_res.append(action.damper())
        time.sleep(0.1)     
#         # self.spring()
    print result
    print t_res
#         res = self.ang_read()
#         print res
#     self.motor_on()
#     self.set_duty(0x4000)
#     time.sleep(5)
#     print "turning off" 
#     self.motor_off()

