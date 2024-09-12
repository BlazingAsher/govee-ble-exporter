"""
Detection callback w/ scanner
--------------

Example showing what is returned using the callback upon detection functionality

Updated on 2020-10-11 by bernstern <bernie@allthenticate.net>
Updated on 2025-09-12 by BlazingAsher

"""

import asyncio
import logging
import time

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from prometheus_client import Gauge

from sensor_state_data import SensorLibrary, DeviceClass, DeviceKey

from app.lib.structs import BluetoothServiceInfo
from app.lib.govee_ble import GoveeBluetoothDeviceData

logger = logging.getLogger(__name__)

current_temperature = Gauge("govee_sensor_temperature", "Current temperature in celsius.", ['device_name'])
current_relative_humidity = Gauge("govee_sensor_relative_humidity", "Current relative humidity in percentage.", ['device_name'])
current_battery = Gauge("govee_sensor_battery", "Current battery level in percentage.", ['device_name'])
current_signal_strength = Gauge("govee_sensor_signal_strength", "Current signal strength to the sensor in dBm.", ['device_name'])
last_received_update = Gauge("govee_sensor_last_update", "Time of last update from the sensor in Unix epoch seconds.", ['device_name'])

TEMPERATURE_KEY = DeviceKey(
    key=SensorLibrary.TEMPERATURE__CELSIUS.device_class.value
)
HUMIDITY_KEY = DeviceKey(
    key=SensorLibrary.HUMIDITY__PERCENTAGE.device_class.value
)
BATTERY_KEY = DeviceKey(
    key=SensorLibrary.BATTERY__PERCENTAGE.device_class.value
)
SIGNAL_STRENGTH_KEY =  DeviceKey(
    key=DeviceClass.SIGNAL_STRENGTH.value
)

def simple_callback(device: BLEDevice, advertisement_data: AdvertisementData):
    service_info = BluetoothServiceInfo(
        name=advertisement_data.local_name,
        address=device.address,
        rssi=advertisement_data.rssi,
        manufacturer_data=advertisement_data.manufacturer_data,
        service_data=advertisement_data.service_data,
        service_uuids=advertisement_data.service_uuids,
        source="govee-exporter"
    )

    if not service_info.name or not service_info.name.startswith("GV"):
        return
    else:
        logger.info("%s (%s): %r", service_info.name, device.address, advertisement_data)

    govee_device = GoveeBluetoothDeviceData()
    update_info = govee_device.update(service_info)
    device_name = govee_device.get_device_name()

    current_temperature.labels(device_name=device_name).set(update_info.entity_values.get(TEMPERATURE_KEY).native_value)
    current_relative_humidity.labels(device_name=device_name).set(update_info.entity_values.get(HUMIDITY_KEY).native_value)
    current_battery.labels(device_name=device_name).set(update_info.entity_values.get(BATTERY_KEY).native_value)
    current_signal_strength.labels(device_name=device_name).set(update_info.entity_values.get(SIGNAL_STRENGTH_KEY).native_value)

    last_received_update.labels(device_name=device_name).set(time.time())

async def run():
    scanner = BleakScanner(
        simple_callback, None, scanning_mode="active"
    )
    logger.info("Starting Bluetooth scanner.")
    async with scanner:
        await asyncio.sleep(15.0)
