from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton
)
from nbaData import get_most_recent_game_stats


def show_stats_selection_dialog(parent, player_name, player_id):
    """Show dialog to select which type of stats to view."""
    dialog = QDialog(parent)
    dialog.setWindowTitle(f"{player_name} - Select Stats Type")
    dialog.resize(300, 200)
    
    layout = QVBoxLayout()
    
    label = QLabel(f"Select stats type for {player_name}:")
    layout.addWidget(label)
    
    # Career Stats button
    career_btn = QPushButton("Career Stats")
    career_btn.clicked.connect(lambda: show_career_stats(dialog, parent, player_name, player_id))
    layout.addWidget(career_btn)
    
    # Season Stats button
    season_btn = QPushButton("Season Stats")
    season_btn.clicked.connect(lambda: show_season_stats(dialog, parent, player_name, player_id))
    layout.addWidget(season_btn)
    
    # Last Game Stats button
    last_game_btn = QPushButton("Last Game Stats")
    last_game_btn.clicked.connect(lambda: show_last_game_stats(dialog, parent, player_name, player_id))
    layout.addWidget(last_game_btn)
    
    dialog.setLayout(layout)
    dialog.exec()


def show_career_stats(selection_dialog, parent, player_name, player_id):
    """Show career stats (placeholder for now)."""
    selection_dialog.close()
    show_stats_popup(parent, player_name, "Career stats coming soon!")


def show_season_stats(selection_dialog, parent, player_name, player_id):
    """Show season stats (placeholder for now)."""
    selection_dialog.close()
    show_stats_popup(parent, player_name, "Season stats coming soon!")


def show_last_game_stats(selection_dialog, parent, player_name, player_id):
    """Show last game stats (existing functionality)."""
    selection_dialog.close()
    stats = get_most_recent_game_stats(player_id)
    if stats:
        show_stats_popup(parent, player_name, stats)
    else:
        show_stats_popup(parent, player_name, "No recent game data found.")


def show_stats_popup(parent, player_name, stats):
    """Display stats in a popup dialog."""
    dialog = QDialog(parent)
    dialog.setWindowTitle(f"{player_name} - Stats")
    dialog.resize(600, 500)
    layout = QVBoxLayout()
    label = QLabel(f"Stats for {player_name}:")
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
