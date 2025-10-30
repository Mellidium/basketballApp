from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt


class MainMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_stats = QPushButton('Stats by Player')
        btn_leaders = QPushButton('League Leaders')
        btn_stats.setFixedSize(200, 50)
        btn_leaders.setFixedSize(200, 50)
        layout.addStretch(1)
        layout.addWidget(btn_stats, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(btn_leaders, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch(1)
        btn_stats.clicked.connect(self.show_player_stats)
        btn_leaders.clicked.connect(self.show_league_leaders)
        self.setLayout(layout)

    def show_player_stats(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_league_leaders(self):
        self.stacked_widget.setCurrentIndex(2)
