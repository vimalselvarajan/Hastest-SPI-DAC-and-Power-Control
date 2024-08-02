from pyvisa import ResourceManager
from pyvisa.resources import MessageBasedResource


class InstrumentBase:

    def __init__(self, resource_name: str, timeout: int = 5000):
        self._resource = None
        rm = ResourceManager()
        self._resource: MessageBasedResource = rm.open_resource(resource_name)
        self._resource.timeout = timeout

    def clear(self) -> None:
        self._resource.write("*CLS")

    def close(self) -> None:
        self._resource.close()

    def get_id(self) -> str:
        response = self._resource.query("*IDN?")
        return response

    def query(self, command: str) -> str:
        response = self._resource.query(command)
        return response

    def read(self) -> str:
        response = self._resource.read()
        return response

    def reset(self) -> None:
        self._resource.write("*RST")

    def write(self, command: str) -> None:
        self._resource.write(command)
