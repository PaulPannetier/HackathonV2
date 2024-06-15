# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QTimer)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHeaderView, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTableWidget, QTableWidgetItem,
    QWidget)
import os
from singleton import singleton
from predict import ImageDetector
from PIL import Image, ImageDraw
import cv2


@singleton
class Ui_MainWindow(object):
    label_img_path:str

    def __init__(self):
        self.cap = None
        self.timer = QTimer()

    def on_compute_button_down(self):
        from BottleMaps.bottleMaps import bottleMaps, TiltedWasteData
        imageDetector:ImageDetector = ImageDetector()
        results = imageDetector.predict(self.label_img_path)

        qimage = self.label.pixmap().toImage()
        qimage.save(os.path.join(os.getcwd(), "tmp\\qimage.png"))

        pil_img_path = os.path.join(os.getcwd(), "tmp\\qimage.png")
        pil_image = Image.open(pil_img_path)
        draw = ImageDraw.Draw(pil_image)

        for res in results:
            bottleMaps.add_waste(TiltedWasteData(res.x, res.y, res.type))
            draw.rectangle((res.x - (res.width * 0.5), res.y - (res.height * 0.5), res.x + (res.width * 0.5), res.y + (res.height * 0.5)), fill=None, outline='red')
        
        bottleMaps.save_map()

        data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
        qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
        qpixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(qpixmap)

    def on_combobox_changed(self, index):
        current_text = self.comboBox.itemText(index)
        #print(f"Current ComboBox item: {current_text}")
        if current_text == "Image":
            self.label.setPixmap(QPixmap(self.label_img_path))
            self.stop_camera()
        elif current_text == "Camera":
            self.start_camera()
        else:
            self.label.clear()
            self.stop_camera()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(image))

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1113, 727)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 541, 461))
        self.label_img_path = u"BottleMaps/000003_jpg.rf.717a772246ebd76a5719aa5868950699.jpg"
        self.label.setPixmap(QPixmap(self.label_img_path))
        self.label.setScaledContents(True)
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(210, 480, 341, 192))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(570, 10, 531, 591))
        self.label_2.setPixmap(QPixmap(u"BottleMaps/maps.png"))
        self.label_2.setScaledContents(True)
        from BottleMaps.bottleMaps import bottleMaps
        bottleMaps.save_map()
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(30, 480, 151, 31))
        self.pushButton.clicked.connect(self.on_compute_button_down)
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(30, 530, 151, 31))
        self.comboBox.setMaxVisibleItems(2)
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1113, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.comboBox.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText("")
        self.label_2.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Compute", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Image", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Camera", None))

        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

ui_MainWindow = Ui_MainWindow()
