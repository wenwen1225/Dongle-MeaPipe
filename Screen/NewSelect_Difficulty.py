from PyQt5 import QtWidgets, QtGui, QtCore
import os 

class Ui_NewSelectDifficulty(QtWidgets.QWidget):
    difficulty_selected = QtCore.pyqtSignal(str)  
    prevButton_clicked = QtCore.pyqtSignal() 

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        self.setGeometry(screen_geometry)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)  

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setFont(QtGui.QFont("標楷體", 48))
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.label)

        # 間隔
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer)

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("QGroupBox { border: none; }")  
        self.groupBox.setTitle("")  

        self.verticalLayoutGroupBox = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayoutGroupBox.setObjectName("verticalLayoutGroupBox")

        # 按鈕與圖片
        self.add_button_with_icon("簡單", "icon1.png")
        self.add_button_with_icon("普通", "icon2.png")
        self.add_button_with_icon("困難", "icon3.png")
        self.add_button_with_icon("隨機挑戰", "icon4.png")

        self.verticalLayout.addWidget(self.groupBox)

        # 上一步
        self.prevButton = QtWidgets.QPushButton(self.centralwidget)
        self.prevButton.setFont(QtGui.QFont("標楷體", 18))
        self.prevButton.setMinimumHeight(100)
        self.prevButton.setFixedWidth(400) 
        self.verticalLayout.addWidget(self.prevButton, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)
        self.prevButton.clicked.connect(self.on_prev_clicked)

        self.setLayout(self.verticalLayout)
        self.retranslateUi()

    # 文字顯示
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "難易度選擇"))
        self.prevButton.setText(_translate("MainWindow", "上一步"))

    # 難易度選擇+手勢圖片
    def add_button_with_icon(self, text, icon_filename):
        button = QtWidgets.QPushButton(self.groupBox)
        button.setFont(QtGui.QFont("標楷體", 30))
        button.setMinimumHeight(200)
        button.setFixedWidth(600)
        button.setText(text)

        img_path = os.path.join(os.path.dirname(__file__), 'img',  icon_filename)
        pixmap = QtGui.QPixmap(img_path)
        icon_label = QtWidgets.QLabel(self.groupBox)
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(200, 200)
        icon_label.setScaledContents(True)  

        button.clicked.connect(lambda: self.on_difficulty_selected(text))

        layout = QtWidgets.QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(button, alignment=QtCore.Qt.AlignLeft)
        layout.addWidget(icon_label, alignment=QtCore.Qt.AlignRight)
        layout.addStretch(1)
        self.verticalLayoutGroupBox.addLayout(layout)

    # 難易度
    def on_difficulty_selected(self, difficulty):
        self.difficulty_selected.emit(difficulty)

    # 上一步
    def on_prev_clicked(self):
        self.prevButton_clicked.emit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_NewSelectDifficulty()
    
    MainWindow.setCentralWidget(ui)

    window_rect = MainWindow.frameGeometry()
    center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
    window_rect.moveCenter(center_point)
    MainWindow.move(window_rect.topLeft())

    MainWindow.show()
    sys.exit(app.exec_())
