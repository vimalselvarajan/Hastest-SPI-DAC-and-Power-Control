from .instrument_base import InstrumentBase

class KeysightE36312a(InstrumentBase):
    def enable_output(self, ch: int, enable: bool) -> None:
        self.write(f"OUTP {int(enable)},(@{ch})")

    def set_output_current(self, ch: int, current: float) -> None:
        self.write(f"CURR {current:.3f},(@{ch})")

    def set_output_voltage(self, ch: int, voltage: float) -> None:
        self.write(f"VOLT {voltage:.3f},(@{ch})")

    def measure_current(self, ch: int) -> float:
        return float(self.query(f"MEAS:CURR?,(@{ch})"))

    def measure_voltage(self, ch: int) -> float:
        return float(self.query(f"MEAS:VOLT?,(@{ch})"))

    def measure_voltage_no_channel(self) -> float:
        return float(self.query("MEAS:VOLT?"))

    def set_voltage_range(self, ch: int, range: float) -> None:
        self.write(f"SOUR:VOLT:RANG {range:.3f},(@{ch})")

    def get_voltage_range(self, ch: int) -> float:
        return float(self.query(f"SOUR:VOLT:RANG?,(@{ch})"))
