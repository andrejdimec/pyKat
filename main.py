import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtGui import Qt
from PySide6.QtCore import Slot


import vars
from ui_form import Ui_MainWindow
from logger import Logger
from comm import Comm

from aglo_hs import AgloHs
from om_v_arcgis import OmArcgis
from prenesi_hs import HsArcgis
from brisi_hs_izven import BrisiHs
from prebivalci_v_hs import PrebivalciHs
from hsmid_v_crp import HsmidCrp


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.comm = Comm()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.comm.signalText[str, Qt.GlobalColor].connect(self.izpis_v_text_box)

        # odzivi na klike
        self.ui.btn_konec.clicked.connect(konec)
        self.ui.btn_om_arcgis_table.clicked.connect(self.odjemna_arcgis)
        self.ui.btn_prenesi_hs.clicked.connect(self.prenesi_hs)
        # self.ui.btn_porocilo_voda.clicked.connect(self.porocilo_voda)
        self.ui.btn_hs_aglo.clicked.connect(self.aglo_hs)
        self.ui.btn_brisi_hs.clicked.connect(self.brisi_hs)
        self.ui.btn_preb.clicked.connect(self.vpisi_prebivalce)
        self.ui.btn_hsmid_crp.clicked.connect(self.dodaj_hsmid)

        # Logger
        self.logWindow = self.ui.textEdit
        self.logger = Logger(comm=self.comm)

        self.aglohs = AgloHs(comm=self.comm)
        self.omarcgis = OmArcgis(comm=self.comm)
        self.hsarcgis = HsArcgis(comm=self.comm)
        self.brisihs = BrisiHs(comm=self.comm)
        self.prebivalcihs = PrebivalciHs(comm=self.comm)
        self.hsmidcrp = HsmidCrp(comm=self.comm)

        self.ui.label_wks.setText("Workspace: " + str(vars.wkspace))

        # self.napolni_om_fc()
        # self.odjemna_arcgis()
        # self.prenesi_hs()
        # self.brisi_hs()
        # self.dodaj_hsmid()

    def vpisi_prebivalce(self):
        # print("vpisi_prebivalce")
        self.prebivalcihs.prebivalci_hs()

    def dodaj_hsmid(self):
        # V Crp Excel dodaj polji za Hsmid
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("Excel datoteke (*.xls, *.xlsx")
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        dialog.setDirectory("d:/podatki/")
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            if filename:
                #
                # filename = "d:/podatki/crp-01-07-2024.xlsx"
                self.hsmidcrp.hsmid_crp(filename)

    def prenesi_hs(self):
        msgBox = MsgBox(
            "Želiš prenesti nove hišne številke? Stare bodo zbrisane iz katastra", self
        )
        if msgBox.clickedButton() == msgBox.buttonY:
            self.hsarcgis.prenesi_hs()
        else:
            print("Izbrano ne")

        # print("prenesi_hs")

    def brisi_hs(self):
        msgBox = MsgBox("Želiš izbrisati odvečne hišne številke?", self)
        if msgBox.clickedButton() == msgBox.buttonY:
            self.brisihs.brisi_hs()
        else:
            print("Izbrano ne")

    def keyPressEvent(self, e):
        print("Keypress event", e)
        if e.key() == Qt.Key.Key_F10:
            konec()

    @Slot(str, Qt.GlobalColor)
    def izpis_v_text_box(self, text, col):
        self.logWindow.setTextColor(col)
        self.logWindow.append(text)
        self.logWindow.repaint()
        print("log:", text)

    def odjemna_arcgis(self):
        msgBox = MsgBox("Želiš prenesti nova odjemna mesta v kataster?", self)
        if msgBox.clickedButton() == msgBox.buttonY:
            self.omarcgis.napolni_om_fc()
        else:
            print("Izbrano ne")

    def aglo_hs(self):
        self.aglohs.agloVoda()
        # self.aglohs.agloKan()


class MsgBox(QMessageBox):
    def __init__(self, tekst, parent=None):
        super().__init__(parent)
        self.tekst = tekst

        self.setWindowTitle("Odloči.")
        self.setIcon(QMessageBox.Icon.Question)
        self.setText(tekst)
        self.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        self.buttonY = self.button(QMessageBox.StandardButton.Yes)
        self.buttonY.setText("Da")
        self.buttonN = self.button(QMessageBox.StandardButton.No)
        self.buttonN.setText("Ne")
        MsgBox.exec(self)
        # buttons = (
        #     QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No
        # )


def konec():
    app.exit()
    print("Konec.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    aglohs = AgloHs()
    widget.show()
    sys.exit(app.exec())
