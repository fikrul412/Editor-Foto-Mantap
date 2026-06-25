from PyQt5.QtWidgets import (
   QApplication, QWidget, QLabel, QPushButton,
   QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog,
   QFontDialog,
)
import os
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import ImageFilter

app = QApplication([])
win = QWidget()      
win.resize(700, 500)
win.setWindowTitle('Image Editor #34')


#Widgets
lb_image = QLabel("I\nM\nA\nG\nE\n\nG\nO\nE\nS\n\nH\nE\nR\nE")
btn_dir = QPushButton("Folder")
lw_files = QListWidget()


#Buttons
btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_flip = QPushButton("Mirror")
btn_blur = QPushButton("Blur")
btn_bw = QPushButton("B/W")
btn_reset = QPushButton("Reset")


#Making the layout
row = QHBoxLayout()  #MAIN LINE
col1 = QVBoxLayout()
col2 = QVBoxLayout()

#Col 1
col1.addWidget(lb_image, 95)
row_tools = QHBoxLayout() #BARIS TOMBOL
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_blur)
row_tools.addWidget(btn_bw)
row_tools.addWidget(btn_reset)
col1.addLayout(row_tools)

#Col 2
col2.addWidget(btn_dir)
col2.addWidget(lw_files)

#Laying it out
row.addLayout(col1, 80)
row.addLayout(col2, 20)
win.setLayout(row)
workdir = ""

#Styling
win.setStyleSheet('background-color: lightgreen')
btn_right.setStyleSheet('background-color: #45d61c')
btn_left.setStyleSheet('background-color: #45d61c')
btn_bw.setStyleSheet('background-color: #45d61c')
btn_blur.setStyleSheet('background-color: #45d61c')
btn_flip.setStyleSheet('background-color: #45d61c')
btn_reset.setStyleSheet('background-color: #45d61c')
btn_dir.setStyleSheet('background-color: #45d61c')


#Functions
def chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    print(workdir)

def showFilenameList():
    chooseworkdir()
    filenames = filter(os.listdir(workdir))
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

def filter(files):
    result = []
    extensions = ['.jpg', 'jpng', 'png', 'gif', 'bmp']
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

#CLASS IMAGE PROCESSOR
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = 'Modified/'
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        lb_image.hide()
        gambar = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        gambar = gambar.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(gambar)
        lb_image.show()
        
    #Image Filters
    def do_bnw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_mir(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def reset(self):
        image_path = os.path.join(workdir, self.filename)
        self.image = Image.open(image_path)
        self.showImage(image_path)
    
    #Save    
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

workimage = ImageProcessor()

#Show Image
def ShowChoosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

#Button connection
btn_dir.clicked.connect(showFilenameList)
lw_files.currentRowChanged.connect(ShowChoosenImage)
btn_bw.clicked.connect(workimage.do_bnw)
btn_blur.clicked.connect(workimage.do_blur)
btn_flip.clicked.connect(workimage.do_mir)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_reset.clicked.connect(workimage.reset)

#Execute the app
win.show()
app.exec()