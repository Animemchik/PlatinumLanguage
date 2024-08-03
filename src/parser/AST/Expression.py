from typing import List
from abc import ABC, abstractmethod

from bytecode import Instr


class Expression(ABC):
    @abstractmethod
    def optimize(self) -> 'Expression': ...

    @abstractmethod
    def compile(self) -> List[Instr]: ...

    @abstractmethod
    def check_error(self) -> 'Expression': ...

    @abstractmethod
    def output(self) -> str: ...
