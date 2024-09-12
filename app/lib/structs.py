import dataclasses

@dataclasses.dataclass
class BluetoothServiceInfo:
    """Prepared info from bluetooth entries."""

    name: str
    address: str
    rssi: int
    manufacturer_data: dict[int, bytes]
    service_data: dict[str, bytes]
    service_uuids: list[str]
    source: str
