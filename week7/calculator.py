import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('20253615조희섭')
        self.setFixedSize(360, 500)
        self.expression = ''
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet('background-color: #1C1C1C;')  # 아이폰 다크 배경

        layout = QGridLayout()
        layout.setSpacing(8)
        self.setLayout(layout)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont('Courier', 32))
        self.display.setStyleSheet('color: white; background-color: black; border: none; padding: 20px;')
        layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ('C', 1, 0), ('+/-', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('−', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 1, 2), ('.', 5, 2), ('=', 5, 3)
        ]

        for button_info in buttons:
            label = button_info[0]
            row = button_info[1]
            col = button_info[2]
            rowspan = button_info[3] if len(button_info) > 3 else 1
            colspan = button_info[4] if len(button_info) > 4 else 1

            button = QPushButton(label)
            button.setFont(QFont('Helvetica', 20, QFont.Bold))

            # 색상 지정
            if label in ['÷', '×', '−', '+', '=']:
                color = '#FF9500'
                text_color = 'white'
            elif label in ['C', '+/-', '%']:
                color = '#A5A5A5'
                text_color = 'black'
            else:
                color = '#333333'
                text_color = 'white'

            # 0 버튼만 넓은 타원
            if label == '0':
                button.setStyleSheet(f'''
                    QPushButton {{
                        background-color: {color};
                        color: {text_color};
                        font-size: 20px;
                        border: none;
                        border-radius: 35px;
                        min-width: 140px;
                        min-height: 70px;
                        text-align: left;
                        padding-left: 25px;
                    }}
                ''')
            else:
                button.setStyleSheet(f'''
                    QPushButton {{
                        background-color: {color};
                        color: {text_color};
                        font-size: 20px;
                        border: none;
                        min-width: 70px;
                        min-height: 70px;
                        border-radius: 35px;
                    }}
                ''')

            button.clicked.connect(lambda _, text=label: self.on_click(text))
            layout.addWidget(button, row, col, rowspan, colspan)

    def format_result(self, result, digits=6, max_len=14):
        try:
            float_result = round(float(result), digits)
            result = str(float_result)
            if len(result) > max_len:
                result = result[:max_len] + '...'
            return result
        except:
            return 'Error'

    def on_click(self, text):
        if text == 'C':
            self.expression = ''
            self.display.setText('')
        elif text == '=':
            try:
                expr = self.expression.replace('×', '*').replace('÷', '/').replace('−', '-')
                raw_result = str(eval(expr))
                result = self.format_result(raw_result)
                self.display.setText(result)
                self.expression = result
            except Exception:
                self.display.setText('Error')
                self.expression = ''
        elif text == '+/-':
            if self.expression.startswith('-'):
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
            self.display.setText(self.expression)
        else:
            self.expression += text
            self.display.setText(self.expression)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
