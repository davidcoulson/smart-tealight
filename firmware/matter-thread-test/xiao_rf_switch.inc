// XIAO ESP32-C6 RF switch. Paste into main/app_main.cpp:
//   1. this include near the other #includes
#include "driver/gpio.h"

//   2. this block as the first thing in app_main(), before nvs_flash_init()
{
    // GPIO3 (WIFI_ENABLE) low powers the RF switch; GPIO14 (WIFI_ANT_CONFIG)
    // low = onboard ceramic antenna, high = external U.FL. Must happen before
    // the BLE / 802.15.4 radio is initialised.
    gpio_config_t rf = {
        .pin_bit_mask = (1ULL << GPIO_NUM_3) | (1ULL << GPIO_NUM_14),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&rf);
    gpio_set_level(GPIO_NUM_3, 0);
    gpio_set_level(GPIO_NUM_14, 0); // 1 for the external antenna
}
