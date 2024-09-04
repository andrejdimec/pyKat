# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from ui_frm_posodobi_vodo import Ui_frmPosodobiv


class PosodobiVodo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_frmPosodobiv()
        self.ui.setupUi(self)

        self.btn_cancel = self.ui.btn_cancel
        self.btn_cancel.clicked.connect(self.close)

        self.btn_posodobi = self.ui.btn_posodobi
        self.btn_posodobi.clicked.connect(self.posodobi_worker)

    def posodobi_worker(self):
        pass
