cmake_minimum_required(VERSION 3.13)
set(PICO_BOARD pico_w)

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(valiant-turtle-2 C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(${PROJECT_NAME}
    main.c
    debug.c
    cli.c
    i2cbus.c
    ina260.c
    penservo.c
    ${CMAKE_CURRENT_LIST_DIR}/embedded-cli/lib/src/embedded_cli.c
    )

pico_add_extra_outputs(${PROJECT_NAME})

target_link_libraries(${PROJECT_NAME} 
    pico_stdlib
    pico_cyw43_arch_none
    hardware_i2c
    hardware_pwm
    hardware_clocks
    )

# Required for btstack_config.h
target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/embedded-cli/lib/include
    )

# Run as a bluetooth server
target_compile_definitions(${PROJECT_NAME} PRIVATE
    RUNNING_AS_CLIENT=0
    )

pico_enable_stdio_usb(${PROJECT_NAME} 0)
pico_enable_stdio_uart(${PROJECT_NAME} 1)
