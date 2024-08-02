from instrument_lib.instrument_base import InstrumentBase


class KeysightE36312a(InstrumentBase):
    # Channel 1: 6V, 5A, 30W Channel 2: 25V, 1A, 25W, Channel 3: 25V, 1A, 25W
    def enable_output(self, ch: int, enable: bool) -> None:
        self.write(f"OUTP {int(enable)},(@{ch})")
        return

    def set_output_current(self, ch: int, current: float) -> None:
        self.write(f"CURR {current:.3f},(@{ch})")
        return

    def set_output_voltage(self, ch: int, voltage: float) -> None:
        self.write(f"VOLT {voltage:.3f},(@{ch})")
        return

    def measure_current(self, ch: int) -> float:
        return float(self.query(f"MEAS:CURR?,(@{ch})"))

    def measure_voltage(self, ch: int) -> float:
        return float(self.query(f"MEAS:VOLT?,(@{ch})"))
