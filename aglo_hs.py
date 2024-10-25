import arcpy
from arcpy import env
import time
from logger import Logger
from comm import Comm
import vars

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


class AgloHs:
    env.workspace = vars.wkspace

    def __init__(self, comm=Comm()):
        super(AgloHs, self).__init__()
        self.comm = comm
        self.logger = Logger(comm=self.comm)

    def log(self, in_str, barva):
        self.logger.izpisi(in_str, barva)

    def agloVoda(self):
        start_time = time.time()
        self.log("V tabelo s hišnimi številkami vpiši prave aglomeracije", green)
        self.log("", black)
        self.log("Aglomeracije pitna voda", blue)

        self.log("", black)

        agloV = []
        fcAglo = r"Aglomeracije/aglo_voda_2022"
        fcHs = r"RPE/Hisne_stevilke"
        field = "aglov"
        hsFieldType = "LONG"
        createField = True
        if arcpy.TestSchemaLock(fcHs):
            # Preveri, če v hisne_stevilke obstaja field aglov (long), če ne ga naredi
            lstFields = arcpy.ListFields(fcHs)

            for row in lstFields:
                if row.name == field:
                    createField = False
                    self.log("Field exists -" + row.name, black)

            if createField:  # Create field aglov
                try:
                    print("Creating field ", field)
                    arcpy.management.AddField(fcHs, field, hsFieldType)
                except Exception as e:
                    print("Error: " + e.args[0])

            # Vsem zapisom dodeli -1 v aglov polje, ker bomo vse določili na novo
            arcpy.CalculateField_management(fcHs, "aglov", -1)

            # Id vseh aglomeracij za vodo v LIST
            field = "AGLO_ID"
            with arcpy.da.SearchCursor(fcAglo, "*") as cursor:
                idx = cursor.fields.index(field)
                for row in cursor:
                    agloV.append(int(row[idx]))
            # print(agloV)

            # Za vsako aglomeracijo iz seznama poišči hišne številke, ki so v njej
            i = 0
            for aglo in agloV:
                i += 1
                aktivniId = str(aglo)
                fc_selected = "voda_selected" + str(i)

                try:
                    # Izberi aglomeracijo
                    qry = f'"AGLO_ID"={aktivniId}'
                    agloLayer = arcpy.MakeFeatureLayer_management(fcAglo, fc_selected)
                    arcpy.SelectLayerByAttribute_management(
                        agloLayer, "NEW_SELECTION", qry
                    )
                    # cnt = arcpy.GetCount_management(flayer)
                    # print("The number of selected records is: " + str(cnt))

                    # Izberi hišne številke v izbrani aglomeraciji
                    fc_hs_selected = "hs_voda_selected" + str(i)
                    hslayer = arcpy.MakeFeatureLayer_management(fcHs, fc_hs_selected)
                    arcpy.SelectLayerByLocation_management(
                        hslayer, "COMPLETELY_WITHIN", agloLayer
                    )
                    cnt_hs = arcpy.GetCount_management(hslayer)
                    self.log(f"V aglomeraciji {aglo} je {cnt_hs} hišnih številk", black)

                    # Izpiši posamične hišne številke v aglomeracijah
                    cursor = arcpy.SearchCursor(fc_hs_selected)
                    field = "ST_HS"
                    # for row in cursor:
                    #     print(int(row.getValue(field)))

                    # Izbranim hišnim številkam zapiši številko aglomeracije
                    arcpy.CalculateField_management(fc_hs_selected, "aglov", aglo)

                except Exception as e:
                    self.log("Error: " + e.args[0], v.red)

            # Konec agloVoda

            # Zapiši v bazo s hišnimi številkami v katero aglomeracijo spadajo
            self.log("", black)
            self.log("Aglomeracije kanalizacija", blue)
            self.log("", black)

            agloK = []

            fcAglo = r"Aglomeracije/aglo_kanal_2020"  # Tabela v bazi
            fcHs = r"RPE/Hisne_stevilke"
            field = "aglok"
            hsFieldType = "LONG"
            createField = True

            # Preveri, če v hisne_stevilke obstaja field aglok (long), če ne ga naredi
            lstFields = arcpy.ListFields(fcHs)

            for row in lstFields:
                if row.name == field:
                    createField = False
                    self.log("Field exists -" + row.name, black)

            if createField:  # Create field aglov
                try:
                    self.log("Creating field " + field, black)
                    arcpy.management.AddField(fcHs, field, hsFieldType)
                except Exception as e:
                    self.log("Error: " + e.args[0], black)

            # Vsem zapisom dodeli -1 v aglok polje, ker bomo vse določili na novo
            arcpy.CalculateField_management(fcHs, "aglok", -1)

            # Id vseh aglomeracij za kanalizacijo v LIST
            field = "AGLO_ID"
            with arcpy.da.SearchCursor(fcAglo, "*") as cursor:
                idx = cursor.fields.index(field)
                for row in cursor:
                    agloK.append(int(row[idx]))
            # print(agloV)

            # Za vsako aglomeracijo iz seznama poišči hišne številke, ki so v njej
            i = 0
            for aglo in agloK:
                i += 1
                aktivniId = str(aglo)
                fc_selected = "kan_selected" + str(i)

                try:
                    # Izberi aglomeracijo
                    qry = f'"AGLO_ID"={aktivniId}'
                    agloLayer = arcpy.MakeFeatureLayer_management(fcAglo, fc_selected)
                    arcpy.SelectLayerByAttribute_management(
                        agloLayer, "NEW_SELECTION", qry
                    )
                    # cnt = arcpy.GetCount_management(flayer)
                    # print("The number of selected records is: " + str(cnt))

                    # Izberi hišne številke v izbrani aglomeraciji
                    fc_hs_selected = "hs_kan_selected" + str(i)
                    hslayer = arcpy.MakeFeatureLayer_management(fcHs, fc_hs_selected)
                    arcpy.SelectLayerByLocation_management(
                        hslayer, "COMPLETELY_WITHIN", agloLayer
                    )
                    cnt_hs = arcpy.GetCount_management(hslayer)
                    self.log(f"V aglomeraciji {aglo} je {cnt_hs} hišnih številk", black)

                    # Izpiši posamične hišne številke v aglomeracijah
                    arcpy.SearchCursor(fc_hs_selected)
                    # field = "ST_HS"
                    # for row in cursor:
                    #     print(int(row.getValue(field)))

                    # Izbranim hišnim številkam zapiši številko aglomeracije
                    arcpy.CalculateField_management(fc_hs_selected, "aglok", aglo)

                except Exception as e:
                    self.log("Error: " + e.args[0], err)
            self.log("", black)

            minutes, seconds = stop(start_time)
            self.log(f"Končano v {minutes} min {seconds} sek.", blue)
        else:
            self.log(f"Error: datoteka {fcHs} je zaklenjena", err)

    # Konec agloKan
