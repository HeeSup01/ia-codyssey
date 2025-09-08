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
        self.setStyleSheet('background-color: #1C1C1C;')
        layout = QGridLayout()
        layout.setSpacing(8)
        self.setLayout(layout)
        self.create_display(layout)
        self.create_buttons(layout)

    def create_display(self, layout):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont('Courier', 32))
        self.display.setStyleSheet('color: white; background-color: black; border: none; padding: 20px;')
        layout.addWidget(self.display, 0, 0, 1, 4)

    def create_buttons(self, layout):
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
            color, text_color = self.get_button_colors(label)
            style = self.get_button_style(label, color, text_color)
            button.setStyleSheet(style)
            button.clicked.connect(lambda _, text=label: self.on_click(text))
            layout.addWidget(button, row, col, rowspan, colspan)

    def get_button_colors(self, label):
        if label in ['÷', '×', '−', '+', '=']:
            return '#FF9500', 'white'
        elif label in ['C', '+/-', '%']:
            return '#A5A5A5', 'black'
        else:
            return '#333333', 'white'

    def get_button_style(self, label, color, text_color):
        if label == '0':
            return f'''
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
            '''
        else:
            return f'''
                QPushButton {{
                    background-color: {color};
                    color: {text_color};
                    font-size: 20px;
                    border: none;
                    min-width: 70px;
                    min-height: 70px;
                    border-radius: 35px;
                }}
            '''

    def format_result(self, result, digits=6, max_len=14):
        try:
            float_result = round(float(result), digits)
            result = str(float_result)
            self.adjust_font_size(len(result))
            if len(result) > max_len:
                result = result[:max_len] + '...'
            return result
        except:
            return 'Error'

    def adjust_font_size(self, length):
        size = 32
        if length > 12:
            size = 24
        if length > 16:
            size = 18
        self.display.setFont(QFont('Courier', size))

    def on_click(self, text):
        if text == 'C':
            self.reset()
        elif text == '=':
            self.equal()
        elif text == '+/-':
            self.negative_positive()
        elif text == '%':
            self.percent()
        else:
            if text == '.' and '.' in self.expression.split()[-1]:
                return
            self.expression += text
            self.display.setText(self.expression)

    def reset(self):
        self.expression = ''
        self.display.setText('')

    def negative_positive(self):
        if self.expression.startswith('-'):
            self.expression = self.expression[1:]
        else:
            self.expression = '-' + self.expression
        self.display.setText(self.expression)

    def percent(self):
        try:
            value = float(self.expression)
            self.expression = str(value / 100)
            self.display.setText(self.expression)
        except:
            self.display.setText('Error')
            self.expression = ''

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError
        return a / b

    def equal(self):
        try:
            expr = self.expression.replace('×', '*').replace('÷', '/').replace('−', '-')
            result = eval(expr)
            if result == float('inf') or result == float('-inf'):
                raise ZeroDivisionError
            result = self.format_result(result)
            self.display.setText(result)
            self.expression = result
        except ZeroDivisionError:
            self.display.setText('Cannot divide by zero')
            self.expression = ''
        except Exception:
            self.display.setText('Error')
            self.expression = ''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
