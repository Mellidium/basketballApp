from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton,
    QTabWidget, QWidget, QProgressDialog, QComboBox, QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from nbaData import get_most_recent_game_stats, get_player_career_stats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from styles import apply_graph_style


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
    dialog.resize(300, 150)
    
    layout = QVBoxLayout()
    
    label = QLabel(f"Select stats type for {player_name}:")
    layout.addWidget(label)
    
    # Career Stats button
    career_btn = QPushButton("Career Stats")
    career_btn.clicked.connect(lambda: show_career_stats(dialog, parent, player_name, player_id))
    layout.addWidget(career_btn)
    
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
        
        # Stats Graph Tab
        if career_data.get('season_totals_regular_season'):
            graph_widget = create_stats_graph_widget(career_data['season_totals_regular_season'], player_name)
            tabs.addTab(graph_widget, "Stats Graph")
        
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


def create_stats_graph_widget(season_data, player_name):
    """Create a widget with a dropdown to select stat and a line graph."""
    widget = QWidget()
    layout = QVBoxLayout()
    
    # Create dropdown and controls
    controls_layout = QHBoxLayout()
    controls_layout.addWidget(QLabel("Select Stat:"))
    
    stat_dropdown = QComboBox()
    
    # Add stat categories that are numeric and meaningful to graph
    stat_categories = [
        ('PTS', 'Points'),
        ('REB', 'Rebounds'),
        ('AST', 'Assists'),
        ('STL', 'Steals'),
        ('BLK', 'Blocks'),
        ('MIN', 'Minutes'),
        ('FG_PCT', 'FG%'),
        ('FG3_PCT', '3P%'),
        ('FT_PCT', 'FT%'),
        ('FG3M', '3PM'),
        ('FTM', 'FTM'),
        ('FGM', 'FGM'),
        ('OREB', 'Off Reb'),
        ('DREB', 'Def Reb'),
        ('TOV', 'Turnovers'),
        ('PF', 'Fouls')
    ]
    
    # Only add stats that exist in the data
    available_stats = []
    if season_data:
        for stat_key, stat_label in stat_categories:
            if stat_key in season_data[0]:
                stat_dropdown.addItem(stat_label, stat_key)
                available_stats.append((stat_key, stat_label))
    
    controls_layout.addWidget(stat_dropdown)
    controls_layout.addStretch(1)
    layout.addLayout(controls_layout)
    
    # Create matplotlib figure and canvas
    figure = Figure(figsize=(10, 6))
    canvas = FigureCanvas(figure)
    layout.addWidget(canvas)
    
    # Create annotation for hover tooltip
    annot = None
    
    def update_graph():
        """Update the graph based on selected stat."""
        nonlocal annot
        stat_key = stat_dropdown.currentData()
        stat_label = stat_dropdown.currentText()
        
        if not stat_key or not season_data:
            return
        
        # Aggregate data by season (handle multiple teams in same season)
        # Data comes in PerGame format, so we need to convert to totals first
        season_dict = {}
        
        for season in season_data:
            season_id = season.get('SEASON_ID', '')
            if not season_id:
                continue
            
            # Initialize season if not seen before
            if season_id not in season_dict:
                season_dict[season_id] = {
                    'games': 0,
                    'totals': {}
                }
            
            # Accumulate data for this season
            gp = season.get('GP', 0)
            if gp:
                season_dict[season_id]['games'] += gp
                
                # Convert per-game stats to totals by multiplying by GP, then sum
                for key in ['PTS', 'REB', 'AST', 'STL', 'BLK', 'MIN', 'FG3M', 'FTM', 'FGM', 
                           'OREB', 'DREB', 'TOV', 'PF', 'FGA', 'FG3A', 'FTA']:
                    if key in season:
                        value = season.get(key, 0)
                        if value is not None:
                            # Convert per-game to total by multiplying by games played
                            total_value = value * gp
                            season_dict[season_id]['totals'][key] = season_dict[season_id]['totals'].get(key, 0) + total_value
        
        # Extract seasons and stat values
        seasons = []
        values = []
        full_season_labels = []
        
        # Sort seasons chronologically
        sorted_seasons = sorted(season_dict.keys())
        
        for season_id in sorted_seasons:
            season_year = season_id.split('-')[0] if '-' in season_id else season_id
            total_games = season_dict[season_id]['games']
            
            if total_games == 0:
                continue
            
            # Calculate the stat value
            stat_value = None
            
            # For percentage stats, recalculate from totals
            if stat_key == 'FG_PCT':
                fgm = season_dict[season_id]['totals'].get('FGM', 0)
                fga = season_dict[season_id]['totals'].get('FGA', 0)
                if fga > 0:
                    stat_value = fgm / fga
            elif stat_key == 'FG3_PCT':
                fg3m = season_dict[season_id]['totals'].get('FG3M', 0)
                fg3a = season_dict[season_id]['totals'].get('FG3A', 0)
                if fg3a > 0:
                    stat_value = fg3m / fg3a
            elif stat_key == 'FT_PCT':
                ftm = season_dict[season_id]['totals'].get('FTM', 0)
                fta = season_dict[season_id]['totals'].get('FTA', 0)
                if fta > 0:
                    stat_value = ftm / fta
            else:
                # For counting stats, convert total back to per-game average
                total_stat = season_dict[season_id]['totals'].get(stat_key, 0)
                stat_value = total_stat / total_games if total_games > 0 else 0
            
            if stat_value is not None:
                seasons.append(season_year)
                full_season_labels.append(season_id)
                values.append(float(stat_value))
        
        # Clear the figure and create new plot
        figure.clear()
        ax = figure.add_subplot(111)
        
        if seasons and values:
            # Apply modern styling to the graph
            apply_graph_style(figure, ax)
            
            # Create the line plot with modern styling
            line, = ax.plot(seasons, values, marker='o', linewidth=2.5, markersize=8, 
                           linestyle='-', color='#89b4fa', markerfacecolor='#89b4fa', 
                           markeredgecolor='#cdd6f4', markeredgewidth=1, picker=5)
            
            # Customize the plot
            ax.set_xlabel('Season', fontsize=12, fontweight='600', color='#cdd6f4')
            ax.set_ylabel(stat_label, fontsize=12, fontweight='600', color='#cdd6f4')
            ax.set_title(f'{player_name} - {stat_label} by Season', fontsize=14, fontweight='bold', 
                        color='#cdd6f4', pad=15)
            
            # Rotate x-axis labels for better readability
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Create annotation object for hover tooltip with modern styling
            annot = ax.annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                              bbox=dict(boxstyle="round,pad=0.7", fc="#89b4fa", alpha=0.95, 
                                       edgecolor="#cdd6f4", linewidth=2),
                              arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2",
                                            color="#cdd6f4", linewidth=1.5),
                              fontsize=10, fontweight='bold', color='#1e1e2e')
            annot.set_visible(False)
            
            def hover(event):
                """Handle mouse hover events."""
                if event.inaxes == ax:
                    # Check if mouse is near any data point
                    for i, (x, y) in enumerate(zip(range(len(seasons)), values)):
                        # Get display coordinates of the data point
                        display_coords = ax.transData.transform((x, y))
                        mouse_coords = (event.x, event.y)
                        
                        # Calculate distance from mouse to point
                        distance = ((display_coords[0] - mouse_coords[0])**2 + 
                                  (display_coords[1] - mouse_coords[1])**2)**0.5
                        
                        # If mouse is within 10 pixels of a point
                        if distance < 15:
                            # Format the value based on stat type
                            if stat_key.endswith('_PCT'):
                                formatted_value = f"{y:.3f}"
                            elif stat_key == 'MIN':
                                formatted_value = f"{y:.1f}"
                            else:
                                formatted_value = f"{y:.1f}" if isinstance(y, float) else str(y)
                            
                            # Update annotation
                            annot.xy = (x, y)
                            text = f"{full_season_labels[i]}\n{stat_label}: {formatted_value}"
                            annot.set_text(text)
                            annot.set_visible(True)
                            canvas.draw_idle()
                            return
                    
                    # If not near any point, hide annotation
                    if annot.get_visible():
                        annot.set_visible(False)
                        canvas.draw_idle()
            
            # Connect hover event
            canvas.mpl_connect('motion_notify_event', hover)
            
            # Add some padding
            figure.tight_layout()
        else:
            ax.text(0.5, 0.5, 'No data available for this stat', 
                   ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
        
        canvas.draw()
    
    # Connect dropdown to update function
    stat_dropdown.currentIndexChanged.connect(update_graph)
    
    # Initial graph
    if available_stats:
        update_graph()
    
    widget.setLayout(layout)
    return widget
