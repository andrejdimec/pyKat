import arcpy
from arcpy import env
import openpyxl
from openpyxl import load_workbook

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


class PrebivalciHs(Comm):
    def __init__(self, comm=Comm()):
        super(PrebivalciHs, self).__init__()
        self.comm = comm
        self.logger = Logger(comm=self.comm)

    def prebivalci_hs(self):
        env.workspace = vars.wkspace
        self.log("Workspace: " + str(env.workspace))
        hs_fc = r"RPE\hisne_stevilke"
        na_fc = r"RPE\NA_2024"
        ul_fc = r"RPE\UL_2024"

        self.log(f"Arcgis datoteka: {hs_fc}")
        start_time = time.time()
        # dialog = QFileDialog(self)
        # dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        # dialog.setNameFilter("Excel datoteke (*.xls, *.xlsx")
        # dialog.setViewMode(QFileDialog.ViewMode.Detail)
        # dialog.setDirectory("d:/podatki/")
        # if dialog.exec():
        #     filename = dialog.selectedFiles()[0]
        #     if filename:

        print("Prebivalci v hs...")
        filename = "d:/podatki/crp-01-07-2024.xlsx"
        print(filename)
        workbook = load_workbook(filename)
        sheet = workbook.active
        seznam1 = []
        # crp = [[1, 1, 1], [2, 2, 2]]
        crp = []  # prečiščeni seznam z združenimi hsmid
        # Get the column indices for the specified headings
        header = {cell.value: cell.column for cell in sheet[1]}
        # Kolone v listi
        emso_col = header["EMŠO"]
        st_obcina_col = header["Občina STPR"]
        st_naselje_col = header["Naziv naselja STPR"]
        st_ulica_col = header["Naziv ulice STPR"]
        st_hs_col = header["Hišna št. STPR"]
        st_hsd_col = header["Hišna št. STPR dodatek"]

        zc_obcina_col = header["Občina ZCPR"]
        zc_naselje_col = header["Naziv naselja ZCPR"]
        zc_ulica_col = header["Naziv ulice ZCPR"]
        zc_hs_col = header["Hišna št. ZCPR"]
        zc_hsd_col = header["Hišna št. ZCPR dodatek"]
        # st_index=st_hs_col+st_hsd_col+st_naselje_col+st_ulica_col
        # zc_index=zc_hs_col+zc_hsd_col+zc_naselje_col+zc_ulica_col

        # Naloži vse potrebne kolone iz excela v list
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            # emso = row[emso_col - 1].value
            # st_obcina = row[st_obcina_col - 1].value
            st_ulica = row[st_ulica_col - 1].value
            st_naselje = row[st_naselje_col - 1].value
            st_hs = row[st_hs_col - 1].value
            st_hsd = row[st_hsd_col - 1].value
            # zc_obcina = row[zc_obcina_col - 1].value
            zc_ulica = row[zc_ulica_col - 1].value
            zc_naselje = row[zc_naselje_col - 1].value
            zc_hs = row[zc_hs_col - 1].value
            zc_hsd = row[zc_hsd_col - 1].value
            if st_hs is None:
                st_hs = 0
            if st_hsd is None:
                st_hsd = ""
            if st_naselje is None:
                st_naselje = ""
            if st_ulica is None:
                st_ulica = ""

            if zc_hsd is None:
                zc_hsd = ""
            if zc_naselje is None:
                zc_naselje = ""
            if zc_ulica is None:
                zc_ulica = ""
            if zc_hs is None:
                zc_hs = 0

            st_index = str(int(st_hs)) + st_hsd + st_naselje + st_ulica
            zc_index = str(int(zc_hs)) + zc_hsd + zc_naselje + zc_ulica
            seznam1.append([st_index.replace(" ", ""), zc_index.replace(" ", "")])

        # Print the list to verify the values
        print("Seznam:", seznam1)
        print("Število oseb v CRP " + str(len(seznam1)))
        # Hišne številke v list
        print("Branje HŠ")

        seznam_hs = []
        with arcpy.da.SearchCursor(hs_fc, ["*"]) as cursor:
            stevec = 0
            for row in cursor:
                stevec = stevec + 1
                eid_naselje = row[7]
                eid_ulica = row[8]
                hs = str(int(row[4]))
                hsd = row[5]
                if hsd is None:
                    hsd = ""

                # Najdi ime naselja
                query = f"EID_NASELJ = '{eid_naselje}'"
                with arcpy.da.SearchCursor(na_fc, ["NAZIV"], query) as cursorna:
                    for rowna in cursorna:
                        naziv_naselja = rowna[0]

                # Najdi ime ulice
                query = f"EID_ULICA = '{eid_ulica}'"
                naziv_ulice = naziv_naselja
                with arcpy.da.SearchCursor(ul_fc, ["NAZIV"], query) as cursorul:
                    if cursorul:
                        for rowul in cursorul:
                            naziv_ulice = rowul[0]
                dodaj_hs = hs + hsd + naziv_naselja + naziv_ulice
                seznam_hs.append([dodaj_hs.replace(" ", "")])
                if stevec > 500:
                    break

        for hs in seznam_hs:
            print(hs)

        # for row in seznam1:
        #     hsmid_isci = row[0]
        #     obstaja = False
        #     # print("išči " + str(hsmid_isci))
        #
        #     for row2 in crp:
        #         if row2[0] == hsmid_isci:
        #             obstaja = True
        #             print("Obstaja, prištej")
        #             # prištej
        #             row2[1] += row[1]
        #             row2[2] += row[2]
        #             break
        #
        #     if not obstaja:
        #         # print("Ne obstaja, dodaj hsmid " + str(hsmid_isci))
        #         crp.append(row)
        #
        # print("Vrstic v crp[] " + str(len(crp)))
        self.presledek()
        minutes, seconds = stop(start_time)
        self.logc(f"Končano v {minutes} min {seconds} sek.", blue)

    def log(self, in_str):
        self.logger.izpisi(in_str, black)

    def logc(self, in_str, barva):
        self.logger.izpisi(in_str, barva)

    def presledek(self):
        self.log("\n")
