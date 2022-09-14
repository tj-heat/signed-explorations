import queue
import time, unittest
from threading import Thread

from src.util.ring_buffer import RingBuffer

EXHAUSTIVE = False

class TestRingBuffer(unittest.TestCase):
    def setUp(self) -> None:
        self._buf = RingBuffer(capacity=10, overlap=True)

    def test_put_overlap(self):
        """ Test put method with overlap enabled """
        self._buf.put(1)
        self.assertEqual(self._buf.qsize(), 1)
        self._buf.get()

        for i in range(10):
            self._buf.put(i)
        self.assertEqual(self._buf.qsize(), 10)
        
        self._buf.put(1)
        self.assertEqual(self._buf.qsize(), 10)

    def test_put_no_overlap(self):
        """ Test put method with overlap disabled """
        buf = RingBuffer(capacity=10, overlap=False)
        buf.put(1)
        self.assertEqual(buf.qsize(), 1)

        for i in range(9):
            buf.put(i)

        self.assertRaises(queue.Full, buf.put_nowait, (1,))

    def test_get(self):
        """ Test get method """
        # Test getting '1' as '0' is overwritten by 10
        for i in range(11):
            self._buf.put(i)
        self.assertEqual(self._buf.get(), 1) 

        # Ensure count went down
        self.assertEqual(self._buf.qsize(), 9) 

    if EXHAUSTIVE:
        def test_thread_safety(self):
            """ Test RingBuffer handles thread-safe read/write. """

            def buffer_produce_t(buffer: RingBuffer):
                """ Continuously adds to a ring buffer """
                for i in range(100):
                    buffer.put(i)
                    time.sleep(0.0001)

            producer = Thread(target=buffer_produce_t, args=(self._buf,))
            producer.start()
            
            # Attempt to read value from buffer
            time.sleep(0.01)
            self.assertEqual(self._buf.get(), 0)
            producer.join()


if __name__ == "__main__":
    unittest.main()