from threading import Thread
import time


class container_wrapper:
    def __init__(self, image, tag="latest", name=None, restart=True):
        self.image = image
        self.tag = tag
        self.container = None
        self.running = False
        self.restart = restart
        self.func = None
        self.funcThread = None
        self.heartbeatThread = None
        self.killed = False

    def heartbeat(self, func=None):
        while self.running:
            if func:
                self.func = func
                self.funcThread = Thread(target=func)
                self.funcThread.start()
            self.running = self.get_status() == "running"
            time.sleep(30)

        if self.restart and not self.killed:
            self.run(self.client, self.func)

    def kill(self):
        self.running = False
        self.killed = True
        if self.funcThread:
            self.funcThread.join()
        self.heartbeatThread.join()
        self.container.stop()

    def run(self, client, func=None):
        if not self.running:
            self.client = client
            self.container = self.client.containers.run(self.image, detach=True)
            self.running = True
            self.heartbeatThread = Thread(target=self.heartbeat, args=[func])
            self.heartbeatThread.start()
        else:
            # TODO: throw exception if all ready running
            pass

    def get_status(self, reload=True):
        if reload:
            self.container.reload()
        return self.container.status
