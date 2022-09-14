import time, unittest
from threading import Thread

from src.util.ring_buffer import RingBuffer

EXHAUSTIVE = False

class TestRingBuffer(unittest.TestCase):
    def setUp(self) -> None:
        self._buf = RingBuffer(capacity=10, overlap=True)

    def test_move_head_tail(self):
        """ Test _move_head and _move_tail methods """
        self._buf._move_head()
        self._buf._move_tail()
        self.assertEqual(self._buf._head, 1)
        self.assertEqual(self._buf._tail, 0)

        for _ in range (9):
            self._buf._move_head()
            self._buf._move_tail()
        self.assertEqual(self._buf._head, 0)
        self.assertEqual(self._buf._tail, 9)

        self._buf._move_tail()
        self.assertEqual(self._buf._tail, 0)

    def test_get_size(self):
        """ Test get_size method """
        self.assertEqual(self._buf.get_size(), 0)

        for _ in range(10):
            self._buf.put(1)

        self.assertEqual(self._buf.get_size(), 10)

    def test_is_empty(self):
        """ Test is_empty method """
        self.assertTrue(self._buf.is_empty())

        self._buf.put(1)
        self.assertFalse(self._buf.is_empty())
        
        self._buf.get()
        self.assertTrue(self._buf.is_empty())

    def test_is_full(self):
        """ Test is_empty method """
        self.assertFalse(self._buf.is_full())

        for i in range(10):
            self._buf.put(i)
        self.assertTrue(self._buf.is_full())
        
        self._buf.get()
        self.assertFalse(self._buf.is_full())

    def test_put_overlap(self):
        """ Test put method with overlap enabled """
        self._buf.put(1)
        self.assertEqual(self._buf.get_size(), 1)
        self._buf.get()

        for i in range(10):
            self._buf.put(i)
        self.assertEqual(self._buf.get_size(), 10)
        
        self._buf.put(1)
        self.assertEqual(self._buf.get_size(), 10)

    def test_put_no_overlap(self):
        """ Test put method with overlap disabled """
        buf = RingBuffer(capacity=10, overlap=False)
        buf.put(1)
        self.assertEqual(buf.get_size(), 1)

        for i in range(9):
            buf.put(i)

        self.assertRaises(AttributeError, buf.put, (1))

    def test_get(self):
        """ Test get method """
        self.assertRaises(AttributeError, self._buf.get)

        # Test getting '1' as '0' is overwritten by 10
        for i in range(11):
            self._buf.put(i)
        self.assertEqual(self._buf.get(), 1) 

        # Ensure count went down
        self.assertEqual(self._buf.get_size(), 9) 

    def test_peek(self):
        """ Test peek method """
        self.assertRaises(AttributeError, self._buf.peek)

        self._buf.put(1)

        self.assertEqual(self._buf.peek(), 1)
        self.assertEqual(self._buf.get_size(), 1)
        self.assertEqual(self._buf._tail, -1)

    def test_get_capacity(self):
        """ Test get_capacity method """
        self.assertEqual(self._buf.get_capacity(), 10)


if EXHAUSTIVE:
    class TestRingBufferThreaded:
        def setUp(self) -> None:
            self._buf = RingBuffer(capacity=10, overlap=True)

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
            value = self._buf.get()
            self.assertEqual(value, 0)
            producer.join()


if __name__ == "__main__":
    unittest.main()