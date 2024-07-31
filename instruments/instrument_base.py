from pyvisa import ResourceManager
from pyvisa.resources import MessageBasedResource

class InstrumentBase:
    def __init__(self, resource_name: str):
        rm = ResourceManager()
        self._resource: MessageBasedResource = rm.open_resource(resource_name)

    def clear(self) -> None:
        self._resource.write("*CLS")

    def close(self) -> None:
        self._resource.close()

    def get_id(self) -> str:
        return self._resource.query("*IDN?")

    def query(self, command: str) -> str:
        return self._resource.query(command)

    def read(self) -> str:
        return self._resource.read()

    def reset(self) -> None:
        self._resource.write("*RST")

    def write(self, command: str) -> None:
        self._resource.write(command)

    def get_scan_mode(self) -> str:
        return self.query("ROUT:SCAN?")
