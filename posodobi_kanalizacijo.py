import sys

import arcpy
from arcgis.gis import GIS
import os
import xml.dom.minidom as DOM
from PySide6 import QtCore
from sympy import false

import vars
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Slot, Qt

# from test9 import mymap
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
        self.log("Prijava v ArcGIS Online...")
        try:
            arcpy.SignInToPortal(portal_url, username, password)
            gis = GIS(portal_url, username, password)
            self.logc("Uspešno.", green)

        except Exception as e:
            self.logc("Napaka pri prijavi " + str(e), err)
            dalje = False

        if dalje:
            project = os.path.join(project_path, aprx_name)
            aprx = arcpy.mp.ArcGISProject(project)
            mymap = aprx.listMaps(map_name)[0]

            self.presledek()
            for layer_pro in layer_ok:
                layer = mymap.listLayers(layer_pro)[0]
                output_service_name = layer_pro
                # self.log("layer" + str(layer.name))
                self.logc("Posodabljam layer " + layer_pro, black)
                search_result = gis.content.search(
                    query=layer_pro, item_type="Feature Layer"
                )
                if search_result:
                    self.logc(f"Layer že obstaja -> posodabljam.", green)
                else:
                    self.logc(f"Layer še ne obstaja -> dodajam.", red)

                # Dejansko posodobi

                # preveri in naredi scratch folder
                scratch_folder = arcpy.env.scratchFolder
                if not scratch_folder:
                    scratch_folder = os.path.join(os.getcwd(), "scratch")
                    os.makedirs(scratch_folder, exist_ok=True)
                    arcpy.env.scratchFolder = scratch_folder

                # self.log(f"Scratch folder: {scratch_folder}")

                # Define paths for service definition draft and staged service
                sddraft_file = os.path.join(scratch_folder, f"{layer_pro}.sddraft")
                sd = os.path.join(scratch_folder, f"{layer_pro}.sd")
                thumb = os.path.join(scratch_folder, "Thumbnail.png")

                novi = True

                if novi:
                    self.log("Novi način sddraft")
                    # sharing draft - novi način
                    # Create FeatureSharingDraft and set metadata, portal folder, export data properties, and CIM symbols
                    server_type = "HOSTING_SERVER"
                    sddraft = mymap.getWebLayerSharingDraft(
                        server_type, "FEATURE", output_service_name
                    )
                    # sddraft = mymap.getWebLayerSharingDraft(
                    #     server_type, "FEATURE", output_service_name
                    # )
                    sddraft.credits = "These are credits"
                    sddraft.description = "This is description"
                    sddraft.summary = "This is summary"
                    sddraft.tags = "tag1, tag2"
                    sddraft.useLimitations = "These are use limitations"
                    sddraft.portalFolder = ""
                    sddraft.allowExporting = True
                    sddraft.useCIMSymbols = True

                    # Create Service Definition Draft file
                    sddraft.exportToSDDraft(sddraft_file)

                    # Read the .sddraft file
                    docs = DOM.parse(sddraft_file)
                    key_list = docs.getElementsByTagName("Key")
                    value_list = docs.getElementsByTagName("Value")

                    # Change following to "true" to share
                    SharetoOrganization = "false"
                    SharetoEveryone = "true"
                    SharetoGroup = "false"
                    # If SharetoGroup is set to "true", uncomment line below and provide group IDs
                    GroupID = ""  # GroupID = "f07fab920d71339cb7b1291e3059b7a8, e0fb8fff410b1d7bae1992700567f54a"

                    # Each key has a corresponding value. In all the cases, value of key_list[i] is value_list[i].
                    for i in range(key_list.length):
                        if key_list[i].firstChild.nodeValue == "PackageUnderMyOrg":
                            value_list[i].firstChild.nodeValue = SharetoOrganization
                        if key_list[i].firstChild.nodeValue == "PackageIsPublic":
                            value_list[i].firstChild.nodeValue = SharetoEveryone
                        if key_list[i].firstChild.nodeValue == "PackageShareGroups":
                            value_list[i].firstChild.nodeValue = SharetoGroup
                        if (
                            SharetoGroup == "true"
                            and key_list[i].firstChild.nodeValue == "PackageGroupIDs"
                        ):
                            value_list[i].firstChild.nodeValue = GroupID

                    # Write to the .sddraft file
                    f = open(sddraft_file, "w")
                    docs.writexml(f)
                    f.close()

                else:
                    # Create a service definition draft
                    self.presledek()
                    self.log(f"Creating service definition draft...")
                    arcpy.mp.CreateWebLayerSDDraft(
                        map_or_layers=layer,  # Input layer object
                        out_sddraft=sddraft,  # Output path for .sddraft file
                        service_name=output_service_name,  # Name of the web service to be published
                        service_type="HOSTING_SERVER",  # ArcGIS Online hosting server
                        server_type="MY_HOSTED_SERVICES",  # Service connection type for ArcGIS Online
                        folder_name="Kanalizacija",  # Folder on ArcGIS Online (empty means root folder)
                        overwrite_existing_service=True,  # Overwrite existing service with the same name
                        summary=f"Web layer of the '{layer_pro}' layer",  # Summary for the service
                        tags=f"arcpy, {layer_pro}, ArcGIS Online",  # Tags to describe the web layer
                        description=f"This web layer is created from the '{layer_pro}' layer in ArcGIS Pro",
                        # Detailed description
                    )

                self.log(f"Staging service definition...")
                try:
                    arcpy.StageService_server(sddraft_file, sd)
                    warnings = arcpy.GetMessages(1)
                    if warnings:
                        self.log(f"Warnings:")
                        for warning in warnings:
                            self.log(f"\t{warning}")
                except Exception as e:
                    dalje = False
                    self.logc("Staging error. - {}".format(str(e)), err)
                    self.brisi_temp(sddraft, sd, thumb)
                    # sys.exit("Napaka pri staging.")

                # if dalje:
                #     # Upload the staged service definition to ArcGIS Online
                #     self.log(f"Uploading '{layer_pro}'...")
                #     try:
                #         arcpy.UploadServiceDefinition_server(sd, "MY_HOSTED_SERVICES")
                #         self.logc(f"Layer '{layer_pro}' - uspešno posodobljen.", green)
                #
                #     except Exception as e:
                #         self.logc("Napaka pri upload - {}".format(str(e)), err)
                #         self.brisi_temp(sddraft, sd, thumb)
                #         dalje = False
                #         # sys.exit("Napaka pri upload.")

                # self.brisi_temp(sddraft, sd, thumb)
        # Konec
        # self.presledek()
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
            # print(": " + layer_name)
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

        # for lyr in layer_ok:
        #     self.log("ok: " + lyr)

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

    def brisi_temp(self, sddraft, sd, thumb):
        # Zbriši temp datoteke
        try:
            self.log("Brisanje začasnih datotek...")
            if os.path.exists(sddraft):
                os.remove(sddraft)
                # self.log(f"Deleted: {sddraft}")
            if os.path.exists(sd):
                os.remove(sd)
                # self.log(f"Deleted: {sd}")
            if os.path.exists(thumb):
                os.remove(thumb)
                # self.log(f"Deleted: {thumb}")
        except Exception as e:
            self.logc(f"Napaka pri brisanju temp datotek: {str(e)}", err)


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
