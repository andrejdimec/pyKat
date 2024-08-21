import arcpy
import vars
from arcpy import env
from logger import Logger
from comm import Comm
from mysql_rutine import ConnectMySql

black = vars.black
red = vars.darkRed
green = vars.darkGreen
blue = vars.darkBlue
err = vars.red


class OmArcgis:
    env.workspace = vars.wkspace

    def __init__(self, comm=Comm()):
        super(OmArcgis, self).__init__()
        self.comm = comm
        self.logger = Logger(comm=self.comm)

    def log(self, in_str, barva):
        self.logger.izpisi(in_str, barva)

    def napolni_om_fc(self):
        env.workspace = vars.wkspace
        brez_hsmid = []
        brez_hsmid_in_xy = []
        om_fc = r"Odjemna_mesta\Odjemna_mesta_auto"
        self.presledek()
        self.log("Prenašam OM iz Bass v ArcGis " + om_fc, green)

        result_om = ConnectMySql().get_all_om()
        stevec = 0

        self.log("Prebrano iz Bass " + str(len(result_om))+' odjemnih mest', black)

        if result_om:
            self.log("Iščem storitve za odjemna mesta...", black)
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
            # For rowl

            # izprazni_fc(om_fc)
            self.izprazni_fc(om_fc)

            print("Zapisujem v Arcgis (" + str(len(result_om)) + ")")

            self.log("Zapisujem v Arcgis " +str(len(result_om)) + " odjemnih mest", black)

            # for i in range(len(brez_hsmid_in_xy)):
            #     self.log(str(i),green)
            # self.log(str(brez_hsmid_in_xy), green)
            # Zapiši tabelo v ArcGis om_table

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

            for row in result_om:
                try:
                    edit.startOperation()
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
                    self.napaka(e)
                    print("Napaka pri dodajanju om", e)
                finally:
                    edit.stopOperation()

            self.presledek()
            self.log(
                "Odjemna mesta brez HSMID, imajo pa x,y (" + str(len(brez_hsmid)) + ")",
                green,
            )
            for vrsta in brez_hsmid:
                print(vrsta)
                self.log(str(vrsta), black)

            self.presledek()
            self.log(
                "Odjemna mesta brez HSMID in brez koordinat ("
                + str(len(brez_hsmid_in_xy))
                + ")",
                green,
            )
            for vrsta in brez_hsmid_in_xy:
                print(vrsta)
                self.log(str(vrsta), black)
            self.presledek()
            # Končaj editing
            edit.stopEditing(True)
            self.log("Končano.", blue)

        else:
            self.log("Napaka pri prenosu iz Bass!", err)
            return

    def izprazni_fc(self, fc):
        # edit = arcpy.da.Editor(env.workspace)
        # edit.stopEditing(True)
        try:
            arcpy.management.DeleteRows(fc)
            # arcpy.management.TruncateTable(fc)
            self.log("Praznim datoteko " + str(fc), black)
        except Exception as e:
            self.napaka(e)

    def presledek(self):
        self.log("\n", black)

    def napaka(self, e):
        self.presledek()
        self.log("Napaka! " + str(e), err)


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
