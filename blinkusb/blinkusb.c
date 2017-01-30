#include <p24FJ128GB206.h>
#include "config.h"
#include "common.h"
#include "usb.h"
#include "pin.h"
#include "ui.h"
#include "oc.h"
#include "timer.h"

#define TOGGLE_LED1 0   // Changes state of LED
#define SET_DUTY    1   // What % of cycle is high
#define GET_DUTY    2   // 
#define MOTOR_ON    3   //
#define MOTOR_OFF   4
#define MOTOR_REV   5

_PIN*nCS1;
_PIN*nCS2;
_PIN*MOSI;
_PIN*MISO;

MOSI = &D[0];
MISO = &D[1];
nCS1 = &D[3];
nCS2 = &D[4];
// uint16_t oc1;

//void ClassRequests(void) {
//    switch (USB_setup.bRequest) {
//        default:
//            USB_error_flags |= 0x01;                    // set Request Error Flag
//    }
//}

void VendorRequests(void) {
    WORD temp, angle;

    switch (USB_setup.bRequest) {
        case MOTOR_ON:
            pin_write(&D[5],0xFFFF);
            pin_write(&D[6],0x0000);
            // pin_clear(&D[6]);
            BD[EP0IN].bytecount = 0;    // set EP0 IN byte count to 0 
            BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit
            break;
        case MOTOR_OFF:
            pin_write(&D[5],0x0000);
            pin_write(&D[6],0x0000);
            BD[EP0IN].bytecount = 0;    // set EP0 IN byte count to 0 
            BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit
            break;
        // case TOGGLE_LED1:
        // 	led_toggle(&led1);
        //     BD[EP0IN].bytecount = 0;    // set EP0 IN byte count to 0 
        //     BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit
        //     break;
        case ANG_SENSE:
            pin_clear(nCS1);
            angle.b[1] = spi.transfer(&spi1, 0);
            angle.b[0] = spi.transfer(&spi2, 0);
            pin_set(nCS1);
            break;    
        case MOTOR_REV:
            pin_write(&D[5],0x0000);
            pin_write(&D[6],0xFFFF);
            BD[EP0IN].bytecount = 0;    // set EP0 IN byte count to 0 
            BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit
            break;
       	case SET_DUTY:
       		pin_write(&D[5], USB_setup.wValue.w);
       		BD[EP0IN].bytecount = 0;    // set EP0 IN byte count to 0 
            BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit
       		break;
        case GET_DUTY:
        	temp.w = pin_read(&D[5]);
        	BD[EP0IN].address[0] = temp.b[0];
        	BD[EP0IN].address[1] = temp.b[1];
        	BD[EP0IN].bytecount = 2;    // set EP0 IN byte count to 2 
            BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit
        	break;
        default:
            USB_error_flags |= 0x01;    // set Request Error Flag
    }
}

void VendorRequestsIn(void) {
    switch (USB_request.setup.bRequest) {
        default:
            USB_error_flags |= 0x01;                    // set Request Error Flag
    }
}

void VendorRequestsOut(void) {
    switch (USB_request.setup.bRequest) {
        default:
            USB_error_flags |= 0x01;                    // set Request Error Flag
    }
}

int16_t main(void) {
    init_clock();
    init_ui();
    init_pin();
    init_oc();

    // oc_pwm(&oc1, &D[13], NULL, 10e3, 0x8000);
    oc_pwm(&oc1, &D[5], NULL, 10e3, 0x8000);
    oc_pwm(&oc2, &D[6], NULL, 10e3, 0x8000);

    InitUSB();                              // initialize the USB registers and serial interface engine
    while (USB_USWSTAT!=CONFIG_STATE) {     // while the peripheral is not configured...
        ServiceUSB();                       // ...service USB requests
    }
    while (1) {
        ServiceUSB();                       // service any pending USB requests
    }
}

