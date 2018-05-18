class EventHook(object):
    """
    Simple event class used to provide hooks for different types of events in Locust.

    Here's how to use the EventHook class::

        my_event = EventHook()
        def on_my_event(a, b, **kw):
            print "Event was fired with arguments: %s, %s" % (a, b)
        my_event += on_my_event
        my_event.fire(a="foo", b="bar")
    """

    def __init__(self):
        self._handlers = []

    def __iadd__(self, handler):
        self._handlers.append(handler)
        return self

    def __isub__(self, handler):
        self._handlers.remove(handler)
        return self

    def fire(self, *args, **kwargs):
        for handler in self._handlers:
            handler(*args, **kwargs)

runner_data_refresh = EventHook()
make_data_done = EventHook()
make_slave_queue = EventHook()
slave_be_ready = EventHook()
slave_data_done = EventHook()
slave_report = EventHook()
receive_master_data = EventHook()
reset_slave = EventHook()
report_to_master = EventHook()
slave_stopping = EventHook()
#collected system metrics to master eg: cpu mem etc..
system_metrics_report = EventHook()