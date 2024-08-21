import sys

# import arcpy
# import vars
# from mysql_rutine import ConnectMySql

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import Qt
from PySide6.QtCore import Slot
from ui_form import Ui_MainWindow
from logger import Logger
from comm import Comm

# from aglo_hs import AgloHs
# from om_v_arcgis import OmArcgis


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.comm = Comm()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.comm.signalText[str, Qt.GlobalColor].connect(self.izpis_v_text_box)
        self.ui.btn_konec.clicked.connect(konec)
        self.ui.btn_om_arcgis_table.clicked.connect(self.odjemna_arcgis)
        # self.ui.btn_porocilo_voda.clicked.connect(self.porocilo_voda)
        self.ui.btn_hs_aglo.clicked.connect(self.aglo_hs)
        self.logWindow = self.ui.textEdit
        self.logger = Logger(comm=self.comm)

        # self.aglohs = AgloHs(comm=self.comm)
        # self.omarcgis = OmArcgis(comm=self.comm)

        # self.napolni_om_fc()
        # self.odjemna_arcgis()

    def keyPressEvent(self, e):
        print("Keypress event", e)
        if e.key() == Qt.Key.Key_F10:
            konec()

    @Slot(str, Qt.GlobalColor)
    def izpis_v_text_box(self, text, col):
        self.logWindow.setTextColor(col)
        self.logWindow.append(text)
        self.logWindow.repaint()
        print("log:", text)

    def odjemna_arcgis(self):
        self.omarcgis.napolni_om_fc()

    def aglo_hs(self):
        self.aglohs.agloVoda()
        self.aglohs.agloKan()


def konec():
    app.exit()
    print("Konec.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    # aglohs = AgloHs()
    widget.show()
    sys.exit(app.exec())
