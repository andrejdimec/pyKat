# Izbriši hišne številke izven občin

import arcpy
from arcpy import env
import vars
import time
from logger import Logger
from comm import Comm

black = vars.black
red = vars.darkRed
green = vars.darkGreen
blue = vars.darkBlue
err = vars.red


def stop(st):
    end_time = time.time()
    elapsed_time = end_time - st
    m = int(elapsed_time / 60)
    s = int(elapsed_time % 60)
    return m, s


class BrisiHs(Comm):
    def __init__(self, comm=Comm()):
        super(BrisiHs, self).__init__()
        self.comm = comm
        self.logger = Logger(comm=self.comm)

    def brisi_hs(self):
        hs_fc = "RPE\hisne_stevilke"
        ob_fc = "RPE\OB"
        start_time = time.time()
        env.workspace = vars.wkspace
        starih_zapisov = arcpy.management.GetCount(hs_fc)
        self.logc(
            "Brisanje hišnih številk iz katastra, ki niso v občinah Gornja Radgona, Apače, Radenci",
            green,
        )
        self.presledek()
        self.log(f"Arcgis datoteka: {hs_fc}")
        self.presledek()
        start_time = time.time()

        # Izberi vse tri občine
        fc_selected = "obcina_selected"  # začasno zaradi brisanja
        # qry = f'"OB_MID"={vars.obcina_radgona} OR "OB_MID"={vars.obcina_apace} OR "OB_MID"={vars.obcina_radenci} OR "OB_MID"={vars.obcina_jurij}'
        qry = f'"OB_MID"={vars.obcina_radgona}'  # Samo radgona
        obcinaLayer = arcpy.MakeFeatureLayer_management(ob_fc, fc_selected)
        arcpy.SelectLayerByAttribute_management(obcinaLayer, "NEW_SELECTION", qry)
        cnt = arcpy.GetCount_management(obcinaLayer)
        print("The number of selected records is: " + str(cnt))

        # Izberi hišne številke, ki so izven izbranih občin

        hs_selected = "hs_selected"
        hslayer = arcpy.MakeFeatureLayer_management(hs_fc, hs_selected)
        arcpy.SelectLayerByLocation_management(
            hslayer,
            "COMPLETELY_WITHIN",
            obcinaLayer,
            invert_spatial_relationship="INVERT",
        )
        cnt_hs = arcpy.GetCount_management(hslayer)
        self.log(f"Izven občin je {cnt_hs} hišnih številk")

        # Zbriši izbrane hišne številke
        arcpy.DeleteFeatures_management(hslayer)
        novih_zapisov = arcpy.management.GetCount(hslayer)
        # Poročilo

        razlika = int(novih_zapisov[0]) - int(starih_zapisov[0])
        self.presledek()

        self.log(f"Prejšnje stanje: {starih_zapisov} hišnih številk.")
        self.log(f"Novo stanje: {novih_zapisov} hišnih številk.")
        self.log(f"Razlika: {razlika} hišnih številk.")
        self.presledek()
        minutes, seconds = stop(start_time)
        self.logc(f"Končano v {minutes} min {seconds} sek.", blue)

    def log(self, in_str):
        self.logger.izpisi(in_str, black)

    def logc(self, in_str, barva):
        self.logger.izpisi(in_str, barva)

    def presledek(self):
        self.log("\n")
