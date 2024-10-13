from typing import Optional
from .gen2 import ShellyGen2


class ShellyGen3(ShellyGen2):
    """
    Implements a general Class for interaction with Shelly devices of generation 3
    """

    def __init__(self, ip: str, port: int = 80, timeout: int = 5,
                 login: Optional[dict[str, str]] = None, debug: bool = False, init: bool = False) -> None:

        super().__init__(ip=ip, port=port, timeout=timeout, login=login, debug=debug, init=init)
        self._generation: int = 3
