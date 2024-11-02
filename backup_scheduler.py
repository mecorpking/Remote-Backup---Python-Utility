from threading import Timer

class BackupScheduler:
    def __init__(self, interval, task):
        self.interval = interval
        self.task = task
        self.timer = None

    def start(self):
        self.timer = Timer(self.interval, self.run)
        self.timer.start()

    def run(self):
        self.task()
        self.start()

    def stop(self):
        if self.timer:
            self.timer.cancel() 