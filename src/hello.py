#!/Users/kevinwhitney/Documents/basketballApp/.venv/bin/python

import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Hello World App')
layout = QVBoxLayout()
label = QLabel('Hello, World!')
layout.addWidget(label)
window.setLayout(layout)
window.resize(300, 100)
window.show()

sys.exit(app.exec())
