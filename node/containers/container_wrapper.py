from threading import Thread
import time


class container_wrapper:
    def __init__(self, image, tag):
        self.name = image
        self.tag = tag
        self.container = None
        self.running = False

    def heartbeat(self, func=None):
        while self.running:
            if func:
                Thread(target=func).start()
            self.running = self.get_status() == "running"
            time.sleep(30)

    def run(self, client, func=None):
        if not self.running:
            self.client = client
            self.container = self.client.containers.run(self.name, detach=True)
            self.running = True
            Thread(target=self.heartbeat, args=[func]).start()
        else:
            # TODO: throw exception if all ready running
            pass

    def get_status(self, reload=True):
        if reload:
            self.container.reload()
        return self.container.status
