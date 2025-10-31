from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt


class MainMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Add title
        title = QLabel('Basketball Stats App')
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #89b4fa;
            padding: 20px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_stats = QPushButton('Stats by Player')
        btn_leaders = QPushButton('League Leaders')
        btn_stats.setFixedSize(250, 60)
        btn_leaders.setFixedSize(250, 60)
        
        layout.addStretch(1)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(30)
        layout.addWidget(btn_stats, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(15)
        layout.addWidget(btn_leaders, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch(1)
        
        btn_stats.clicked.connect(self.show_player_stats)
        btn_leaders.clicked.connect(self.show_league_leaders)
        self.setLayout(layout)

    def show_player_stats(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_league_leaders(self):
        self.stacked_widget.setCurrentIndex(2)
