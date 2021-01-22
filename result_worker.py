import sys


from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic.properties import QtCore
from PyQt5 import QtCore
from resultui import Ui_MainWindow as W_ui

class Result_manager(QMainWindow, W_ui):
    def __init__(self, total_p, total_c, maxi_c, med_c):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Статистика аккаунта')
        self.setFixedSize(350, 310)

        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)

        """self.lineEdit_2.setAlignment(QtCore.AlignCenter)
        self.lineEdit_3.setAlignment(QtCore.AlignCenter)
        self.lineEdit_4.setAlignment(QtCore.AlignCenter)"""

        self.lineEdit.setText(str(total_c))
        self.lineEdit_2.setText(str(total_p))
        self.lineEdit_3.setText(str(maxi_c))
        self.lineEdit_4.setText(str(med_c))


        self.lineEdit.setDisabled(True)
        self.lineEdit_2.setDisabled(True)
        self.lineEdit_3.setDisabled(True)
        self.lineEdit_4.setDisabled(True)

        self.pushButton.clicked.connect(self.cl)

    def cl(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.cl()


def result_shower(total_games: int, total_count: int, max_count: int, med_count: float):
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    work_class =Result_manager(total_games, total_count, max_count, med_count)
    work_class.show()
    if app.exec_():
        pass
    return True

if __name__ == '__main__':
    result_shower(1,2, 3,4)