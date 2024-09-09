import sys

import arcpy
from arcgis.gis import GIS
import os

from PySide6 import QtCore
import vars
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Slot, Qt
from ui_frm_posodobi_kanalizacijo import Ui_frmPosodobiKan
from comm import Comm
from logger import Logger
import time

black = vars.black
red = vars.darkRed
green = vars.darkGreen
blue = vars.darkBlue
err = vars.red


class PosodobiKanalizacijo(QDialog):
    def __init__(self, comm=Comm()):
        super().__init__()
        self.ui = Ui_frmPosodobiKan()
        self.ui.setupUi(self)
        self.dialog = Ui_frmPosodobiKan()
        self.comm = comm
        self.logger = Logger(comm=self.comm)
        self.logWindow = self.ui.te2
        self.btn_cancel = self.ui.btn_cancel
        self.btn_cancel.clicked.connect(konec)
        self.comm.signalText[str, Qt.GlobalColor].connect(self.izpis_v_text_box)
        self.btn_posodobi = self.ui.btn_posodobi
        self.btn_posodobi.clicked.connect(self.posodobi)

        # self.posodobi_worker()

    def posodobi(self):
        start_time = time.time()
        self.logc("Prenesi kanalizacijo iz ArcGIS Pro", green)
        self.logc("v ArcGIS Online.", green)
        self.presledek()

        # Določi datoteke, ki se prenašajo
        dir_glavni = "Kanalizacija"
        dir_linije = "Kanalizacijske linije"
        file_linije = "Kanalizacijska linija"
        dir_jaski = "Kanalizacijski jaški"
        file_jaski = "Kanalizacijski jašek"
        file_iztok = "Izpust"
        minutes, seconds = stop(start_time)

        self.logc(f"Končano v {minutes} min {seconds} sek.", blue)
        # msgbox = MsgBox("Končano")

    @Slot(str, Qt.GlobalColor)
    def izpis_v_text_box(self, text, col):
        self.logWindow.setTextColor(col)
        self.logWindow.append(text)
        self.logWindow.repaint()
        print("log:", text)

    def log(self, in_str):
        self.logger.izpisi(in_str, black)

    def logc(self, in_str, barva):
        self.logger.izpisi(in_str, barva)

    def presledek(self):
        self.log("\n")


def stop(st):
    end_time = time.time()
    elapsed_time = end_time - st
    m = int(elapsed_time / 60)
    s = int(elapsed_time % 60)
    return m, s


def konec():
    print("Konec.")
    sys.exit()
    # self.close()
