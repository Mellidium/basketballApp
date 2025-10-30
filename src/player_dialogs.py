from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton,
    QTabWidget, QWidget, QProgressDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from nbaData import get_most_recent_game_stats, get_player_career_stats


class CareerStatsWorker(QThread):
    """Worker thread for loading career stats data."""
    finished = pyqtSignal(dict)
    
    def __init__(self, player_id):
        super().__init__()
        self.player_id = player_id
    
    def run(self):
        """Fetch career stats data in background thread."""
        career_data = get_player_career_stats(self.player_id)
        self.finished.emit(career_data)


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
    """Show career stats using PlayerCareerStats endpoint."""
    selection_dialog.close()
    
    # Show loading dialog
    loading_dialog = QProgressDialog(f"Loading career stats for {player_name}...", None, 0, 0, parent)
    loading_dialog.setWindowTitle("Please Wait")
    loading_dialog.setWindowModality(Qt.WindowModality.WindowModal)
    loading_dialog.setCancelButton(None)
    loading_dialog.setMinimumDuration(0)
    loading_dialog.show()
    
    # Create worker thread
    worker = CareerStatsWorker(player_id)
    
    def on_finished(career_data):
        loading_dialog.close()
        show_career_stats_popup(parent, player_name, career_data)
    
    worker.finished.connect(on_finished)
    worker.start()
    
    # Keep reference to worker to prevent garbage collection
    parent._career_stats_worker = worker


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


def show_career_stats_popup(parent, player_name, career_data):
    """Display career stats in a tabbed dialog with season-by-season and career totals."""
    dialog = QDialog(parent)
    dialog.setWindowTitle(f"{player_name} - Career Stats")
    dialog.resize(900, 600)
    
    layout = QVBoxLayout()
    label = QLabel(f"Career stats for {player_name}:")
    layout.addWidget(label)
    
    # Check if we have any data
    has_data = any(career_data.get(key) for key in career_data.keys())
    
    if not has_data:
        layout.addWidget(QLabel("No career stats available for this player."))
    else:
        # Create tabs for different views
        tabs = QTabWidget()
        
        # Regular Season Stats Tab
        if career_data.get('season_totals_regular_season'):
            season_widget = create_season_stats_table(career_data['season_totals_regular_season'])
            tabs.addTab(season_widget, "Regular Season")
        
        # Career Totals Tab
        if career_data.get('career_totals_regular_season'):
            career_widget = create_career_totals_table(career_data['career_totals_regular_season'])
            tabs.addTab(career_widget, "Career Totals")
        
        # Playoff Stats Tab (if available)
        if career_data.get('season_totals_post_season'):
            playoff_widget = create_season_stats_table(career_data['season_totals_post_season'])
            tabs.addTab(playoff_widget, "Playoffs")
        
        # Playoff Career Totals Tab (if available)
        if career_data.get('career_totals_post_season'):
            playoff_career_widget = create_career_totals_table(career_data['career_totals_post_season'])
            tabs.addTab(playoff_career_widget, "Playoff Totals")
        
        layout.addWidget(tabs)
    
    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dialog.accept)
    layout.addWidget(close_btn)
    
    dialog.setLayout(layout)
    dialog.exec()


def create_season_stats_table(season_data):
    """Create a table widget for season-by-season stats."""
    widget = QWidget()
    layout = QVBoxLayout()
    
    table = QTableWidget()
    table.setRowCount(len(season_data))
    
    if season_data:
        # Define columns to display (most important stats)
        display_columns = ['SEASON_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 
                          'PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT', 'FT_PCT']
        
        # Filter to only include columns that exist in the data
        available_columns = [col for col in display_columns if col in season_data[0]]
        
        table.setColumnCount(len(available_columns))
        table.setHorizontalHeaderLabels(available_columns)
        
        # Populate table
        for i, season in enumerate(season_data):
            for j, col in enumerate(available_columns):
                value = season.get(col, '')
                # Format percentages and floats
                if col.endswith('_PCT') and value:
                    try:
                        value = f"{float(value):.3f}"
                    except (ValueError, TypeError):
                        pass
                elif col == 'MIN' and value:
                    try:
                        value = f"{float(value):.1f}"
                    except (ValueError, TypeError):
                        pass
                table.setItem(i, j, QTableWidgetItem(str(value)))
        
        table.resizeColumnsToContents()
    
    layout.addWidget(table)
    widget.setLayout(layout)
    return widget


def create_career_totals_table(career_data):
    """Create a table widget for career totals."""
    widget = QWidget()
    layout = QVBoxLayout()
    
    if career_data:
        # Career totals usually has just one row
        totals = career_data[0]
        
        table = QTableWidget()
        table.setRowCount(len(totals))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Stat", "Value"])
        
        # Order stats logically
        stat_order = ['GP', 'GS', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF',
                     'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT',
                     'OREB', 'DREB']
        
        # Get all keys, prioritizing the ordered ones
        all_keys = [k for k in stat_order if k in totals] + [k for k in totals.keys() if k not in stat_order]
        
        for i, key in enumerate(all_keys):
            value = totals[key]
            # Format percentages and floats
            if key.endswith('_PCT') and value:
                try:
                    value = f"{float(value):.3f}"
                except (ValueError, TypeError):
                    pass
            elif key == 'MIN' and value:
                try:
                    value = f"{float(value):.1f}"
                except (ValueError, TypeError):
                    pass
            
            table.setItem(i, 0, QTableWidgetItem(str(key)))
            table.setItem(i, 1, QTableWidgetItem(str(value)))
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
    else:
        layout.addWidget(QLabel("No career totals available."))
    
    widget.setLayout(layout)
    return widget
