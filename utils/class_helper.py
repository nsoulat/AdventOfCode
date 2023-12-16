from abc import ABC
from itertools import count


class WithID(ABC):
    def __init__(self):
        self.identifier: int = count().__next__()

    def __hash__(self) -> int:
        return self.identifier
