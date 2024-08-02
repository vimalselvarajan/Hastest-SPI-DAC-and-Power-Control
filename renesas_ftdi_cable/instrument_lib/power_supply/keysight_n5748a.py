from instrument_lib.instrument_base import InstrumentBase


class KeysightN5748a(InstrumentBase):
    # 80V, 9.5A
    def enable_output(self, enable: bool) -> None:
        self.write(f"OUTP {int(enable)})")
        return

    def set_output_current(self, current: float) -> None:
        self.write(f"CURR {current:.3f}")
        return

    def set_output_voltage(self, voltage: float) -> None:
        self.write(f"VOLT {voltage:.3f}")
        return

    def measure_current(self) -> float:
        return float(self.query(f"MEAS:CURR?"))

    def measure_voltage(self) -> float:
        return float(self.query(f"MEAS:VOLT?"))
