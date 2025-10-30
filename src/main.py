#!/Users/kevinwhitney/Documents/basketballApp/.venv/bin/python

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from nbaData import get_active_players, get_player_id_by_name, get_most_recent_game_stats

class PlayerListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NBA Players')
        self.resize(400, 500)

        self.nba_players = get_active_players()
        self.page = 0
        self.page_size = 20

        from PyQt6.QtWidgets import QLineEdit
        self.layout = QVBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search players...')
        self.search_bar.textChanged.connect(self.filter_players)
        self.layout.addWidget(self.search_bar)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        self.list_widget.itemClicked.connect(self.show_player_game_data)

        self.filtered_players = self.nba_players

        # Pagination controls
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton('Previous')
        self.next_button = QPushButton('Next')
        self.page_label = QLabel()
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(self.next_button)
        self.layout.addLayout(self.pagination_layout)

        self.setLayout(self.layout)
        self.update_list()

    def show_player_game_data(self, item):
        player_name = item.text()
        player_id = get_player_id_by_name(player_name)
        if player_id is not None:
            stats = get_most_recent_game_stats(player_id)
            if stats:
                stats_str = '\n'.join([f"{k}: {v}" for k, v in stats.items()])
                self.show_stats_popup(player_name, stats_str)
            else:
                self.show_stats_popup(player_name, "No recent game data found.")
        else:
            self.show_stats_popup(player_name, "Player ID not found.")

    def show_stats_popup(self, player_name, stats_str):
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle(f"{player_name} - Most Recent Game")
        msg.setText(stats_str)
        msg.exec()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlayerListApp()
    window.show()
    sys.exit(app.exec())
