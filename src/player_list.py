from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics, QFont
from nbaData import get_active_players, get_player_id_by_name
from player_dialogs import show_stats_selection_dialog


class PlayerListApp(QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.setWindowTitle('NBA Players')
        self.resize(400, 500)

        self.stacked_widget = stacked_widget
        self.nba_players = get_active_players()
        self.page = 0
        self.page_size = 20
        
        # Get base unit for relative sizing
        font = QFont()
        font.setPointSize(14)
        metrics = QFontMetrics(font)
        base_unit = metrics.height()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(int(base_unit * 1.4), int(base_unit * 1.4), 
                                       int(base_unit * 1.4), int(base_unit * 1.4))
        self.layout.setSpacing(int(base_unit))
        
        # Top bar for Back button (always present)
        top_bar = QHBoxLayout()
        back_btn = QPushButton('Back')
        back_btn.setMinimumWidth(int(base_unit * 7))
        back_btn.clicked.connect(self.go_back)
        top_bar.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        top_bar.addStretch(1)
        self.layout.addLayout(top_bar)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search players...')
        self.search_bar.setMinimumHeight(int(base_unit * 2.8))
        self.search_bar.textChanged.connect(self.filter_players)
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
        self.list_widget.itemClicked.connect(self.show_player_game_data)

        self.filtered_players = self.nba_players

        # Pagination controls
        self.pagination_layout = QHBoxLayout()
        self.pagination_layout.setSpacing(int(base_unit))
        self.prev_button = QPushButton('Previous')
        self.next_button = QPushButton('Next')
        self.prev_button.setMinimumHeight(int(base_unit * 2.8))
        self.next_button.setMinimumHeight(int(base_unit * 2.8))
        self.page_label = QLabel()
        self.page_label.setStyleSheet("font-weight: bold; font-size: 1em;")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(self.next_button)
        self.layout.addLayout(self.pagination_layout)

        self.setLayout(self.layout)
        self.update_list()

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(0)
        else:
            self.close()

    def show_player_game_data(self, item):
        player_name = item.text()
        player_id = get_player_id_by_name(player_name)
        
        if player_id is None:
            from player_dialogs import show_stats_popup
            show_stats_popup(self, player_name, "Player ID not found.")
            return
        
        # Show selection dialog
        show_stats_selection_dialog(self, player_name, player_id)

    def update_list(self):
        self.list_widget.clear()
        start = self.page * self.page_size
        end = start + self.page_size
        for player in self.filtered_players[start:end]:
            self.list_widget.addItem(player['full_name'])
        total_pages = (len(self.filtered_players) - 1) // self.page_size + 1
        self.page_label.setText(f'Page {self.page + 1} of {total_pages}')
        self.prev_button.setEnabled(self.page > 0)
        self.next_button.setEnabled(end < len(self.filtered_players))

    def filter_players(self, text):
        text = text.lower()
        if text:
            self.filtered_players = [p for p in self.nba_players if text in p['full_name'].lower()]
        else:
            self.filtered_players = self.nba_players
        self.page = 0
        self.update_list()

    def next_page(self):
        if (self.page + 1) * self.page_size < len(self.nba_players):
            self.page += 1
            self.update_list()

    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.update_list()
