// XIAO ESP32-C6 antenna switch. GPIO3 (WIFI_ENABLE) low powers the RF
// switch; GPIO14 (WIFI_ANT_CONFIG) low = onboard ceramic antenna, high =
// external U.FL. Call from on_boot at priority 1000, before any radio
// (Wi-Fi, BLE or 802.15.4) is initialised.
#pragma once
#include "driver/gpio.h"

inline void xiao_c6_rf_switch(bool external_antenna) {
  gpio_config_t cfg = {};
  cfg.pin_bit_mask = (1ULL << GPIO_NUM_3) | (1ULL << GPIO_NUM_14);
  cfg.mode = GPIO_MODE_OUTPUT;
  cfg.pull_up_en = GPIO_PULLUP_DISABLE;
  cfg.pull_down_en = GPIO_PULLDOWN_DISABLE;
  cfg.intr_type = GPIO_INTR_DISABLE;
  gpio_config(&cfg);
  gpio_set_level(GPIO_NUM_3, 0);
  gpio_set_level(GPIO_NUM_14, external_antenna ? 1 : 0);
}
