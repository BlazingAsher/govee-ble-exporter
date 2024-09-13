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

## Installing
Since Docker doesn't really play well with Bluetooth, you can run this as a systemd service. These instructions assume that you will install the exporter at `/opt/govee-ble-exporter`.

1. Create a user for the exporter to run under: `sudo useradd --system --no-create-home --shell /usr/sbin/nologin govee-ble-exporter`.
1. Go to the `/opt` folder and clone the git repository.
1. Give the user ownership of the directory: `sudo chown govee-ble-exporter: /opt/govee-ble-exporter`.
1. Change into the repository directory: `cd govee-ble-exporter`.
1. Create the venv: `sudo su govee-ble-exporter -s /bin/sh -c "python3 -m venv venv"`.
1. Install all dependencies: `sudo su govee-ble-exporter -s /bin/sh -c "python3 -m pip install -r requirements.txt"`.
1. Create the service file `/etc/systemd/system/govee-ble-exporter.service` using the template `docs/govee-ble-exporter.service`.
1. Create the defaults file `/etc/default/govee-ble-exporter`.
   - Leave the file blank to use all the default options (see `app/utils/constants.py`).
   - If your Prometheus instance isn't running locally, you'll probably need to add the line `LISTEN_ADDRESS=0.0.0.0`. Otherwise, the exporter will only listen on localhost.
1. Reload systemd: `sudo systemctl daemon-reload`.
1. Start and enable the service to run at startup: `sudo systemctl enable --now govee-ble-exporter.service`.
1. Configure Prometheus to scrape the exporter:
    ```
   scrape_configs:
     - job_name: "govee_ble_exporter"
       scrape_interval: "1m"
       static_configs:
         - targets: ["<exporter IP address>:8000"]
   ```
   
## Updating
To update the exporter, you can run a git pull when you're in the repository directory (eg. `/opt/govee-ble-exporter`): `sudo su govee-ble-exporter -s /bin/sh -c "git pull"`.
Then, simply restart the service using systemd: `sudo systemctl restart govee-ble-exporter.service`.