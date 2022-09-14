import queue

class Closed(Exception):
    """ Exception raised by RingBuffer.put/get when RingBuffer closed. """
    pass

class NotifyBufferFinish():
    """ This class is a sentinel to inform buffer consumers to stop buffer 
    operations.
    """

class RingBuffer(queue.Queue):
    """ A FIFO Queue implementation that allows for cyclic value replacement. 
    """
    def __init__(self, capacity: int = 10, overlap: bool = True) -> None:
        """ Construct a RingBuffer instance.
        
        Params:
            capacity (int): The maximum number of items the buffer can hold. 
                Defaults to 0. capacity <= 0 means infinite.
            overlap (bool): Whether the buffer placement can wrap. When false,
                acts as a FIFO Queue. When true, acts as a ring buffer. Defaults
                to True.
        """
        super().__init__(maxsize=capacity)
        self._overlap = overlap
        self._closed = False

    def _close(self):
        """ Close the buffer so no more values can be placed/removed. """
        self._closed = True

    def put(self, item, block=True, timeout=None):
        """ Put an item onto the ring buffer.
        
        If the buffer allows overlap and is full, the oldest value in the buffer
        will be replaced. If the buffer does not allow overlap, acts like a FIFO
        queue.

        If the buffer is closed, raises Closed exception.            

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until a free slot is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Full exception if no free slot was available within that time.
        Otherwise ('block' is false), put an item on the queue if a free slot
        is immediately available, else raise the Full exception ('timeout'
        is ignored in that case).
        """
        if self._closed:
            raise Closed("The RingBuffer is closed. Cannot Put item")

        if self._overlap and self.full():
            self.get()

        super().put(item, block, timeout)
        
    def get(self, block=True, timeout=None):
        """ Remove and return an item from the queue.

        If the buffer is closed, raises Closed exception.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).
        """
        if self._closed:
            raise Closed("The RingBuffer is closed. Cannot Put item")
        return super().get(block, timeout)

    def capacity(self):
        return self.maxsize

    def notify_finish(self):
        """ Begin the process of notifying all consumers that the buffer should
        close.
        """
        self.put(NotifyBufferFinish())

    def confirm_sentinel(self, sentinel: NotifyBufferFinish) -> None:
        """ Used to acknowledge that a sentinel has been received. Will 
        propagate the sentinel to other consumers, unless the buffer is empty.
        If the buffer is empty, the buffer will be closed.
        """
        if self.empty():
            self._close()
        else:
            self.put(sentinel)
        