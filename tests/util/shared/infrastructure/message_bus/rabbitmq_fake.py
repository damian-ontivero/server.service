class RabbitMQFake:
    def __init__(self):
        self._queue = []

    def publish(self, message):
        self._queue.append(message)

    def consume(self):
        return self._queue.pop(0)

    def clear(self):
        self._queue.clear()

    def __len__(self):
        return len(self._queue)
