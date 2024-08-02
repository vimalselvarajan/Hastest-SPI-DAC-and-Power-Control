from typing import Union, List

from instrument_lib.instrument_base import InstrumentBase


class KeysightDaq970a(InstrumentBase):

    def measure_voltage(self, ch: Union[int, str], v_range: Union[None, float] = None,
                        resolution: Union[None, float] = None) -> Union[float, List[float]]:
        command = "MEAS:VOLT:DC?"
        if v_range is not None:
            if resolution is not None:
                command = f"{command} {v_range},{resolution},(@{ch})"
            else:
                command = f"{command} {v_range},(@{ch})"
        else:
            command = f"{command} (@{ch})"

        response = self.query(command)
        if isinstance(ch, int):
            return float(response)
        else:
            values = response.split(',')
            return [float(value) for value in values]
