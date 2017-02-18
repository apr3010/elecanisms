
import usb.core
import time

class blinkusb:

    def __init__(self):
        self.TOGGLE_LED1 = 0
        self.SET_DUTY = 1
        self.GET_DUTY = 2
        self.MOTOR_ON = 3
        self.MOTOR_OFF = 4
        self.MOTOR_REV = 5
        self.ANG_READ = 6
        self.SPRING = 7
        self.WALL = 8
        self.DAMPER = 9
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

    def spring(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.SPRING, 0, 0, 2)
        except usb.core.USBError:
            print "Could not send SPRING vendor request."
        else:
            cur_pos = action.ang_read()
            # print ("LSB is " + str(int(ret[0])))
            # print ("MSB is " + str(int(ret[1])))
            # val = (int(ret[0])+256*(int(ret[1])))/(2**16-1.0)
            # vout = val*3.3
            # current = (vout-(0.5*3.3))/(10*75e-3)
            # tor_real = (15.8e-3)*current
            # return vout, current, tor_real
            if (cur_pos > 12285):
                diff = cur_pos - 12285
                action.motor_on()
                action.set_duty(hex(diff))
            elif (cur_pos < 12285):
                diff = abs(cur_pos - 12285)
                action.motor_rev()
                action.set_duty(hex(diff))
            else:
                action.motor_off()


    def wall(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.ANG_READ, 0, 0, 2)
        except usb.core.USBError:
            print "Could not send WALL vendor request."
        else:
            cur_pos = action.ang_read()
            if (cur_pos > 4700):
                print "I should be on (CC)"
                action.motor_rev()
                action.set_duty(0x8000)
            elif (cur_pos < 2000):
                print "I should be on (C)"
                action.motor_on()
                action.set_duty(0x8000)
            else:
                print "I should be off"
                action.motor_off()
                # action.set_duty(0x0000)

    # def damper(self):
    #     try:
    #         ret = self.dev.ctrl_transfer(0xC0, self.DAMPER, 0, 0, 2)
    #     except usb.core.USBError:
    #         print "Could not send DAMPER vendor request."
    #     else:
    #         val = (int(ret[0])+256*(int(ret[1])))/(2**16-1.0)
    #         vout = val*3.3
    #         current = (vout-(0.5*3.3))/(10*75e-3)
    #         tor_real = (15.8e-3)*current
    #         # torque = tor_real*constant
    #         set_duty(torque)

if __name__ == '__main__':
    action = blinkusb()
    while True:
        action.spring()
#         action.motor_off()
#         action.wall()
#         res = action.ang_read()
#         print res
#     action.motor_on()
#     action.set_duty(0x4000)
#     time.sleep(5)
#     print "turning off" 
#     action.motor_off()
#     result = []
#     for t in range(0,1000):
#         time.sleep(0.001)
#         result.append(action.ang_read())
#     print result
