from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Ui_Game_Start(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # 設定視窗
        self.setFixedSize(1080, 720)
        self.setWindowTitle("Game Start")

        # 字體設置
        font = QFont("Arial", 30)
        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setFont(font)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setGeometry(100, 100, 880, 50)

        self.show_text_with_random_effect("這是一個測試題目，包含錯字", "錯字")

    def highlight_typo_in_text(self, text, typo):
        # 使用 HTML 標籤將錯字變成紅色
        highlighted_text = text.replace(typo, f'<font color="red">{typo}</font>')
        return highlighted_text

    def show_text_with_random_effect(self, text, typo):
        # 顯示帶有錯字的文本
        highlighted_text = self.highlight_typo_in_text(text, typo)
        self.text_label.setText(highlighted_text)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Ui_Game_Start()
    window.show()
    app.exec_()
