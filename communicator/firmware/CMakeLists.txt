cmake_minimum_required(VERSION 3.13)
set(PICO_BOARD pico_w)

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(vt2-communicator C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(${PROJECT_NAME}
    main.c
    uart.c
    leds.c
    btcomms.c
    fifo.c
    )

pico_add_extra_outputs(${PROJECT_NAME})


target_link_libraries(${PROJECT_NAME} 
    pico_stdlib
    pico_cyw43_arch_none
    hardware_clocks
    hardware_uart
    pico_btstack_classic
    pico_btstack_ble
    pico_btstack_cyw43
    )

# Include external libraries
target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
    )

# Run as a bluetooth server/client
target_compile_definitions(${PROJECT_NAME} PRIVATE
    RUNNING_AS_CLIENT=1
    )

# Enable USB stdio
pico_enable_stdio_usb(${PROJECT_NAME} 1)
pico_enable_stdio_uart(${PROJECT_NAME} 0)
