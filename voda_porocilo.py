#
# TODO Poročilo vodovod
#
import arcpy

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QMessageBox
import vars
import time
from logger import Logger
from comm import Comm
import pandas as pd

black = vars.black
red = vars.darkRed
green = vars.darkGreen
blue = vars.darkBlue
err = vars.red


class MsgBox(QMessageBox):
    def __init__(self, tekst, parent=None):
        super().__init__(parent)
        self.tekst = tekst

        self.setWindowTitle("Sporočilo.")
        self.setIcon(QMessageBox.Icon.Information)
        self.setText(tekst)
        self.setStandardButtons(QMessageBox.StandardButton.Yes)
        self.buttonY = self.button(QMessageBox.StandardButton.Yes)
        self.buttonY.setText("V redu")
        MsgBox.exec(self)


def stop(st):
    end_time = time.time()
    elapsed_time = end_time - st
    m = int(elapsed_time / 60)
    s = int(elapsed_time % 60)
    return m, s


def brisi_temp(fc, lyr, prlyr):
    # če temp table že obstaja jo zbriši
    if arcpy.Exists(fc):
        arcpy.Delete_management(fc)
        print(f"Table {fc} has been deleted.")
    else:
        print(f"Table {fc} does not exist.")

    if arcpy.Exists(lyr):
        arcpy.Delete_management(lyr)
        print(f"Layer {lyr} has been deleted.")
    else:
        print(f"Layer {lyr} does not exist.")
    if arcpy.Exists(prlyr):
        arcpy.Delete_management(prlyr)
        print(f"Layer {prlyr} has been deleted.")
    else:
        print(f"Layer {prlyr} does not exist.")


class PorociloVoda(Comm):
    progress = Signal(int)
    status = Signal(str)

    def __init__(self, comm=Comm()):
        super(PorociloVoda, self).__init__()
        self.comm = comm
        self.logger = Logger(comm=self.comm)

    def napaka(self, e):
        self.presledek()
        self.logc("Napaka! " + str(e), err)

    def log(self, in_str):
        self.logger.izpisi(in_str, black)

    def logc(self, in_str, barva):
        self.logger.izpisi(in_str, barva)

    def presledek(self):
        self.log("\n")

    def pripravi_porocilo(self, filename):
        # filename = "d:/podatki/test.xlsx"
        self.logc(f"Priprava poročila o vodovodu", green)
        self.presledek()
        env.workspace = vars.wkspace
        vodomer_fc = r"Vodovod\vodomeri_infotim"
        start_time = time.time()
