from typing import Union, List
from instrument_lib.instrument_base import InstrumentBase


class KeysightE36312a(InstrumentBase):
    # Channel 1: 6V, 5A, 30W Channel 2: 25V, 1A, 25W, Channel 3: 25V, 1A, 25W
    def enable_output(self, ch: Union[int, str], enable: bool) -> None:
        self.write(f"OUTP {int(enable)},(@{ch})")
        return

    def set_output_current(self, ch: Union[int, str], current: float) -> None:
        self.write(f"CURR {current:.3f},(@{ch})")
        return

    def set_output_voltage(self, ch: Union[int, str], voltage: float) -> None:
        self.write(f"VOLT {voltage:.3f},(@{ch})")
        return

    def measure_current(self, ch: Union[int, str]) -> float:
        return float(self.query(f"MEAS:CURR?,(@{ch})"))

    def measure_voltage(self, ch: Union[int, str]) -> float:
        return float(self.query(f"MEAS:VOLT?,(@{ch})"))
