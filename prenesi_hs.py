import arcpy
from arcpy import env
import vars
import time
from logger import Logger
from comm import Comm
import requests

black = vars.black
red = vars.darkRed
green = vars.darkGreen
blue = vars.darkBlue
err = vars.red

# # Spodaj levo
# x1='15.8821'
# y1='46.5813'
#
# # Zgoraj desno
# x2='16.0373'
# y2='46.6881'

# Spodaj levo
x1 = "15.9507"
y1 = "46.6806"
# Zgoraj desno
x2 = "15.9598"
y2 = "46.6836"


def convert_to_slovenia_grid(lat, lon):
    input_sr = arcpy.SpatialReference(4326)  # WGS 1984
    output_sr = arcpy.SpatialReference(3794)  # Slovenia National Grid 1996

    point = arcpy.Point(lon, lat)
    point_geom = arcpy.PointGeometry(point, input_sr)
    projected_point_geom = point_geom.projectAs(output_sr)

    x_meters = projected_point_geom.centroid.X
    y_meters = projected_point_geom.centroid.Y

    return x_meters, y_meters


def stop(st):
    end_time = time.time()
    elapsed_time = end_time - st
    m = int(elapsed_time / 60)
    s = int(elapsed_time % 60)
    return m, s


class HsArcgis(Comm):
    # env.workspace = vars.wkspace

    def __init__(self, comm=Comm()):
        super(HsArcgis, self).__init__()
        self.comm = comm
        self.logger = Logger(comm=self.comm)

    def log(self, in_str):
        self.logger.izpisi(in_str, black)

    def logc(self, in_str, barva):
        self.logger.izpisi(in_str, barva)

    def presledek(self):
        self.log("\n")

    def izprazni_fc(self, fc):
        try:
            arcpy.management.DeleteRows(fc)
            self.log("Brišem stare zapise " + str(fc))
            print("Brišem stare zapise " + str(fc))
        except Exception as e:
            print("Napaka pri brisanju.", e)
            self.logc("Napaka pri brisanju." + str(e), err)

    def prenesi_hs(self):
        hs_fc = "RPE\hisne_stevilke"
        env.workspace = vars.wkspace
        self.log("Workspace: " + str(env.workspace))
        self.log(f"Arcgis datoteka: {hs_fc}")
        start_time = time.time()
        self.presledek()
        print("Prenesi hišne številke s portala Geoserver v Arcgis Pro")
        self.logc("Prenesi hišne številke s portala Geoserver v Arcgis Pro", green)
        url = f"https://ipi.eprostor.gov.si/wfs-si-gurs-kn/ogc/features/collections/SI.GURS.KN:HISNE_STEVILKE/items?bbox={x1},{y1},{x2},{y2}&filter-lang=cql-text&additionalProp1"
        self.presledek()

        self.log("Prenašam hišne številke s portala...")
        response = requests.get(url)
        geojson_data = response.json()
        # print(str(len(geojson_data)) + " zapisov")

        hisne_stevilke = []

        self.log("Pretvarjam koordinate v SLO 1996...")
        for feature in geojson_data["features"]:
            coords = feature["geometry"]["coordinates"]
            x, y = convert_to_slovenia_grid(coords[1], coords[0])
            # print("coord", coords, f"slo x {int(x)} y {int(y)}")
            props = list(feature["properties"].values())
            new_hs = (
                (x, y),
                props[0],
                props[1],
                props[2],
                props[3],
                props[4],
                props[5],
                props[6],
                props[7],
                props[8],
                props[9],
                props[10],
                -9,
                -9,
                -9,
                -9,
                -9,
            )
            hisne_stevilke.append(new_hs)
        novih_zapisov = len(hisne_stevilke)
        # Shrani v ArcGis
        fields = [
            "SHAPE@XY",
            "FEATUREID",
            "EID_HISNA_STEVILKA",
            "HS_STEVILKA",
            "HS_DODATEK",
            "EID_STAVBA",
            "EID_NASELJE",
            "EID_ULICA",
            "TIP_TABLICE",
            "EID_POSTNI_OKOLIS",
            "DATUM_SYS",
            "ST_HS",
            "aglov",
            "aglok",
            "prebivalcev",
            "stalno",
            "zacasno",
        ]

        starih_zapisov = arcpy.management.GetCount(hs_fc)
        self.izprazni_fc(hs_fc)
        self.log(rf"Shranjujem {novih_zapisov} hišnih številk v Arcgis Pro...")
        edit = arcpy.da.Editor(env.workspace)
        edit.startEditing(False, True)

        for hs in hisne_stevilke:
            try:
                edit.startOperation()
                with arcpy.da.InsertCursor(hs_fc, fields) as cursor:
                    cursor.insertRow(hs)
            except Exception as e:
                # self.napaka(e)
                self.logc("Napaka pri shranjevanju hišnih številk." + str(e), err)
            finally:
                edit.stopOperation()

        edit.stopEditing(True)
        razlika = int(starih_zapisov[0]) - novih_zapisov
        self.presledek()

        self.log(f"Prejšnje stanje: {starih_zapisov} hišnih številk.")
        self.log(f"Novo stanje: {novih_zapisov} hišnih številk.")
        self.log(f"Razlika: {razlika} hišnih številk.")
        self.presledek()
        minutes, seconds = stop(start_time)
        self.logc(f"Končano v {minutes} min {seconds} sek.", blue)
