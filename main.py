import sys
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QApplication, QGridLayout
from PyQt6.QtGui import QKeySequence, QShortcut
import accessible_output2.outputs.auto

nvda = accessible_output2.outputs.auto.Auto()
button_list = ['Clear', 'Back space', '', 'Exit', '7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '.', '0', '=', '+']

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.result = QLineEdit()
        self.result.setReadOnly(True)
        self.result.setText('0')
        self.result.textChanged.connect(self.talk)
        grid.addWidget(self.result, 0, 0, 1, 4)

        pos = [(row, col) for row in range(1, 6) for col in range(4)]

        for i,b in enumerate(button_list):
            if b=='' : continue
            btn = QPushButton(b)
            btn.setAccessibleName(b)
            btn.clicked.connect(self.calc)
            if b not in ['Clear', 'Back space', 'Exit', '=']:
                shortcut = QShortcut(QKeySequence(b), btn)
            elif b == 'Clear' :
                shortcut = QShortcut(QKeySequence('Delete'), btn)
            elif b == 'Back space' :
                shortcut = QShortcut(QKeySequence('Backspace'), btn)
            elif b == 'Exit' :
                shortcut = QShortcut(QKeySequence('Escape'), btn)
            else :
                shortcut = QShortcut(QKeySequence('Enter'), btn)
            shortcut.activated.connect(btn.click)
            #shortcut.activated.connect(btn.setFocus)
            #btn.setDefault(True)
            name = 'btn'+ str(i)
            btn.setObjectName(name)
            setattr(self, name, btn)
            grid.addWidget(btn, *pos[i])

        self.equal = False
        self.setLayout(grid)
        self.setWindowTitle('Calculator')
        self.resize(240, 240)
        self.setFixedSize(self.size())
        self.show()

    def calc(self):
        btn = self.sender().text()
        value = self.result.text()
        if btn == 'Exit' :exit()

        if self.equal :
            self.equal=False
            if btn not in ['-', '+', '/', '*'] :
                value='0'
        if value == '0' or value == 'Error':
            if btn in ['Clear', 'Back space', '=']: 
                self.result.setText('0')
                return
            self.result.setText(btn)
        else :
            if btn == 'Clear' :
                self.result.setText('0')
                return
            if btn == 'Back space' :
                if len(value) == 1 :
                    self.result.setText('0')
                else:
                    self.result.setText(value[:-1])
                return
            if btn == '=' :
                try:
                    self.result.setText(str(eval(value)))
                    self.equal=True
                except:
                    self.result.setText('Error')
                return
            self.result.setText(value+btn)
            return

    def talk(self):
        nvda.output(self.result.text())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__' :
    main()