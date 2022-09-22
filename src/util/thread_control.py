import threading

class ThreadCloser():
    """ Utility class to flag when a thread should/should not run. This is
    handled by two control variables. A thread can be flagged as active/inactive
    which is analagous to running/paused, or flagged as killed, which should 
    start the thread closing process. Kill should always supercede 
    active/inactive.
    """
    def __init__(self) -> None:
        self._active = True
        self._kill = False

    def set_active(self):
        """ Set an associated thread to be active """
        self._active = True

    def set_inactive(self):
        """ Set an associated thread to be inactive """
        self._active = False

    def kill(self):
        """ Flag an associated thread to end """
        self.set_inactive()
        self._kill = True

    def is_killed(self) -> bool:
        """ (bool) True if a thread should be closing. False otherwise. """
        return self._kill

    def is_active(self) -> bool:
        """ (bool) True if a thread should be active. False otherwise. """
        return self._active


class ThreadController():
    """ Utility class to store a thread and its associated thread closer. """
    def __init__(
        self, 
        thread: threading.Thread, 
        closer: ThreadCloser
    ) -> None:
        """ Initialise a thread controller object. Stores a thread and an 
        associated thread closer.
        
        Params:
            thread (Thread): The thread to store.
            closer (ThreadCloser): The closer associated with the given thread.
        """
        self._t = thread
        self._closer = closer

    @property
    def thread(self):
        """ (Thread) Returns the controller's thread object. """
        return self._t

    @property
    def t(self):
        """ (Thread) Returns the controller's thread object. """
        return self._t

    @property
    def closer(self):
        """ (ThreadCloser) Returns the controller's thread closer object. """
        return self._closer

    def get_thread(self) -> threading.Thread:
        """ (Thread) Returns the controller's thread object. """
        return self.thread

    def get_closer(self) -> ThreadCloser:
        """ (ThreadCloser) Returns the controller's thread closer object. """
        return self.closer

    def start(self) -> None:
        """ Start the controller's thread """
        self.t.start()

    def kill(self) -> None:
        """ Flag the controller's thread for closing """
        self.closer.kill()