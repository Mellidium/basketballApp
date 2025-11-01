from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics, QFont
from nbaData import get_nba_teams, get_team_id_by_name
from team_dialogs import show_team_stats_dialog


class TeamListApp(QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.setWindowTitle('NBA Teams')
        self.resize(400, 500)

        self.stacked_widget = stacked_widget
        self.nba_teams = get_nba_teams()
        
        # Sort teams alphabetically by full name
        self.nba_teams.sort(key=lambda x: x['full_name'])
        
        # Get base unit for relative sizing
        font = QFont()
        font.setPointSize(14)
        metrics = QFontMetrics(font)
        base_unit = metrics.height()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(int(base_unit * 1.4), int(base_unit * 1.4), 
                                       int(base_unit * 1.4), int(base_unit * 1.4))
        self.layout.setSpacing(int(base_unit))

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search teams...')
        self.search_bar.setMinimumHeight(int(base_unit * 2.8))
        self.search_bar.textChanged.connect(self.filter_teams)
        self.layout.addWidget(self.search_bar)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget::item {
                padding: 0.85em;
                border-bottom: 1px solid #313244;
            }
            QListWidget::item:hover {
                background-color: #313244;
            }
            QListWidget::item:selected {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
        """)
        self.layout.addWidget(self.list_widget)
        self.list_widget.itemClicked.connect(self.show_team_stats)

        self.filtered_teams = self.nba_teams

        # Bottom bar for Back button
        bottom_bar = QHBoxLayout()
        back_btn = QPushButton('Back')
        back_btn.setMinimumWidth(int(base_unit * 7))
        back_btn.clicked.connect(self.go_back)
        bottom_bar.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        bottom_bar.addStretch(1)
        self.layout.addLayout(bottom_bar)

        self.setLayout(self.layout)
        self.update_list()

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(0)
        else:
            self.close()

    def show_team_stats(self, item):
        team_name = item.text()
        team_id = get_team_id_by_name(team_name)
        
        if team_id is None:
            # TODO: Show error message
            print(f"Team ID not found for {team_name}")
            return
        
        # Show team stats dialog
        show_team_stats_dialog(self, team_name, team_id)

    def update_list(self):
        self.list_widget.clear()
        for team in self.filtered_teams:
            self.list_widget.addItem(team['full_name'])

    def filter_teams(self, text):
        text = text.lower()
        if text:
            self.filtered_teams = [t for t in self.nba_teams 
                                  if text in t['full_name'].lower() or 
                                  text in t['nickname'].lower() or
                                  text in t['city'].lower()]
        else:
            self.filtered_teams = self.nba_teams
        self.update_list()
