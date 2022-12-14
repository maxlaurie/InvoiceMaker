# Main_InvoiceMaker.py
# Version 1.1
# Max Laurie 12/12/2022

# Generates an invoice from the GUI form/config.ini

from PyQt6 import QtWidgets
import UI_InvoiceMaker
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    
    ui = UI_InvoiceMaker.Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec())
