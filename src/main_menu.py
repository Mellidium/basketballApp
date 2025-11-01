from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFontMetrics, QFont


class MainMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        # Get base unit for relative sizing
        font = QFont()
        font.setPointSize(14)
        metrics = QFontMetrics(font)
        base_unit = metrics.height()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(int(base_unit * 1.4))
        layout.setContentsMargins(int(base_unit * 2.8), int(base_unit * 2.8), 
                                 int(base_unit * 2.8), int(base_unit * 2.8))
        
        # Add title
        title = QLabel('Basketball Stats App')
        title.setStyleSheet("""
            font-size: 2em;
            font-weight: bold;
            color: #89b4fa;
            padding: 1.4em;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_stats = QPushButton('Stats by Player')
        btn_teams = QPushButton('Team Stats')
        btn_leaders = QPushButton('League Leaders')
        
        # Use relative sizing based on font metrics
        btn_width = int(base_unit * 17)
        btn_height = int(base_unit * 4.2)
        btn_stats.setMinimumSize(QSize(btn_width, btn_height))
        btn_teams.setMinimumSize(QSize(btn_width, btn_height))
        btn_leaders.setMinimumSize(QSize(btn_width, btn_height))
        
        layout.addStretch(1)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(int(base_unit * 2))
        layout.addWidget(btn_stats, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(int(base_unit))
        layout.addWidget(btn_teams, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(int(base_unit))
        layout.addWidget(btn_leaders, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch(1)
        
        btn_stats.clicked.connect(self.show_player_stats)
        btn_teams.clicked.connect(self.show_team_stats)
        btn_leaders.clicked.connect(self.show_league_leaders)
        self.setLayout(layout)

    def show_player_stats(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_team_stats(self):
        self.stacked_widget.setCurrentIndex(3)

    def show_league_leaders(self):
        self.stacked_widget.setCurrentIndex(2)
