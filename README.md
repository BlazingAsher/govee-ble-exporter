# Govee BLE Exporter
Prometheus exporter for Govee BLE temperature/humidity sensors.

This application is built off the work of https://github.com/Bluetooth-Devices/govee-ble (the lib/govee_ble.py is effectively the same as parser.py).
The biggest change is the removal of anything HomeAssistant related as a dependency by using our own structs.
Updating the file should be as easy as copying it over and changing the imports, making sure no new fields/structs are needed.

The device's recorded temperature, humidity, battery level, signal strength, and last data update is recorded as a gauge metric.
We cache the values instead of determining them at scrape-time because the BLE discovery process takes some time.
In addition, to avoid constantly spamming surrounding Bluetooth devices, we only scan for updates every `SCAN_FREQUENCY` (default 900) seconds for `SCAN_DURATION` (default 15) seconds.

All options can be found in `app/utils/constants.py` and are configured with environment variables.

This has only been tested against the H5100 sensor, but I see no reason why it wouldn't work for any other sensors supported by the Bluetooth-Devices project.