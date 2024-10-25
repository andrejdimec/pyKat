import sys
import os
import winsound

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import Slot, Qt, QThread

import vars
from ui_form import Ui_MainWindow
from logger import Logger
from comm import Comm
from aglo_hs import AgloHs
from om_v_arcgis import OmArcgisWorker
from prenesi_hs import HsArcgis
from brisi_hs_izven import BrisiHs
from prebivalci_v_hs import PrebivalciHs
from hsmid_v_crp_worker import HsmidCrpWorker
from posodobi_kanalizacijo import PosodobiKanalizacijo
from uvozi_infotim_vodomere import UvoziInfotim


def play_sound():
    # Play the Windows system confirmation sound
    winsound.MessageBeep(winsound.MB_OK)


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
        self.ui.btn_hs_aglo.clicked.connect(self.aglo_hs)
        self.ui.btn_brisi_hs.clicked.connect(self.brisi_hs)
        self.ui.btn_preb.clicked.connect(self.vpisi_prebivalce)
        self.ui.btn_hsmid_crp.clicked.connect(self.dodaj_hsmid)
        self.ui.btn_posodobi_kanal.clicked.connect(self.posodobi_kanalizacijo)
        self.ui.btn_infotim.clicked.connect(self.uvozi_vodomere)
        self.ui.btn_porocilo_voda.clicked.connect(self.porocilo_voda)

        # Progress bar in števec
        self.progress_bar = self.ui.progress_bar
        self.progress_label = self.ui.progress_label

        # Logger
        self.logWindow = self.ui.textEdit
        self.logger = Logger(comm=self.comm)

        self.aglohs = AgloHs(comm=self.comm)
        self.hsarcgis = HsArcgis(comm=self.comm)
        self.brisihs = BrisiHs(comm=self.comm)
        self.prebivalcihs = PrebivalciHs(comm=self.comm)
        self.hsmidcrp_worker = HsmidCrpWorker(comm=self.comm)
        self.omarcgis_worker = OmArcgisWorker(comm=self.comm)
        self.prenesihs_worker = HsArcgis(comm=self.comm)
        self.posodobi_kan = PosodobiKanalizacijo(comm=self.comm)
        self.uvozi_infotim_worker = UvoziInfotim(comm=self.comm)

        self.ui.label_wks.setText("Workspace: " + str(vars.wkspace))
        self.progress_label.setText("")
        self.progress_bar.setVisible(False)

        self.wpk = None

        # self.napolni_om_fc()
        # self.odjemna_arcgis()
        # self.prenesi_hs()
        # self.brisi_hs()
        # self.dodaj_hsmid()
        # self.posodobi_kanalizacijo()
        # self.uvozi_vodomere()
        self.vpisi_prebivalce()

    def test(self):
        pass

    def posodobi_kanalizacijo(self):
        if self.wpk is None:
            self.wpk = PosodobiKanalizacijo()
        self.wpk.exec()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.progress_bar.repaint()

    def update_status(self, message):
        self.progress_label.setText(message)
        self.progress_label.repaint()

    def vpisi_prebivalce(self):
        # print("vpisi_prebivalce")
        self.prebivalcihs.prebivalci_hs()
        exit(1)

    def is_file_open(self, file_path):
        # Preveri, če je Excel datoteka že odprta
        try:
            os.rename(file_path, file_path)
            return False
        except:
            return True

    def porocilo_voda(self):
        pass

    def odjemna_arcgis(self):
        # Prenesi odjemna mesti iz bass v kataster
        msgBox = MsgBoxYesNo("Želiš prenesti nova odjemna mesta v kataster?", self)
        if msgBox.clickedButton() == msgBox.buttonY:
            self.progress_bar.setVisible(True)
            self.thread = QThread()
            self.worker = self.omarcgis_worker
            self.worker.moveToThread(self.thread)

            self.worker.progress.connect(self.update_progress)
            # self.worker.status.connect(self.update_status)
            self.thread.started.connect(self.worker.napolni_om_fc())
            # self.worker.status.connect(lambda: self.thread.quit())
            self.thread.start()
            play_sound()

            # self.omarcgis_worker.napolni_om_fc()
        else:
            print("Izbrano ne")

    def uvozi_vodomere(self):
        # Uvozi vodomere iz excel izvožen iz infotim portala
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("Excel datoteke (*.xls, *.xlsx")
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        dialog.setDirectory("d:/podatki/")
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            if filename:
                if not self.is_file_open(filename):
                    self.progress_bar.setVisible(True)
                    self.thread = QThread()
                    self.worker = self.uvozi_infotim_worker
                    self.worker.moveToThread(self.thread)

                    self.worker.progress.connect(self.update_progress)
                    self.worker.status.connect(self.update_status)
                    self.thread.started.connect(self.worker.uvoz(filename))
                    self.worker.status.connect(lambda: self.thread.quit())
                    self.thread.start()
                    play_sound()
                else:
                    MsgBox("Najprej zapri datoteko " + filename)

    def dodaj_hsmid(self):
        # V Crp Excel dodaj polji za Hsmid in EIDHS
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("Excel datoteke (*.xls, *.xlsx")
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        dialog.setDirectory("d:/podatki/")
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            if filename:
                if not self.is_file_open(filename):
                    self.progress_bar.setVisible(True)
                    self.thread = QThread()
                    self.worker = self.hsmidcrp_worker
                    self.worker.moveToThread(self.thread)

                    self.worker.progress.connect(self.update_progress)
                    self.worker.status.connect(self.update_status)
                    self.thread.started.connect(self.worker.hsmid_crp(filename))
                    self.worker.status.connect(lambda: self.thread.quit())
                    self.thread.start()
                    play_sound()
                else:
                    MsgBox("Najprej zapri datoteko " + filename)
                #
                # filename = "d:/podatki/crp-01-07-2024.xlsx"
                # self.hsmidcrp.hsmid_crp(filename)

    def prenesi_hs(self):
        # Prenesi hišne številke s portala Geoservis
        msgBox = MsgBoxYesNo(
            "Želiš prenesti nove hišne številke? Stare bodo zbrisane iz katastra", self
        )
        if msgBox.clickedButton() == msgBox.buttonY:
            self.progress_bar.setVisible(True)
            self.thread = QThread()
            self.worker = self.prenesihs_worker
            self.worker.moveToThread(self.thread)

            self.worker.progress.connect(self.update_progress)
            self.worker.status.connect(self.update_status)
            self.thread.started.connect(self.worker.prenesi_hs())
            self.worker.status.connect(lambda: self.thread.quit())
            self.thread.start()
            play_sound()

            # self.hsarcgis.prenesi_hs()
        else:
            print("Izbrano ne")

        # print("prenesi_hs")

    def brisi_hs(self):
        # Briši hišne številke, ki niso v štirih občinah
        msgBox = MsgBoxYesNo("Želiš izbrisati odvečne hišne številke?", self)
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

    def aglo_hs(self):
        self.aglohs.agloVoda()
        # self.aglohs.agloKan()


class MsgBoxYesNo(QMessageBox):
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
        MsgBoxYesNo.exec(self)
        # buttons = (
        #     QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No
        # )


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


def konec():
    app.exit()
    print("Konec.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    aglohs = AgloHs()
    widget.show()
    sys.exit(app.exec())
