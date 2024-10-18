from PySide6.QtCore import Signal
import arcpy
from openpyxl.styles.builtins import comma

import vars
from arcpy import env
from logger import Logger
from comm import Comm
from mysql_rutine import ConnectMySql
import time

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


class OmArcgisWorker(Comm):
    env.workspace = vars.wkspace
    progress = Signal(int)
    status = Signal(str)

    def __init__(self, comm=Comm()):
        super(OmArcgisWorker, self).__init__()
        self.comm = comm
        self.logger = Logger(comm=self.comm)

    def log(self, in_str):
        self.logger.izpisi(in_str, black)

    def logc(self, in_str, barva):
        self.logger.izpisi(in_str, barva)

    def presledek(self):
        self.log("\n")

    def napolni_om_fc(self):
        start_time = time.time()
        env.workspace = vars.wkspace
        brez_hsmid = []
        brez_hsmid_in_xy = []
        om_fc = r"Odjemna_mesta\Odjemna_mesta_auto"
        self.presledek()
        self.logc("Prenašam OM iz Bass v ArcGis " + om_fc, green)

        result_om = ConnectMySql().get_all_om()
        stevec = 0

        if result_om:
            rows = len(result_om)
            self.log("Prebrano iz Bass " + str(len(result_om)) + " odjemnih mest")

            self.log("Iščem storitve za odjemna mesta...")
            for rowl in result_om:
                stevec += 1
                om_id = rowl[0]
                naziv = rowl[2]
                naslov = rowl[3]
                hsmid = str(rowl[1])
                x = rowl[21]
                y = rowl[22]
                upravitelj_id = rowl[12]

                # Preveri če ima HSMID in XY, če ne, ga daj na seznam napak
                if len(str(hsmid)) < 6:
                    dodaj = [
                        "om:"
                        + om_id
                        + " hs:"
                        + hsmid
                        + " "
                        + naziv
                        + " "
                        + naslov
                        + " lkc:"
                        + rowl[23]
                        + " x:"
                        + str(x)
                        + " y:"
                        + str(y)
                    ]

                    # Preveri, če ima vsaj x,y
                    if (x < 1) or (y < 1):
                        brez_hsmid_in_xy.append(dodaj)
                        # Nima koordinat - daj mu začasni x,y
                        rowl[21] = vars.x_brez_hs
                        rowl[22] = vars.y_brez_hs
                    else:
                        brez_hsmid.append(dodaj)

                # Če so v bass polja za aglomeracijo prazna, daj -1
                if not (isanumber(rowl[14])):
                    rowl[14] = "-1"
                if not (isanumber(rowl[15])):
                    rowl[15] = "-1"

                # Za vsako om poišči storitve

                # Voda - določi glede na šifro upravitelja
                rowl[6] = preveri_upravitelja(upravitelj_id)

                result_storitve = ConnectMySql().get_storitve(om_id)
                if result_storitve:
                    # Čiščenje
                    if result_storitve.count("CIS") > 0:
                        rowl[9] = 1
                    # Odvajanje
                    if result_storitve.count("ODV") > 0:
                        if rowl[9] == 1:
                            rowl[7] = 2
                        else:
                            rowl[7] = 1
                    # Greznice
                    if (
                        result_storitve.count("GRE") > 0
                        or result_storitve.count("GRES") > 0
                    ):
                        rowl[10] = 1

                elif result_storitve:
                    print("Nima storitev")

                    # Update status & progress bar
                self.progress.emit(int(stevec / rows * 100))
                self.status.emit(f"{stevec} / {rows}")
            # For rowl

            # izprazni_fc(om_fc)
            self.izprazni_fc(om_fc)

            self.log("Zapisujem v Arcgis " + str(len(result_om)) + " odjemnih mest")

            # for i in range(len(brez_hsmid_in_xy)):
            #     self.log(str(i),green)
            # self.log(str(brez_hsmid_in_xy), green)

            # Zapiši tabelo v ArcGis om_table
            stevec = 0

            fields = [
                "id_om",
                "HS_MID",
                "naziv",
                "naslov",
                "placnik",
                "placnik_naslov",
                "voda",
                "odvajanje",
                "odvajanje_dod",
                "ciscenje",
                "greznice",
                "odpadki",
                "id_upravljalec",
                "upravljalec",
                "aglov",
                "aglok",
                "prebivalcev",
                "stalno",
                "zacasno",
                "STATUS",
                "meter_id",
                "meter_desc",
                "SHAPE@XY",
            ]
            edit = arcpy.da.Editor(env.workspace)
            edit.startEditing(False, True)
            edit.startOperation()

            for row in result_om:
                stevec += 1
                try:
                    with arcpy.da.InsertCursor(om_fc, fields) as cursor:
                        new_row = (
                            row[0],  # om id
                            row[1],  # hsmid
                            row[2],  # naziv
                            row[3],  # naslov
                            row[4],  # pl naz
                            row[5],  # pl naslov
                            row[6],  # voda
                            row[7],  # odv
                            0,  # odv dod
                            row[9],  # cis
                            row[10],  # gre
                            row[11],  # odp
                            row[12],  # id upravljalec
                            row[13],  # upravljalec naziv
                            row[14],  # aglo kan
                            row[15],  # aglo voda
                            -1,  # prebivalci
                            -1,  # prebivalci
                            -1,  # prebivalci
                            row[18],  # status
                            row[19],  # meter id
                            row[20],  # meter desc
                            (row[21], row[22]),  # x, y
                        )
                        cursor.insertRow(new_row)
                except Exception as e:
                    # self.napaka(e)
                    self.logc("Napaka pri dodajanju om " + str(e), err)
                finally:
                    self.progress.emit(int(stevec / rows * 100))
                    self.status.emit(f"{stevec} / {rows}")

            edit.stopOperation()
            self.presledek()
            self.logc(
                "Odjemna mesta brez HSMID, imajo pa x,y (" + str(len(brez_hsmid)) + ")",
                blue,
            )
            for vrsta in brez_hsmid:
                print(vrsta)
                self.log(str(vrsta))

            self.presledek()
            self.logc(
                "Odjemna mesta brez HSMID in brez koordinat ("
                + str(len(brez_hsmid_in_xy))
                + ")",
                blue,
            )
            for vrsta in brez_hsmid_in_xy:
                print(vrsta)
                self.log(str(vrsta))
            self.presledek()
            # Končaj editing
            edit.stopEditing(True)
            self.presledek()
            minutes, seconds = stop(start_time)

            self.logc(f"Končano v {minutes} min {seconds} sek.", blue)
            # self.log("Končano.", blue)

        else:
            self.logc("Napaka pri prenosu iz Bass!", err)
            return

    def izprazni_fc(self, fc):
        # edit = arcpy.da.Editor(env.workspace)
        # edit.stopEditing(True)
        try:
            arcpy.management.DeleteRows(fc)
            # arcpy.management.TruncateTable(fc)
            self.log("Praznim datoteko " + str(fc))
        except Exception as e:
            self.napaka(e)

    def napaka(self, e):
        self.presledek()
        self.logc("Napaka! " + str(e), err)


def preveri_upravitelja(upravitelj_id):
    match upravitelj_id:
        case "01":  # Radgonski vodovod
            voda = 1
        case "25":  # MB vodovod
            voda = 2
        case "09", "10", "27", "28":  # Lastna voda
            voda = 3
        case _:
            voda = 0
    return voda


def isanumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
