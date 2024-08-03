from typing import List
from abc import ABC, abstractmethod

from . import Expression

from bytecode import Instr


class Statement(ABC):
    @abstractmethod
    def optimize(self) -> 'Statement': ...

    @abstractmethod
    def compile(self) -> List[Instr]: ...

    @abstractmethod
    def check_error(self) -> Expression | None: ...

    @abstractmethod
    def output(self) -> str: ...
