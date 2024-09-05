import sys
import os
import winsound

import arcpy
from arcgis.gis import GIS
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog,
)
import openpyxl

# from PySide6.QtGui import Qt
from PySide6.QtCore import Slot, Qt, QThread, Signal


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
from hsmid_v_crp_worker import HsmidCrpWorker

from posodobi_kanalizacijo import PosodobiKanalizacijo


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
        self.ui.btn_test.clicked.connect(self.test)
        self.ui.btn_posodobi_kanal.clicked.connect(self.posodobi_kanalizacijo)

        self.progress_bar = self.ui.progress_bar
        self.progress_label = self.ui.progress_label

        # Logger
        self.logWindow = self.ui.textEdit
        self.logger = Logger(comm=self.comm)

        self.aglohs = AgloHs(comm=self.comm)
        self.omarcgis = OmArcgis(comm=self.comm)
        self.hsarcgis = HsArcgis(comm=self.comm)
        self.brisihs = BrisiHs(comm=self.comm)
        self.prebivalcihs = PrebivalciHs(comm=self.comm)
        self.hsmidcrp = HsmidCrp(comm=self.comm)
        self.hsmidcrp_worker = HsmidCrpWorker(comm=self.comm)

        self.ui.label_wks.setText("Workspace: " + str(vars.wkspace))

        self.progress_label.setText("")
        self.progress_bar.setVisible(False)

        self.wpk = None

        # self.napolni_om_fc()
        # self.odjemna_arcgis()
        # self.prenesi_hs()
        # self.brisi_hs()
        # self.dodaj_hsmid()
        self.posodobi_worker()

    def posodobi_worker(self):
        print("Posodobi kanalizacijo na AGO...")

        # Local paths
        map_name = vars.map_name
        group_layer_name = "Dev"
        prj_path = os.path.join(vars.aprx_path, vars.aktualna_karta)
        source_layer_1 = "Kanalizacijska linija"
        source_layer_2 = "Kanalizacijski jašek"
        print("Project", prj_path)

        # Set portal login
        portal = vars.ago_url
        ago_user = vars.ago_username
        ago_pass = vars.ago_password

        # Set sharing
        shrOrg = True
        shrEveryone = False
        shrGroups = ""

        # Connect to AGO
        print("Connecting to {}".format(portal))
        gis = GIS(portal, ago_user, ago_pass)
        print("Logged in as: " + gis.properties.user.username + "\n")

        aprx = arcpy.mp.ArcGISProject(prj_path)

        map_obj = aprx.listMaps(map_name)[0]
        group_layer = [
            layer
            for layer in map_obj.listLayers()
            if layer.isGroupLayer and layer.name == group_layer_name
        ][0]

        source_layer_1_obj = [
            layer for layer in group_layer.listLayers() if layer.name == source_layer_1
        ][0]
        source_layer_2_obj = [
            layer for layer in group_layer.listLayers() if layer.name == source_layer_2
        ][0]

        # Set temp staging files
        temp_path = vars.aprx_path
        sddraft = os.path.join(temp_path, "temp_file.sddraft")
        sd = os.path.join(temp_path, "temp_file.sd")

        # Assign environment, project and dictionaries
        arcpy.env.overwriteOutput = True
        prj = arcpy.mp.ArcGISProject(prj_path)
        map_dict = {}
        server_dict = {}

        # source_map = prj.listMaps(source_map_name)[0]
        # source_layer = source_map.listLayers
        # source_layer = source_map.listLayers(source_layer_name)[0]
        # print(source_layer)

    def overwrite_web_layer(self, source_layer):
        pass
        # create sharing draft
        # sharing_draft=map

    def test(self):
        pass

    def posodobi_kanalizacijo(self):
        if self.wpk is None:
            self.wpk = PosodobiKanalizacijo()
        self.wpk.exec()

    def play_sound(self):
        # Play the Windows system confirmation sound
        winsound.MessageBeep(winsound.MB_OK)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.progress_bar.repaint()

    def update_status(self, message):
        self.progress_label.setText(message)
        self.progress_label.repaint()

    def vpisi_prebivalce(self):
        # print("vpisi_prebivalce")
        self.prebivalcihs.prebivalci_hs()

    def is_file_open(self, file_path):
        # Preveri, če je Excel datoteka že odprta
        try:
            os.rename(file_path, file_path)
            return False
        except:
            return True

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
                    self.play_sound()
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
            self.hsarcgis.prenesi_hs()
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

    def odjemna_arcgis(self):
        # Prenesi odjemna mesti iz bass v kataster
        msgBox = MsgBoxYesNo("Želiš prenesti nova odjemna mesta v kataster?", self)
        if msgBox.clickedButton() == msgBox.buttonY:
            self.progress_bar.setVisible(True)
            self.thread = QThread()
            self.worker = self.hsmidcrp_worker
            self.worker.moveToThread(self.thread)

            self.worker.progress.connect(self.update_progress)
            self.worker.status.connect(self.update_status)
            self.thread.started.connect(self.worker.hsmid_crp(filename))
            self.worker.status.connect(lambda: self.thread.quit())
            self.thread.start()
            self.play_sound()

            self.omarcgis.napolni_om_fc()
        else:
            print("Izbrano ne")

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
