# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog
import sys
from PyQt5.uic import loadUi
from PIL import Image
import webbrowser

from imagerec import PlakaOku


class MainWindow(QDialog):
       
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("gui.ui",self)
        self.picture.setEnabled(False)
        self.browse.clicked.connect(self.browsefiles)
        self.browse.clicked.connect(self.enablebutton)        
        self.picture.clicked.connect(self.showpicture)
        self.about.clicked.connect(self.showabout)
        
        #hızlı test etmek için, elle seçme olmadan program açıldığında çalışan fonksiyon: print("Plaka: ", (PlakaOku("C:\\Users\\usm53\\Desktop\\Cars2.png")))

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File' , 'C:/Users/usm53/Desktop','Image files (*.jpg *.png')
        self.filename.setText(fname[0])
        self.DosyaKonumu = self.filename.text().replace('/', '\\') # c:/users/usm53 den c:\\users\\usm53 (windows'un anlayacağı şekle) çevirme        
        OkunanPlaka = PlakaOku(self.DosyaKonumu)
        print("Plaka: %s" % (OkunanPlaka))
        self.lblPlaka.setText(OkunanPlaka)
        
            
    def enablebutton(self):
        self.picture.setEnabled(True)
        
    def showpicture(self):
        webbrowser.open(self.DosyaKonumu)
        
    def showabout(self):
        webbrowser.open('Gerekli Bilgiler.txt')
        
    
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(430)
    widget.setFixedHeight(350)
    widget.show()
    sys.exit(app.exec_())

