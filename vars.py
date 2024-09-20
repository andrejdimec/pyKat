from PySide6.QtCore import Qt

# Variable
# wkspace = r"D:\Kataster\GR_D96\Database\GR_D96_1.gdb"

# Arcgis pro
wkspace = r"D:\Kataster\GR_D96\Database\GR_D96.gdb"
# aktualna_karta = r"Kataster_2024_09.aprx"
# aktualna_karta = r"dev_project.aprx"
# aprx_name = r"dev_project.aprx"
aprx_name = r"Kataster_2024_09.aprx"
aprx_path = r"d:\Kataster\GR_D96\Projects"
map_name = "Kataster D96"
# map_name = "map1"


# Arcgis Online
ago_username = "komunala_radgona"
ago_password = "kora1234"
ago_url = "https://www.arcgis.com"
ago_karta = "Karta za testiranje"


# Baze podatkov
# MS SQL baza
msdbhost = "213.250.28.186"
msdbport = "1433"
msdbuser = "sa"
msdbpass = "Pl@n3tSQL"
msdbname = "Komunala_DB"

# MYSQL baza
mydbhost = "213.250.28.186"
mydbport = 3306
mydbuser = "dimec"
mydbpass = "6iXrN6J8@J"
mydbname = "radgona"

# Razno
verzija = "27.6.2024 py"
obcina_radgona_id = 29
obcina_jurij_id = 116
obcina_apace_id = 195
obcina_radenci_id = 100
obcine_id = [obcina_apace_id, obcina_radenci_id, obcina_jurij_id, obcina_radgona_id]
obcina_radgona_eid = "110200000110268260"
obcina_apace_eid = "110200000214364379"
obcina_jurij_eid = "110200000110274235"
obcina_radenci_eid = "110200000110272536"
obcine_eid = [
    obcina_apace_eid,
    obcina_radenci_eid,
    obcina_jurij_eid,
    obcina_radgona_eid,
]
obcina_radgona = 11026826
obcina_apace = 21436437
obcina_radenci = 11027253
obcina_jurij = 11027423
# začasna lokacija za odlaganje OM brez HS
x_brez_hs = 576683
y_brez_hs = 171374

# Barve
red = Qt.GlobalColor.red
darkRed = Qt.GlobalColor.darkRed
black = Qt.GlobalColor.black
blue = Qt.GlobalColor.blue
darkBlue = Qt.GlobalColor.darkBlue
green = Qt.GlobalColor.green
darkGreen = Qt.GlobalColor.darkGreen
# red = 'red'
# darkRed = 'darkRed'
# black = 'black'
# blue = 'blue'
# darkBlue = 'darkBlue'
# green = 'green'
# darkGreen = 'darkGreen'
