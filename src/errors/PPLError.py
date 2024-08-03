from abc import ABC, abstractmethod

from ..parser import Position


class PPLError(ABC):

    @abstractmethod
    def set_position(self, position: Position) -> None: ...

    @abstractmethod
    def output(self) -> str: ...
