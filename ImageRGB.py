from PyQt5.QtWidgets import QWidget,QFileDialog, QLabel
from UI.ImageRGB import Ui_ImageRGB
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QSize
from PIL.ImageQt import ImageQt
from PIL import Image
import os


class ImageRGB(QWidget, Ui_ImageRGB):

    def __init__(self):
        super(ImageRGB, self).__init__()
        self.setupUi(self)
        self.OpenImageBtn.clicked.connect(self.open_image)
        self.radioButton.index = 0
        self.radioButton_1.index = 1
        self.radioButton_2.index = 2
        self.radioButton.toggled.connect(self.on_radio_button_toggled)
        self.radioButton_1.toggled.connect(self.on_radio_button_toggled)
        self.radioButton_2.toggled.connect(self.on_radio_button_toggled)
        self.GetRGBBtn.clicked.connect(self.get_pixel)
        self.current_image_path = ''
        self.im = None
        self.im_50 = None
        self.im_100 = None
        self.thumb_path_list = []
        self.pixel_size = 0

    def open_image(self):
        img_name, img_type = QFileDialog.getOpenFileName(self, "打开图片", "", "*.png;;*.jpg;;All Files(*)")
        jpg = QPixmap(img_name).scaled(self.orgin.width(), self.orgin.height())
        self.lineEdit.setText(img_name)
        self.orgin.setPixmap(jpg)
        _width, _height = self.get_orgin_size(jpg)
        self.current_image_path = img_name
        self.init_thumbnails(self.current_image_path)
        self.radioButton.setEnabled(True)
        self.radioButton_1.setEnabled(True)
        self.radioButton_2.setEnabled(True)

    def init_thumbnails(self, path):
        self.im = Image.open(path)
        self.im_100 = self.im.copy()
        self.im_50 = self.im.copy()
        dirname, filename = os.path.split(os.path.abspath(__file__))
        img_dirname, img_temp_filename = os.path.split(os.path.abspath(path))
        filename, extension = os.path.splitext(img_temp_filename)
        thumb_path = os.path.join(dirname, 'thumb\\')
        if not os.path.exists(thumb_path):
            os.makedirs(thumb_path, mode=0o777)
        thumb_100_path = os.path.join(thumb_path, filename + 'thumb_100' + extension)
        self.thumb_path_list.append(thumb_100_path)
        thumb_50_path = os.path.join(thumb_path, filename + 'thumb_50' + extension)
        self.thumb_path_list.append(thumb_50_path)
        self.im_100.thumbnail((100, 100), Image.ANTIALIAS)
        self.im_100.save(thumb_100_path)
        self.show_thumbnails(self.im_100, self.thumb_100)
        self.im_50.thumbnail((50, 50), Image.ANTIALIAS)
        self.im_50.save(thumb_50_path)
        self.show_thumbnails(self.im_50, self.thumb_50)

    def on_radio_button_toggled(self):
        self.GetRGBBtn.setEnabled(True)

    def get_pixel(self):
        self.textBrowser.clear()
        if self.radioButton_1.isChecked():
            thumb_list = []
            y_index = self.im_100.height - 1
            while y_index >= 0:
                line_list = []
                for x in range(self.im_100.width):
                    pixel = self.im_100.getpixel((x, y_index))
                    line_list.append(ImageRGB.rgb2hex(pixel[0], pixel[1], pixel[2]))
                thumb_list.append("".join(line_list))
                y_index -= 1
            self.textBrowser.setText("\n".join(thumb_list))
        elif self.radioButton_2.isChecked():
            thumb_list = []
            y_index = self.im_50.height - 1
            while y_index >= 0:
                line_list = []
                for x in range(self.im_50.width):
                    pixel = self.im_50.getpixel((x, y_index))
                    line_list.append(ImageRGB.rgb2hex(pixel[0], pixel[1], pixel[2]))
                thumb_list.append("".join(line_list))
                y_index -= 1
            self.textBrowser.setText("\n".join(thumb_list))
        else:
            thumb_list = []
            y_index = self.im.height - 1
            while y_index >= 0:
                line_list = []
                for x in range(self.im.width):
                    pixel = self.im.getpixel((x, y_index))
                    line_list.append(ImageRGB.rgb2hex(pixel[0], pixel[1], pixel[2]))
                thumb_list.append("".join(line_list))
                y_index -= 1
            self.textBrowser.setText("\n".join(thumb_list))

    def show_thumbnails(self, img: Image, label: QLabel):
        image = ImageQt(img)
        pix_map = QPixmap.fromImage(image).scaled(label.width(), label.height())
        label.setPixmap(pix_map)

    def get_orgin_size(self, image: QPixmap):
        t = QSize(image.size())
        return QSize(t).width(), QSize(t).height()

    @staticmethod
    def rgb2hex(r, g, b):
        return '{:02x}{:02x}{:02x}'.format(r, g, b)