# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_posodobi_kanalizacijo.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QTextEdit, QWidget)

class Ui_frmPosodobiKan(object):
    def setupUi(self, frmPosodobiKan):
        if not frmPosodobiKan.objectName():
            frmPosodobiKan.setObjectName(u"frmPosodobiKan")
        frmPosodobiKan.resize(854, 362)
        font = QFont()
        font.setFamilies([u"Inter"])
        font.setPointSize(10)
        frmPosodobiKan.setFont(font)
        self.horizontalLayout = QHBoxLayout(frmPosodobiKan)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(frmPosodobiKan)
        self.frame.setObjectName(u"frame")
        palette = QPalette()
        brush = QBrush(QColor(246, 246, 246, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.frame.setPalette(palette)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 344, 19))
        font1 = QFont()
        font1.setFamilies([u"Inter"])
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.cb_jaski = QCheckBox(self.frame)
        self.cb_jaski.setObjectName(u"cb_jaski")
        self.cb_jaski.setGeometry(QRect(20, 60, 137, 20))
        self.cb_linije = QCheckBox(self.frame)
        self.cb_linije.setObjectName(u"cb_linije")
        self.cb_linije.setGeometry(QRect(20, 90, 143, 20))
        self.btn_posodobi = QPushButton(self.frame)
        self.btn_posodobi.setObjectName(u"btn_posodobi")
        self.btn_posodobi.setGeometry(QRect(20, 280, 91, 41))
        self.btn_cancel = QPushButton(self.frame)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setGeometry(QRect(140, 280, 91, 41))
        self.cb_iztok = QCheckBox(self.frame)
        self.cb_iztok.setObjectName(u"cb_iztok")
        self.cb_iztok.setGeometry(QRect(20, 150, 143, 20))

        self.horizontalLayout.addWidget(self.frame)

        self.te2 = QTextEdit(frmPosodobiKan)
        self.te2.setObjectName(u"te2")
        palette1 = QPalette()
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        self.te2.setPalette(palette1)
        self.te2.setAutoFillBackground(True)
        self.te2.setFrameShape(QFrame.Shape.Box)
        self.te2.setFrameShadow(QFrame.Shadow.Plain)
        self.te2.setLineWidth(0)

        self.horizontalLayout.addWidget(self.te2)

        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 5)

        self.retranslateUi(frmPosodobiKan)

        QMetaObject.connectSlotsByName(frmPosodobiKan)
    # setupUi

    def retranslateUi(self, frmPosodobiKan):
        frmPosodobiKan.setWindowTitle(QCoreApplication.translate("frmPosodobiKan", u"Posodobi kanalizacijo", None))
        self.label.setText(QCoreApplication.translate("frmPosodobiKan", u"Posodobi kanalizacijske podatke v ArcGis Online", None))
        self.cb_jaski.setText(QCoreApplication.translate("frmPosodobiKan", u"Kanalizacijski ja\u0161ki", None))
        self.cb_linije.setText(QCoreApplication.translate("frmPosodobiKan", u"Kanalizacijske linije", None))
        self.btn_posodobi.setText(QCoreApplication.translate("frmPosodobiKan", u"Posodobi", None))
        self.btn_cancel.setText(QCoreApplication.translate("frmPosodobiKan", u"Nazaj", None))
        self.cb_iztok.setText(QCoreApplication.translate("frmPosodobiKan", u"Iztok kanalizacije", None))
    # retranslateUi

