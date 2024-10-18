# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1146, 908)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        palette1 = QPalette()
        brush1 = QBrush(QColor(222, 222, 222, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        self.centralwidget.setPalette(palette1)
        font = QFont()
        font.setFamilies([u"Inter"])
        font.setPointSize(10)
        self.centralwidget.setFont(font)
        self.centralwidget.setAutoFillBackground(True)
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.top_layout = QHBoxLayout()
        self.top_layout.setObjectName(u"top_layout")
        self.top_layout.setContentsMargins(10, -1, -1, -1)
        self.label_wks = QLabel(self.centralwidget)
        self.label_wks.setObjectName(u"label_wks")

        self.top_layout.addWidget(self.label_wks)

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.top_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel(self.centralwidget)
        self.progress_label.setObjectName(u"progress_label")

        self.top_layout.addWidget(self.progress_label)

        self.top_layout.setStretch(0, 5)
        self.top_layout.setStretch(1, 2)
        self.top_layout.setStretch(2, 3)

        self.verticalLayout.addLayout(self.top_layout)

        self.center_layout = QHBoxLayout()
        self.center_layout.setObjectName(u"center_layout")
        self.center_left_layout = QVBoxLayout()
        self.center_left_layout.setSpacing(10)
        self.center_left_layout.setObjectName(u"center_left_layout")
        self.center_left_layout.setContentsMargins(3, -1, 5, -1)
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        palette2 = QPalette()
        brush2 = QBrush(QColor(240, 240, 240, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.frame_2.setPalette(palette2)
        self.frame_2.setAutoFillBackground(True)
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 10, 101, 16))
        self.btn_om_arcgis_table = QPushButton(self.frame_2)
        self.btn_om_arcgis_table.setObjectName(u"btn_om_arcgis_table")
        self.btn_om_arcgis_table.setGeometry(QRect(10, 40, 131, 40))
        self.btn_om_arcgis_table.setMinimumSize(QSize(100, 40))
        self.textEdit_2 = QTextEdit(self.frame_2)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(150, 40, 271, 41))
        font1 = QFont()
        font1.setFamilies([u"Inter"])
        font1.setPointSize(9)
        self.textEdit_2.setFont(font1)
        self.textEdit_2.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.btn_hs_aglo = QPushButton(self.frame_2)
        self.btn_hs_aglo.setObjectName(u"btn_hs_aglo")
        self.btn_hs_aglo.setGeometry(QRect(10, 140, 131, 40))
        self.btn_hs_aglo.setMinimumSize(QSize(100, 40))
        self.textEdit_3 = QTextEdit(self.frame_2)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setGeometry(QRect(150, 140, 271, 41))
        self.textEdit_3.setFont(font1)
        self.textEdit_3.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.btn_prenesi_hs = QPushButton(self.frame_2)
        self.btn_prenesi_hs.setObjectName(u"btn_prenesi_hs")
        self.btn_prenesi_hs.setGeometry(QRect(10, 90, 131, 40))
        self.btn_prenesi_hs.setMinimumSize(QSize(100, 40))
        self.textEdit_4 = QTextEdit(self.frame_2)
        self.textEdit_4.setObjectName(u"textEdit_4")
        self.textEdit_4.setGeometry(QRect(150, 90, 271, 41))
        self.textEdit_4.setFont(font1)
        self.textEdit_4.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit_4.setFrameShadow(QFrame.Shadow.Sunken)
        self.btn_brisi_hs = QPushButton(self.frame_2)
        self.btn_brisi_hs.setObjectName(u"btn_brisi_hs")
        self.btn_brisi_hs.setGeometry(QRect(10, 190, 131, 40))
        self.btn_brisi_hs.setMinimumSize(QSize(100, 40))
        self.textEdit_5 = QTextEdit(self.frame_2)
        self.textEdit_5.setObjectName(u"textEdit_5")
        self.textEdit_5.setGeometry(QRect(150, 190, 271, 41))
        self.textEdit_5.setFont(font1)
        self.textEdit_5.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit_5.setFrameShadow(QFrame.Shadow.Sunken)
        self.textEdit_6 = QTextEdit(self.frame_2)
        self.textEdit_6.setObjectName(u"textEdit_6")
        self.textEdit_6.setGeometry(QRect(150, 240, 271, 41))
        self.textEdit_6.setFont(font1)
        self.textEdit_6.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit_6.setFrameShadow(QFrame.Shadow.Sunken)
        self.btn_preb = QPushButton(self.frame_2)
        self.btn_preb.setObjectName(u"btn_preb")
        self.btn_preb.setGeometry(QRect(10, 240, 131, 40))
        self.btn_preb.setMinimumSize(QSize(100, 40))
        self.textEdit_7 = QTextEdit(self.frame_2)
        self.textEdit_7.setObjectName(u"textEdit_7")
        self.textEdit_7.setGeometry(QRect(150, 290, 271, 41))
        self.textEdit_7.setFont(font1)
        self.textEdit_7.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit_7.setFrameShadow(QFrame.Shadow.Sunken)
        self.btn_hsmid_crp = QPushButton(self.frame_2)
        self.btn_hsmid_crp.setObjectName(u"btn_hsmid_crp")
        self.btn_hsmid_crp.setGeometry(QRect(10, 290, 131, 40))
        self.btn_hsmid_crp.setMinimumSize(QSize(100, 40))
        self.btn_infotim = QPushButton(self.frame_2)
        self.btn_infotim.setObjectName(u"btn_infotim")
        self.btn_infotim.setGeometry(QRect(10, 340, 131, 40))
        self.btn_infotim.setMinimumSize(QSize(100, 40))
        self.textEdit_8 = QTextEdit(self.frame_2)
        self.textEdit_8.setObjectName(u"textEdit_8")
        self.textEdit_8.setGeometry(QRect(150, 340, 271, 41))
        self.textEdit_8.setFont(font1)
        self.textEdit_8.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.center_left_layout.addWidget(self.frame_2)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        palette3 = QPalette()
        palette3.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.frame.setPalette(palette3)
        self.frame.setAutoFillBackground(True)
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 101, 16))
        self.btn_om_arcgis_ol = QPushButton(self.frame)
        self.btn_om_arcgis_ol.setObjectName(u"btn_om_arcgis_ol")
        self.btn_om_arcgis_ol.setGeometry(QRect(10, 40, 131, 40))
        self.btn_om_arcgis_ol.setMinimumSize(QSize(100, 40))
        self.btn_aglo_om = QPushButton(self.frame)
        self.btn_aglo_om.setObjectName(u"btn_aglo_om")
        self.btn_aglo_om.setGeometry(QRect(10, 90, 131, 40))
        self.btn_aglo_om.setMinimumSize(QSize(100, 40))
        self.btn_posodobi_kanal = QPushButton(self.frame)
        self.btn_posodobi_kanal.setObjectName(u"btn_posodobi_kanal")
        self.btn_posodobi_kanal.setGeometry(QRect(10, 140, 131, 40))
        self.btn_posodobi_kanal.setMinimumSize(QSize(100, 40))

        self.center_left_layout.addWidget(self.frame)

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        palette4 = QPalette()
        palette4.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette4.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette4.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette4.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.frame_3.setPalette(palette4)
        self.frame_3.setAutoFillBackground(True)
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.btn_porocilo_voda = QPushButton(self.frame_3)
        self.btn_porocilo_voda.setObjectName(u"btn_porocilo_voda")
        self.btn_porocilo_voda.setGeometry(QRect(10, 40, 131, 40))
        self.btn_porocilo_voda.setMinimumSize(QSize(100, 40))
        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 10, 101, 16))

        self.center_left_layout.addWidget(self.frame_3)

        self.center_left_layout.setStretch(0, 10)
        self.center_left_layout.setStretch(1, 5)
        self.center_left_layout.setStretch(2, 3)

        self.center_layout.addLayout(self.center_left_layout)

        self.center_right_layout = QVBoxLayout()
        self.center_right_layout.setObjectName(u"center_right_layout")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setEnabled(True)
        palette5 = QPalette()
        brush3 = QBrush(QColor(246, 246, 246, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette5.setBrush(QPalette.Active, QPalette.Window, brush3)
        palette5.setBrush(QPalette.Inactive, QPalette.Window, brush3)
        palette5.setBrush(QPalette.Disabled, QPalette.Base, brush3)
        palette5.setBrush(QPalette.Disabled, QPalette.Window, brush3)
        self.textEdit.setPalette(palette5)
        font2 = QFont()
        font2.setFamilies([u"Cascadia Code"])
        font2.setPointSize(10)
        self.textEdit.setFont(font2)
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit.setFrameShadow(QFrame.Shadow.Raised)
        self.textEdit.setReadOnly(True)

        self.center_right_layout.addWidget(self.textEdit)


        self.center_layout.addLayout(self.center_right_layout)

        self.center_layout.setStretch(0, 5)
        self.center_layout.setStretch(1, 5)

        self.verticalLayout.addLayout(self.center_layout)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setObjectName(u"bottom_layout")
        self.btn_konec = QPushButton(self.centralwidget)
        self.btn_konec.setObjectName(u"btn_konec")
        self.btn_konec.setMaximumSize(QSize(100, 40))

        self.bottom_layout.addWidget(self.btn_konec)


        self.verticalLayout.addLayout(self.bottom_layout)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 30)
        self.verticalLayout.setStretch(2, 2)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Kataster", None))
        self.label_wks.setText(QCoreApplication.translate("MainWindow", u"label_wks", None))
        self.progress_label.setText(QCoreApplication.translate("MainWindow", u"progress_label", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"ArcGis Desktop", None))
        self.btn_om_arcgis_table.setText(QCoreApplication.translate("MainWindow", u"OM ->ArcGis", None))
        self.textEdit_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Inter'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Odjemna mesta iz Bass prenesi v ArcGis</p></body></html>", None))
        self.btn_hs_aglo.setText(QCoreApplication.translate("MainWindow", u"Aglo -> Hs", None))
        self.textEdit_3.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Inter'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">V tabelo s hi\u0161nimi \u0161tevilkami zapi\u0161i pravilne aglomeracije</p></body></html>", None))
        self.btn_prenesi_hs.setText(QCoreApplication.translate("MainWindow", u"Prenesi H\u0161", None))
        self.textEdit_4.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Inter'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">S portala Geoserver prenesi nove hi\u0161ne \u0161tevilke in jih shrani v kataster</p></body></html>", None))
        self.btn_brisi_hs.setText(QCoreApplication.translate("MainWindow", u"Bri\u0161i H\u0160", None))
        self.textEdit_5.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Inter'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Zbri\u0161i hi\u0161ne \u0161tevilke, ki niso v ob\u010dinah Radgona, Apa\u010de, Radenci</p></body></html>", None))
        self.textEdit_6.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Inter'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">V datoteko s H\u0160 vpi\u0161i \u0161tevilo prebivalcev iz CRP Excel (polja: hsmid,stalno, zacasno)</p></body></html>", None))
        self.btn_preb.setText(QCoreApplication.translate("MainWindow", u"Prebivalci v H\u0160", None))
        self.textEdit_7.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Inter'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">V Excel datoteko s CRP dodaj HSMID za stalno in za\u010dasno bivali\u0161\u010de</p></body></html>", None))
        self.btn_hsmid_crp.setText(QCoreApplication.translate("MainWindow", u"HSMID v CRP", None))
        self.btn_infotim.setText(QCoreApplication.translate("MainWindow", u"Uvozi Infotim", None))
        self.textEdit_8.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Inter'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Uvozi vodomere iz Infotim aplikacije </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">v ArcGIS Pro</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"ArcGis Online", None))
        self.btn_om_arcgis_ol.setText(QCoreApplication.translate("MainWindow", u"OM ->ArcGis OL", None))
        self.btn_aglo_om.setText(QCoreApplication.translate("MainWindow", u"Aglo ->OM OL", None))
        self.btn_posodobi_kanal.setText(QCoreApplication.translate("MainWindow", u"Posodobi kanal.", None))
        self.btn_porocilo_voda.setText(QCoreApplication.translate("MainWindow", u"Vodovod", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Poro\u010dila", None))
        self.btn_konec.setText(QCoreApplication.translate("MainWindow", u"Konec (F10)", None))
    # retranslateUi

