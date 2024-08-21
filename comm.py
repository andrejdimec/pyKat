from PySide6.QtCore import QObject, Signal, Qt


class Comm(QObject):
    signalText = Signal(str, Qt.GlobalColor)
