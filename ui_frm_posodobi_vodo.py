# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_posodobi_vodooXfMNW.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QLabel,
    QPushButton, QSizePolicy, QWidget)

class Ui_frmPosodobiv(object):
    def setupUi(self, frmPosodobiv):
        if not frmPosodobiv.objectName():
            frmPosodobiv.setObjectName(u"frmPosodobiv")
        frmPosodobiv.resize(400, 300)
        font = QFont()
        font.setFamilies([u"Inter"])
        font.setPointSize(10)
        frmPosodobiv.setFont(font)
        self.cb_linije = QCheckBox(frmPosodobiv)
        self.cb_linije.setObjectName(u"cb_linije")
        self.cb_linije.setGeometry(QRect(10, 70, 211, 20))
        self.cb_jaski = QCheckBox(frmPosodobiv)
        self.cb_jaski.setObjectName(u"cb_jaski")
        self.cb_jaski.setGeometry(QRect(10, 100, 231, 20))
        self.label = QLabel(frmPosodobiv)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 361, 16))
        font1 = QFont()
        font1.setFamilies([u"Inter"])
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.btn_posodobi = QPushButton(frmPosodobiv)
        self.btn_posodobi.setObjectName(u"btn_posodobi")
        self.btn_posodobi.setGeometry(QRect(10, 240, 91, 41))
        self.btn_cancel = QPushButton(frmPosodobiv)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setGeometry(QRect(120, 240, 91, 41))

        self.retranslateUi(frmPosodobiv)

        QMetaObject.connectSlotsByName(frmPosodobiv)
    # setupUi

    def retranslateUi(self, frmPosodobiv):
        frmPosodobiv.setWindowTitle(QCoreApplication.translate("frmPosodobiv", u"Posodobi kanalizacijo", None))
        self.cb_linije.setText(QCoreApplication.translate("frmPosodobiv", u"Kanalizacijske linije", None))
        self.cb_jaski.setText(QCoreApplication.translate("frmPosodobiv", u"Kanalizacijski ja\u0161ki", None))
        self.label.setText(QCoreApplication.translate("frmPosodobiv", u"Posodobi kanalizacijske podatke v ArcGis Online", None))
        self.btn_posodobi.setText(QCoreApplication.translate("frmPosodobiv", u"Posodobi", None))
        self.btn_cancel.setText(QCoreApplication.translate("frmPosodobiv", u"Prekli\u010di", None))
    # retranslateUi

