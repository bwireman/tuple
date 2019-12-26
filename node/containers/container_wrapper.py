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
        self.heartbeatRhythm = None
        self.killed = False

    def heartbeat(self, func=None):
        while self.running and not self.killed:
            if func:
                self.funcThread = Thread(target=func)
                self.funcThread.start()
            self.running = self.get_status() == "running"
            time.sleep(self.heartbeatRhythm)

        if self.restart and not self.killed:
            self.run(self.client, self.func, self.heartbeatRhythm)

    def kill(self):
        self.running = False
        self.killed = True
        self.container.kill()

    def stop(self):
        self.running = False
        self.killed = True
        if self.funcThread:
            self.funcThread.join()
        self.container.stop()

    def run(self, client, func=None, heartbeatRhythm=30):
        if not self.running:
            self.func = func
            self.heartbeatRhythm = heartbeatRhythm
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
