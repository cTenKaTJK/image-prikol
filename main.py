from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ImagePrikol import ImageRedact
import sys


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('prikol.ui', self)

        self.image_opened = False
        self.select = False
        self.c = 1

        self.Load.clicked.connect(self.load_image)
        self.ReflectOX.clicked.connect(self.reflect_OX)
        self.ReflectOY.clicked.connect(self.reflect_OY)
        self.Negative.clicked.connect(self.negative)
        self.Reset.clicked.connect(self.reset)
        self.Crop.clicked.connect(self.crop)
        self.Slider.valueChanged[int].connect(self.get_value)
        self.Prikol.clicked.connect(self.prikol)

    '''
        if self.image_opened:
            r = self.Red_delta_slider.value()
            g = self.Green_delta_slider.value()
            b = self.Blue_delta_slider.value()
            self.Set_color_map.clicked.connect(self.tone(r, g, b))
    '''

    def load_image(self):
        self.file_name = QFileDialog.getOpenFileName(self,
                                                     'Выбрать Изображение', '',
                                                     'Изображение (*.png);;Шакал (*.jpg);;Все файлы (*)')[0]
        self.kartinko = ImageRedact(self.file_name)
        self.kartinko.autosave()
        self.show_image()

    def show_image(self):
        self.image_opened = True
        x = self.kartinko.get_x()
        y = self.kartinko.get_y()
        self.c = max(x / 810, y / 530)
        pixmap = QPixmap(self.file_name).scaled(int(x / self.c), int(y / self.c))
        self.image.setPixmap(pixmap)

    def get_value(self, value):
        self.SliderValue = value

    def reflect_OX(self):
        if self.image_opened:
            self.kartinko.reflectOX()
            self.kartinko.update()
            self.show_image()

    def reflect_OY(self):
        if self.image_opened:
            self.kartinko.reflectOY()
            self.kartinko.update()
            self.show_image()

    def negative(self):
        if self.image_opened:
            self.kartinko.negative()
            self.kartinko.update()
            self.show_image()

    def prikol(self):
        if self.image_opened:
            self.kartinko.prikol(self.SliderValue)
            self.kartinko.update()
            self.show_image()

    def reset(self):
        if self.image_opened:
            self.kartinko.reset()
            self.kartinko.update()
            self.show_image()

    '''
    def tone(self, r, g, b):
        self.kartinko.tone(r, g, b)
        self.kartinko.update()
        self.show_image()
    '''

    def mousePressEvent(self, event):
        self.x1 = abs(int(int(event.x() - 18) * self.c))
        self.y1 = abs(int(int(event.y() - 48) * self.c))
        if self.kartinko.get_x() >= self.x1 and self.kartinko.get_y() >= self.y1:
            self.x1point.setText(f"x1: {int(self.x1)}")
            self.y1point.setText(f"y1: {int(self.y1)}")

    def mouseReleaseEvent(self, event):
        self.x2 = abs(int(int(event.x() - 18) * self.c))
        self.y2 = abs(int(int(event.y() - 48) * self.c))
        if self.kartinko.get_x() >= self.x2 and self.kartinko.get_y() >= self.y2:
            self.x2point.setText(f"x2: {int(self.x2)}")
            self.y2point.setText(f"y2: {int(self.y2)}")
            self.select = True

    def crop(self):
        if self.image_opened:
            if self.select:
                self.kartinko.crop(self.x1, self.y1, self.x2, self.y2)
            self.kartinko.update()
            self.show_image()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication([])
    win = Main()
    win.setStyleSheet('.Main {background-image: url(background.png);}')
    win.show()
    sys.exit(app.exec())
