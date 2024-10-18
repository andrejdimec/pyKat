import arcpy
from arcpy import env
import os
from pathlib import Path
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QMessageBox

from openpyxl import load_workbook
import csv

import vars
import time
from logger import Logger
from comm import Comm
import pandas as pd


# import geopandas

black = vars.black
red = vars.darkRed
green = vars.darkGreen
blue = vars.darkBlue
err = vars.red

hs_fc = r"RPE\hisne_stevilke"
na_fc = r"RPE\NA_2024"
ul_fc = r"RPE\UL_2024"


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


class UvoziInfotim(Comm):
    progress = Signal(int)
    status = Signal(str)

    def __init__(self, comm=Comm()):
        super(UvoziInfotim, self).__init__()
        self.comm = comm
        self.logger = Logger(comm=self.comm)

    def uvoz(self, filename):
        # filename = "d:/podatki/test.xlsx"
        self.logc(f"Uvoz števcev Infotim iz {filename}", green)
        self.presledek()
        env.workspace = vars.wkspace
        vodomer_fc = r"Vodovod\vodomeri_infotim"
        start_time = time.time()

        if arcpy.TestSchemaLock(vodomer_fc):
            self.log(f"Arcgis ciljna datoteka: {vodomer_fc}")

            wrk_dir = os.path.dirname(filename)
            input_excel = filename
            temp_table = "temp_table"
            temp_layer = "temp_layer"
            temp_projected_layer = "temp_projected_layer"
            temp_excel = wrk_dir + "/tmp_infotim.xlsx"

            crs_source = arcpy.SpatialReference(4326)  # WGS_1984
            crs_destination = arcpy.SpatialReference(3794)  # Slovenia_1996

            self.log("Brisanje starih temp datotek")
            brisi_temp(temp_table, temp_layer, temp_projected_layer)

            # Zbriši in preimenuj excel tabele
            fields_to_delete = [
                "Obdobje",
                "Naprava",
                "Slika zahtevana",
                "Lokacija zahtevana",
                "GPS Lat nov",
                "GPS Lon nov",
                "Datum Pred. popisa",
                "Pred. popis",
                "Povprečje",
                "Datum izvoza",
                "Uporabnik",
                "Opomba",
                "Datum popisa",
                "Popis",
                "Poraba",
            ]
            rename_mapping = {
                "Serijska številka": "serijska_stevilka",
                "GPS Lat": "GPS_Lat",
                "GPS Lon": "GPS_Lon",
            }
            df = pd.read_excel(
                input_excel, dtype={"Koda OM": object, "RF Naslov": object}
            )
            self.log(f"Število vodomerov za prenos: {len(df)}")
            self.log(f"Brisanje odvečnih kolon v {input_excel}")
            df.drop(fields_to_delete, axis=1, inplace=True)
            df.rename(columns=rename_mapping, inplace=True)
            pd_writer = pd.ExcelWriter(temp_excel)
            df.to_excel(pd_writer, sheet_name="Sheet", index=False)
            pd_writer._save()

            self.log("Uvoz Excel datoteke v temp")
            arcpy.ExcelToTable_conversion(temp_excel, temp_table)

            self.log("Zapisovanje vodomerov v ArcGIS Pro")

            arcpy.management.XYTableToPoint(
                temp_table, temp_layer, "GPS_Lon", "GPS_Lat"
            )
            arcpy.management.Project(temp_layer, temp_projected_layer, crs_destination)
            self.izprazni_fc(vodomer_fc)
            arcpy.management.Append(temp_projected_layer, vodomer_fc, "NO_TEST")
            # brisi_temp(temp_table, temp_layer, temp_projected_layer)
        else:
            self.logc(f"Napaka: Datoteka {vodomer_fc} je zaklenjena", red)
        self.presledek()

        minutes, seconds = stop(start_time)
        self.logc(f"Končano v {minutes} min {seconds} sek.", blue)

    def izprazni_fc(self, fc):
        try:
            # self.log("Praznim datoteko " + str(fc))
            arcpy.management.DeleteRows(fc)
        except Exception as e:
            self.napaka(e)

    def napaka(self, e):
        self.presledek()
        self.logc("Napaka! " + str(e), err)

    def log(self, in_str):
        self.logger.izpisi(in_str, black)

    def logc(self, in_str, barva):
        self.logger.izpisi(in_str, barva)

    def presledek(self):
        self.log("\n")
