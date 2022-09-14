from threading import Semaphore
from typing import Any

class RingBuffer():
    def __init__(self, capacity: int = 10, overlap: bool = False) -> None:
        self._max_items = capacity
        self._overlap = overlap

        # Initial data
        self._buffer = [None] * self._max_items
        self._size = 0
        self._head = 0
        self._tail = -1 # Staggered initial value for proper pointing

        # Thread safety
        self.__buffer_sem = Semaphore() # Used for operations involving buffer
        self.__meta_sem = Semaphore() # Used for meta properties

    def _get_next_value(self, value: int) -> int:
        """ TODO """
        return (value + 1) % self._max_items

    def _move_head(self):
        """ TODO """
        self._head = self._get_next_value(self._head)

    def _move_tail(self):
        """ TODO """
        self._tail = self._get_next_value(self._tail)

    def _put(self, item: Any):
        """ TODO """
        if self.is_full():
            if not self._overlap:
                raise AttributeError("Cannot place item. Buffer is full.")

            # Replace oldest item to allow for new
            self._get()

        # Add the item
        self._buffer[self._head] = item
        self._size += 1

        # Move head to new position
        self._move_head()

    def _get(self) -> Any:
        """ TODO """
        if self.is_empty():
            raise AttributeError("Cannot retrieve item. Buffer is empty.")
        
        # Move tail to new position
        self._move_tail()

        # Retrieve oldest item
        item = self._buffer[self._tail]

        # Remove old item
        self._buffer[self._tail] = None
        self._size -= 1

        return item

    def put(self, item: Any):
        """ TODO """
        with self.__buffer_sem:
            self._put(item)

    def get(self) -> Any:
        """ TODO """
        with self.__buffer_sem:
            item = self._get()
            return item

    def peek(self) -> Any:
        """ TODO """
        with self.__buffer_sem:
            if self.is_empty():
                raise AttributeError("Cannot retrieve item. Buffer is empty.")
            
            item = self._buffer[self._get_next_value(self._tail)]
            return item

    def get_capacity(self):
        """ TODO """
        return self._max_items

    def get_size(self):
        """ TODO """
        with self.__meta_sem:
            size = self._size
            return size

    def is_empty(self):
        """ TODO """
        return self.get_size() == 0

    def is_full(self):
        """ TODO """
        return self.get_size() == self.get_capacity()

    def __str__(self) -> str:
        with self.__meta_sem:
            result =  f"Head: {self._head} Tail: {self._tail}\nData: {self._buffer}"

            return result




