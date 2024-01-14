cmake_minimum_required(VERSION 3.13)
set(PICO_BOARD pico_w)

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(valiant-turtle-2 C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(${PROJECT_NAME}
    main.c
    leds.c
    penservo.c
    cli.c
    command.c
    drivemotors.c
    i2cbus.c
    ina260.c
    ssd1306.c
    display.c
    buttons.c
    btcomms.c
    fifo.c
    )

pico_add_extra_outputs(${PROJECT_NAME})

target_link_libraries(${PROJECT_NAME} 
    pico_stdlib
    hardware_pwm
    hardware_clocks
    pico_cyw43_arch_none
    hardware_i2c
    pico_btstack_classic
    pico_btstack_ble
    pico_btstack_cyw43
    )

# Required for btstack_config.h
target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
    )

# Run as a bluetooth server
target_compile_definitions(${PROJECT_NAME} PRIVATE
    RUNNING_AS_CLIENT=0
    )

pico_enable_stdio_usb(${PROJECT_NAME} 0)
pico_enable_stdio_uart(${PROJECT_NAME} 1)
