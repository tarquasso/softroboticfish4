// buttons.h

#ifndef BUTTONS_H
#define BUTTONS_H

#include "mbed.h"

#define ADDR_BOARD_1        0x40
#define ADDR_BOARD_2        0x40

#define BTTN_COUNT_BOARD_1  6
#define BTTN_COUNT_BOARD_2  6
#define BTTN_COUNT          (BTTN_COUNT_BOARD_1 + BTTN_COUNT_BOARD_2)

// Commented indexes go from top left (0) to bottom right (5)
#define BTTN_FASTER      1  // 2
#define BTTN_SLOWER      2  // 1
#define BTTN_YAW_LEFT    4  // 0
#define BTTN_YAW_RIGHT   8  // 5
#define BTTN_PITCH_UP    16 // 4 // swims down
#define BTTN_PITCH_DOWN  32 // 3 // swims up
#define BTTN_RESET_MBED  36 // 0 and 3
#define BTTN_SHUTDOWN_PI 9  // 2 and 5
//#define BTTN_AUTO_MODE   18 // 1 and 4
#define BTTN_AUTO_MODE   33 // 2 and 3

class ButtonBoard
{
private:
    I2C _i2c;
    InterruptIn _int1;
    InterruptIn _int2;

    char out_buf[8];
    
    // Callback functions
    FunctionPointer _callback_table[BTTN_COUNT];
    bool _callback_table_valid[BTTN_COUNT];
    void (*_callbackFunction)(char buttonMask, bool pressed, char curState);
    
    // Interrupt handlers
    void _int1_handler();
    void _int2_handler();
    void _fall_handler(char board);
    
    // status
    volatile uint16_t _led_ports;
    volatile uint8_t _button_state;
    
public:
    ButtonBoard(PinName sda, PinName scl, PinName int1, PinName int2);
    ~ButtonBoard();
    
    void registerCallback(uint32_t button, FunctionPointer p);
    void registerCallback(void (*p)(char buttonMask, bool pressed, char curState));
    //void setLED(uint32_t led, bool val);
    void setLEDs(char mask, bool turnOn, char board = ADDR_BOARD_1);
    char getLEDs(char ledMask, char board = ADDR_BOARD_1);
    char getButtons(char buttonMask, char board = ADDR_BOARD_1);


    //uint16_t readInputs();
};

#endif
