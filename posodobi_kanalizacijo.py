import arcpy
from arcgis.gis import GIS
import os

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
        self.btn_posodobi.clicked.connect(self.posodobi)

        # self.posodobi_worker()

    def posodobi(self):
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
        web_folder = "_Dev"

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

        def overwrite_web_layer(source_layer):
            # create sharing draft
            sharing_draft = map_obj.getWebLayerSharingDraft(
                "HOSTING_SERVER", "FEATURE", source_layer.name
            )
            sharing_draft.overwriteExistingService = True
            sharing_draft.portalFolder = web_folder

            # stage and upload service definitions
            sd_filename = f"{source_layer.name}.sd"
            sd_output = arcpy.server.StageService(sharing_draft, sd_filename)
            arcpy.server.UploadServiceDefinition(sd_output, portal)

            print(f"Sucsessfully overwritten {source_layer.name}")

        overwrite_web_layer(source_layer_1_obj)
        overwrite_web_layer(source_layer_2_obj)

        print("Končano...")

        # # Set temp staging files
        # temp_path = vars.aprx_path
        # sddraft = os.path.join(temp_path, "temp_file.sddraft")
        # sd = os.path.join(temp_path, "temp_file.sd")
        #
        # # Assign environment, project and dictionaries
        # arcpy.env.overwriteOutput = True
        # prj = arcpy.mp.ArcGISProject(prj_path)
        map_dict = {}
        server_dict = {}

        # source_map = prj.listMaps(source_map_name)[0]
        # source_layer = source_map.listLayers
        # source_layer = source_map.listLayers(source_layer_name)[0]
        # print(source_layer)


def konec():
    print("Konec.")
