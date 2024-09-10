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

# Layerji, ki se prenašajo
dir_glavni = "Kanalizacija"
dir_linije = "Kanalizacijske linije"
dir_jaski = "Kanalizacijski jaški"
file_linije = "Kanalizacijska linija"
file_jaski = "Kanalizacijski jašek"
file_iztok = "Izpus"
file_lovilec_olj = "Lovilec olj"
file_greznice = "Greznice"
file_objekt = "Kanalizacijski objekt"
file_crpalisce = "Črpališče"
file_kcn = "Čistilna naprava"

project_path = vars.aprx_path
map_name = vars.map_name
aprx_name = vars.aprx_name

portal_url = vars.ago_url
username = vars.ago_username
password = vars.ago_password

layer_izbran = []
layer_ok = []  # Končni izbor po preverjanju


class PosodobiKanalizacijo(QDialog):
    def __init__(self, comm=Comm()):
        super().__init__()
        self.ui = Ui_frmPosodobiKan()
        self.ui.setupUi(self)
        self.dialog = Ui_frmPosodobiKan()
        self.comm = comm
        self.logger = Logger(comm=self.comm)
        self.logWindow = self.ui.te2
        self.cb_linije = self.ui.cb_linije
        self.cb_jaski = self.ui.cb_jaski
        self.cb_iztok = self.ui.cb_iztok
        self.cb_lovilec = self.ui.cb_lovilec
        self.cb_kcn = self.ui.cb_kcn
        self.cb_greznice = self.ui.cb_greznica
        self.cb_objekt = self.ui.cb_objekt
        self.cb_crpalisce = self.ui.cb_crpalisce

        # Buttons
        self.btn_cancel = self.ui.btn_cancel
        self.btn_cancel.clicked.connect(konec)
        self.comm.signalText[str, Qt.GlobalColor].connect(self.izpis_v_text_box)
        self.btn_posodobi = self.ui.btn_posodobi
        self.btn_posodobi.clicked.connect(self.posodobi)

        # Init
        self.zacetek()

        # Combobox
        self.cb_jaski.stateChanged.connect(self.doloci_layerje)
        self.cb_linije.stateChanged.connect(self.doloci_layerje)
        self.cb_iztok.stateChanged.connect(self.doloci_layerje)
        self.cb_kcn.stateChanged.connect(self.doloci_layerje)
        self.cb_objekt.stateChanged.connect(self.doloci_layerje)
        self.cb_greznice.stateChanged.connect(self.doloci_layerje)
        self.cb_lovilec.stateChanged.connect(self.doloci_layerje)
        self.cb_crpalisce.stateChanged.connect(self.doloci_layerje)

        self.doloci_layerje()
        # self.posodobi_worker()

    # Glavna rutina
    def posodobi(self):
        dalje = True
        start_time = time.time()

        # Prijavi se na AGOL
        self.presledek()
        self.log("Prijavljam se v ArcGIS Online...")
        try:
            arcpy.SignInToPortal(portal_url, username, password)
            gis = GIS(portal_url, username, password)
            self.logc("Prijava uspešna", green)

        except Exception as e:
            self.logc("Napaka pri prijavi " + str(e), err)
            dalje = False

        if dalje:
            self.presledek()
            for layer_pro in layer_ok:
                self.logc("Posodabljam layer " + layer_pro, black)
                search_result = gis.content.search(
                    query=layer_pro, item_type="Feature Layer"
                )
                if search_result:
                    self.logc(f"Layer že obstaja -> posodabljam.", green)
                else:
                    self.logc(f"Layer še ne obstaja -> dodajam.", red)

        # Konec
        self.presledek()
        minutes, seconds = stop(start_time)
        self.logc(f"Končano v {minutes} min {seconds} sek.", blue)
        if dalje:
            self.logc("Uspešno.", green)
        else:
            self.logc("Neuspešno.", err)
        self.presledek()
        # msgbox = MsgBox("Končano")

    def doloci_layerje(self):
        self.logWindow.clear()
        project = os.path.join(project_path, aprx_name)
        self.log(f"ArcGIS Pro projekt: {aprx_name}")
        aprx = arcpy.mp.ArcGISProject(project)
        self.log(f"Aktualna mapa: {map_name}")
        mymap = aprx.listMaps(map_name)[0]

        layer_izbran.clear()

        if self.cb_linije.isChecked():
            layer_izbran.append(os.path.join(file_linije))
        if self.cb_jaski.isChecked():
            layer_izbran.append(os.path.join(file_jaski))
        if self.cb_iztok.isChecked():
            layer_izbran.append(os.path.join(file_iztok))
        if self.cb_lovilec.isChecked():
            layer_izbran.append(os.path.join(file_lovilec_olj))
        if self.cb_kcn.isChecked():
            layer_izbran.append(os.path.join(file_kcn))
        if self.cb_crpalisce.isChecked():
            layer_izbran.append(os.path.join(file_crpalisce))
        if self.cb_greznice.isChecked():
            layer_izbran.append(os.path.join(file_greznice))
        if self.cb_objekt.isChecked():
            layer_izbran.append(os.path.join(file_objekt))
        # layer_izbran.append("jašek razno 11")
        # self.log(layer)

        # Preveri obstoj layerjev v Arcgis Pro

        self.presledek()
        self.log(f"Preverjam layerje, če obstajajo v ArcGis Pro...")
        layer_ok.clear()
        for layer_name in layer_izbran:
            print(": " + layer_name)
            odstrani_layer = ""
            layer = None
            for lyr in mymap.listLayers():
                if lyr.name == layer_name:
                    layer = lyr
                    self.logc(f"Layer '{layer_name}' obstaja.", green)
                    layer_ok.append(layer_name)
                    break

            if not layer:
                pass
                self.logc(f"Layer '{layer_name}' ne obstaja in ne bo posodobljen.", err)
                # layer_izbran.remove(layer_name)
                # print("remove: " + layer_name)
                # sys.exit(1)

        for lyr in layer_ok:
            self.log("ok: " + lyr)

    def zacetek(self):
        self.cb_jaski.setChecked(False)
        self.cb_iztok.setChecked(False)
        self.cb_linije.setChecked(False)
        self.cb_kcn.setChecked(False)
        self.cb_greznice.setChecked(True)
        self.cb_objekt.setChecked(False)
        self.cb_crpalisce.setChecked(False)
        self.cb_lovilec.setChecked(False)

    def preveri_obstoj(self):
        # Preveri če layerji obstajajo na online in če so ista imena v Arcgis pro in če bodo overwriten
        self.doloci_layerje()

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
