import arcpy
from arcgis.gis import GIS


from PySide6 import QtCore
import vars
from PySide6.QtWidgets import QDialog
from ui_frm_posodobi_kanalizacijo import Ui_frmPosodobiKan


class PosodobiKanalizacijo(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_frmPosodobiKan()
        self.ui.setupUi(self)

        self.btn_cancel = self.ui.btn_cancel
        self.btn_cancel.clicked.connect(self.close)

        self.btn_posodobi = self.ui.btn_posodobi
        self.btn_posodobi.clicked.connect(self.posodobi_worker)

        self.posodobi_worker()

    def posodobi_worker(self):
        prj_path = vars.aktualna_karta
        print(prj_path)


def konec():
    print("Konec.")
