
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "mqtt_client.h"
#include "cJSON.h"

#define WIFI_SSID       "TuSSID"
#define WIFI_PASS       "TuPASS"
#define MQTT_BROKER_URI "mqtt://broker.hivemq.com"

#define DEVICE_ID "esp1"  // Cambiar por el mac del esp
// #define LAT -12.0453
#define LON -77.0311

static const char *TAG = "MQTT_CLIENT";
static esp_mqtt_client_handle_t client;

static void send_info() {
    wifi_ap_record_t ap_info;
    esp_wifi_sta_get_ap_info(&ap_info);
    int rssi = ap_info.rssi;

    cJSON *root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "id", DEVICE_ID);
    cJSON_AddNumberToObject(root, "lat", LAT);
    cJSON_AddNumberToObject(root, "lon", LON);
    cJSON_AddNumberToObject(root, "rssi", rssi);

    char *json_str = cJSON_PrintUnformatted(root);
    char topic[64];
    snprintf(topic, sizeof(topic), "response/%s", DEVICE_ID);
    esp_mqtt_client_publish(client, topic, json_str, 0, 0, 0);
    ESP_LOGI(TAG, "Datos enviados: %s", json_str);

    cJSON_Delete(root);
    free(json_str);
}

static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data) {
    esp_mqtt_event_handle_t event = event_data;
    switch ((esp_mqtt_event_id_t)event_id) {
        case MQTT_EVENT_CONNECTED:
            ESP_LOGI(TAG, "Conectado al broker, suscribiendo a request/info");
            esp_mqtt_client_subscribe(client, "request/info", 0);
            break;

        case MQTT_EVENT_DATA:
            if (strncmp(event->data, "SEND_INFO", event->data_len) == 0) {
                send_info();
            }
            break;

        default:
            break;
    }
}

void wifi_init(void) {
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "Conectando a WiFi...");
    esp_wifi_connect();
}

void mqtt_task(void *pvParameters) {
    esp_mqtt_client_config_t mqtt_cfg = {
        .broker.address.uri = MQTT_BROKER_URI,
    };

    client = esp_mqtt_client_init(&mqtt_cfg);
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, NULL);
    esp_mqtt_client_start(client);

    while (1) vTaskDelay(pdMS_TO_TICKS(1000));
}

void app_main(void) {
    ESP_ERROR_CHECK(nvs_flash_init());
    wifi_init();
    xTaskCreate(&mqtt_task, "mqtt_task", 4096, NULL, 5, NULL);
}
