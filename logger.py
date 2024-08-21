from comm import Comm


class Logger:
    def __init__(self, comm=Comm()):
        super(Logger, self).__init__()
        self.comm = comm

    def izpisi(self, t, barva):
        self.comm.signalText.emit(t, barva)
