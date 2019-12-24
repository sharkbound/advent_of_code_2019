from collections import deque
from typing import Iterable, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from shared.intcode import IntCode


class IO:
    def __init__(self, initial: Iterable = (), log_output=True):
        if isinstance((queue := initial), (tuple, list)):
            queue = deque(initial)

        self.log_output = log_output
        self.queue: deque = queue

    def __bool__(self):
        return bool(self.queue)

    def on_output(self, value: int, c: Optional['IntCode'] = None):
        if self.log_output and c:
            print(f'#{c.id} outputted {value}')

    def on_input(self, value: int, c: Optional['IntCode'] = None, first=False, last=False):
        pass

    def peek(self):
        return self.queue[0]

    def peek_last(self):
        return self.queue[-1]

    def first(self, c: Optional['IntCode'] = None):
        value = self.queue.popleft()
        self.on_input(value, c, first=True)
        return value

    def last(self, c: Optional['IntCode'] = None):
        value = self.queue.pop()
        self.on_input(value, c, last=True)
        return value

    def append(self, value, c: Optional['IntCode'] = None):
        self.queue.append(value)

    def append_left(self, value, c: Optional['IntCode'] = None):
        self.queue.appendleft(value)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.queue}>'


class MaxIO(IO):
    def __init__(self, initial: Iterable = (), log_output=False):
        super().__init__(initial, log_output)
        self.max = 0

    def on_output(self, value: int, c: Optional['IntCode'] = None):
        self.append(value)
        self.max = max(self.max, value)


class LastIO(IO):
    def __init__(self, initial: Iterable = (), log_output=False):
        super().__init__(initial, log_output)
        self.value = 0

    def on_output(self, value: int, c: Optional['IntCode'] = None):
        self.value = value


class IOEventRelay(IO):
    others: List[IO]

    def __init__(self, initial: Iterable = (), *others: IO, log_output=False):
        super().__init__(initial, log_output)

        self.others = list(others)

    def on_output(self, value: int, c: Optional['IntCode'] = None):
        super().on_output(value, c)
        for other in self.others:
            other.on_output(value, c)

    def on_input(self, value: int, c: Optional['IntCode'] = None, first=False, last=False):
        super().on_input(value, c, first, last)
        for other in self.others:
            other.on_input(value, c, first, last)
