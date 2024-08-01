from halo import Halo

class Spinner:
    def __init__(self, message):
        self.spinner = Halo(text=message, spinner='dots')

    def start(self):
        self.spinner.start()

    def stop(self):
        self.spinner.stop()

    def succeed(self, message):
        self.spinner.succeed(message)

    def fail(self, message):
        self.spinner.fail(message)
        