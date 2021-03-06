from ..helpers import serializable
from threading import Thread
import time


class container_wrapper(serializable.Serializable):
    def __init__(self, image, tag="latest", name=None, restart=True):
        self.image = image
        self.tag = tag
        self.name = name
        self.container = None
        self.running = False
        self.restart = restart
        self.func = None
        self.funcThread = None
        self.heartbeatThread = None
        self.heartbeatRhythm = None
        self.killed = False
        self.launched = False
        self.removed = False

    def heartbeat(self, func=None):

        while self.running and not self.killed:
            if func:
                self.funcThread = Thread(target=func)
                self.funcThread.start()
            self.running = self.get_status() == "running"
            time.sleep(self.heartbeatRhythm)

        if self.restart and not self.killed:
            print("restarting")
            self.run(self.client, self.func, self.heartbeatRhythm)

    def stop(self):
        self.running = False
        self.killed = True
        if self.funcThread:
            self.funcThread.join()
        self.container.stop()

    def kill(self):
        if self.running:
            self.running = False
            self.killed = True
            self.remove(True)

    def remove(self, force_removal=False):
        if not self.removed:
            self.removed = True
            self.container.remove(force=force_removal)

    def run(self, client, func=None, heartbeatRhythm=30):
        if not self.running:
            self.launched = True
            self.func = func
            self.heartbeatRhythm = heartbeatRhythm
            self.client = client
            self.container = self.client.containers.run(
                self.image, detach=True, name=self.name
            )
            self.running = True
            self.heartbeatThread = Thread(target=self.heartbeat, args=[func])
            self.heartbeatThread.start()
        else:
            # TODO: throw exception if all ready running
            pass

    def get_status(self, reload=True):
        if self.removed:
            return "removed"

        if self.killed:
            return "stopped"

        if self.launched:
            if reload:
                self.container.reload()
            return self.container.status

        return "not started"

    def serialize(self):
        return {
            "image": self.image,
            "tag": self.tag,
            "name": self.name,
            "status": self.get_status(),
            "restart_on_failure": self.restart,
        }
