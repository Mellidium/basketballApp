#!/Users/kevinwhitney/Documents/basketballApp/.venv/bin/python

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QLabel, QStackedWidget
)
from PyQt6.QtCore import Qt
from nbaData import get_active_players, get_player_id_by_name, get_most_recent_game_stats

class PlayerListApp(QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.setWindowTitle('NBA Players')
        self.resize(400, 500)

        self.stacked_widget = stacked_widget
        self.nba_players = get_active_players()
        self.page = 0
        self.page_size = 20

        from PyQt6.QtWidgets import QLineEdit
        self.layout = QVBoxLayout()
        # Top bar for Back button (always present)
        top_bar = QHBoxLayout()
        back_btn = QPushButton('Back')
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(self.go_back)
        top_bar.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        top_bar.addStretch(1)
        self.layout.addLayout(top_bar)

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

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(0)
        else:
            self.close()

    def show_player_game_data(self, item):
        player_name = item.text()
        player_id = get_player_id_by_name(player_name)
        if player_id is not None:
            stats = get_most_recent_game_stats(player_id)
            if stats:
                self.show_stats_popup(player_name, stats)
            else:
                self.show_stats_popup(player_name, "No recent game data found.")
        else:
            self.show_stats_popup(player_name, "Player ID not found.")

    def show_stats_popup(self, player_name, stats):
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{player_name} - Most Recent Game")
        dialog.resize(600, 500)
        layout = QVBoxLayout()
        label = QLabel(f"Stats for {player_name}'s most recent game:")
        layout.addWidget(label)
        if isinstance(stats, str):
            layout.addWidget(QLabel(stats))
        else:
            table = QTableWidget()
            table.setRowCount(len(stats))
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Stat", "Value"])
            table.setMinimumSize(550, 400)
            for i, (k, v) in enumerate(stats.items()):
                table.setItem(i, 0, QTableWidgetItem(str(k)))
                table.setItem(i, 1, QTableWidgetItem(str(v)))
            table.resizeColumnsToContents()
            layout.addWidget(table)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        dialog.setLayout(layout)
        dialog.exec()

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


# Main menu page
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

# Empty League Leaders page
class LeagueLeadersPage(QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()
        # Top bar for Back button (always present)
        top_bar = QHBoxLayout()
        back_btn = QPushButton('Back')
        back_btn.setFixedWidth(80)
        back_btn.clicked.connect(self.go_back)
        top_bar.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        top_bar.addStretch(1)
        layout.addLayout(top_bar)
        label = QLabel('League Leaders (Coming Soon)')
        layout.addWidget(label)
        self.setLayout(layout)

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(0)
        else:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    main_menu = MainMenu(stacked_widget)
    player_list = PlayerListApp(stacked_widget)
    league_leaders = LeagueLeadersPage(stacked_widget)
    stacked_widget.addWidget(main_menu)         # index 0
    stacked_widget.addWidget(player_list)       # index 1
    stacked_widget.addWidget(league_leaders)   # index 2
    stacked_widget.setCurrentIndex(0)
    stacked_widget.setWindowTitle('Basketball App')
    stacked_widget.resize(400, 500)
    stacked_widget.show()
    sys.exit(app.exec())
