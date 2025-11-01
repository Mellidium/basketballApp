from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTabWidget, QWidget, 
    QProgressDialog, QComboBox, QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from nbaData import get_team_shot_locations
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Rectangle, Arc, Polygon
from styles import apply_graph_style


class TeamShotDataWorker(QThread):
    """Worker thread for loading team shot location data."""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, team_id, season):
        super().__init__()
        self.team_id = team_id
        self.season = season
        self._is_cancelled = False
    
    def cancel(self):
        """Cancel the worker thread."""
        self._is_cancelled = True
    
    def run(self):
        """Fetch team shot data in background thread."""
        try:
            if self._is_cancelled:
                return
            shot_data = get_team_shot_locations(self.team_id, self.season)
            if not self._is_cancelled:
                self.finished.emit(shot_data)
        except Exception as e:
            if not self._is_cancelled:
                self.error.emit(str(e))


def show_team_stats_dialog(parent, team_name, team_id):
    """Show team stats dialog with tabs for different stat types."""
    dialog = QDialog(parent)
    dialog.setWindowTitle(f"{team_name} - Team Stats")
    dialog.resize(1200, 800)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(15, 15, 15, 15)
    
    label = QLabel(f"Team stats for {team_name}:")
    label.setStyleSheet("font-size: 1.1em; font-weight: bold; padding: 0.5em 0;")
    layout.addWidget(label)
    
    # Create tabs for different views
    tabs = QTabWidget()
    
    # Shot Location Tab
    shot_location_widget = create_shot_location_widget(team_id, team_name, dialog)
    tabs.addTab(shot_location_widget, "Shot Locations")
    
    # TODO: Add more tabs (Team Stats, Lineup Stats, etc.)
    
    layout.addWidget(tabs)
    
    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dialog.accept)
    layout.addWidget(close_btn)
    
    dialog.setLayout(layout)
    dialog.exec()


def create_shot_location_widget(team_id, team_name, parent_dialog):
    """Create a widget with season selector and shot location visualization."""
    widget = QWidget()
    layout = QVBoxLayout()
    
    # Season selector
    controls_layout = QHBoxLayout()
    controls_layout.addWidget(QLabel("Select Season:"))
    
    season_dropdown = QComboBox()
    # Add recent seasons
    current_year = 2025
    for year in range(current_year, current_year - 10, -1):
        season_str = f"{year-1}-{str(year)[-2:]}"
        season_dropdown.addItem(season_str)
    
    controls_layout.addWidget(season_dropdown)
    controls_layout.addStretch(1)
    layout.addLayout(controls_layout)
    
    # Create matplotlib figure and canvas for the court
    figure = Figure(figsize=(12, 8), tight_layout=True)
    canvas = FigureCanvas(figure)
    canvas.setMinimumSize(700, 600)
    layout.addWidget(canvas)
    
    # Store reference to loading dialog and worker
    loading_refs = {'dialog': None, 'worker': None}
    
    def update_shot_chart():
        """Update the shot chart based on selected season."""
        season = season_dropdown.currentText()
        
        # Show loading dialog on the widget itself (will appear centered on the dialog)
        loading_dialog = QProgressDialog(f"Loading shot data for {season}...", "Cancel", 0, 0, widget)
        loading_dialog.setWindowTitle("Please Wait")
        loading_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        loading_dialog.setMinimumDuration(0)
        loading_dialog.show()
        loading_refs['dialog'] = loading_dialog
        
        # Create worker thread
        worker = TeamShotDataWorker(team_id, season)
        loading_refs['worker'] = worker
        
        def on_finished(shot_data):
            if loading_refs['dialog']:
                loading_refs['dialog'].close()
            draw_shot_chart(figure, canvas, shot_data, team_name, season)
        
        def on_error(error_msg):
            if loading_refs['dialog']:
                loading_refs['dialog'].close()
            print(f"Error loading shot data: {error_msg}")
            # Draw empty court with error message
            draw_shot_chart(figure, canvas, {}, team_name, season, error_msg)
        
        def on_cancelled():
            """Handle cancellation of the loading process."""
            if loading_refs['worker']:
                loading_refs['worker'].cancel()
                loading_refs['worker'].quit()
                loading_refs['worker'].wait()
            if loading_refs['dialog']:
                loading_refs['dialog'].close()
            # Draw empty court with cancellation message
            draw_shot_chart(figure, canvas, {}, team_name, season, "Data loading was cancelled")
        
        # Connect cancel button
        loading_dialog.canceled.connect(on_cancelled)
        
        worker.finished.connect(on_finished)
        worker.error.connect(on_error)
        worker.start()
    
    # Connect dropdown to update function
    season_dropdown.currentIndexChanged.connect(update_shot_chart)
    
    # Initial load
    update_shot_chart()
    
    widget.setLayout(layout)
    return widget


def draw_basketball_court(ax):
    """Draw an NBA basketball court on the given axes using dark theme colors."""
    # Court dimensions (in feet, half court only)
    # We'll draw half court since shot data is typically shown that way
    
    # Colors matching the app theme - darker background, lighter lines
    court_color = '#181825'  # Darker background matching table color
    line_color = '#45475a'   # Subtle gray for court lines
    accent_color = '#6c7086' # Slightly lighter for key elements
    
    ax.set_facecolor(court_color)
    
    # Create the basketball hoop
    hoop = Circle((0, 0), radius=0.75, linewidth=2, color=accent_color, fill=False)
    ax.add_patch(hoop)
    
    # Backboard
    backboard = Rectangle((-3, -0.75), 6, 0.1, linewidth=2, edgecolor=accent_color, facecolor=accent_color)
    ax.add_patch(backboard)
    
    # The paint (the key/lane)
    outer_box = Rectangle((-8, -0.75), 16, 19, linewidth=2, edgecolor=line_color, fill=False)
    ax.add_patch(outer_box)
    
    # Inner box (free throw lane)
    inner_box = Rectangle((-6, -0.75), 12, 19, linewidth=2, edgecolor=line_color, fill=False)
    ax.add_patch(inner_box)
    
    # Free throw circle (top)
    top_free_throw = Arc((0, 19 - 0.75), 12, 12, theta1=0, theta2=180, linewidth=2, color=line_color, fill=False)
    ax.add_patch(top_free_throw)
    
    # Free throw circle (bottom - dashed)
    bottom_free_throw = Arc((0, 19 - 0.75), 12, 12, theta1=180, theta2=0, linewidth=2, color=line_color, 
                            fill=False, linestyle='dashed')
    ax.add_patch(bottom_free_throw)
    
    # Restricted area (4-foot arc under basket)
    restricted = Arc((0, 0), 8, 8, theta1=0, theta2=180, linewidth=2, color=line_color, fill=False)
    ax.add_patch(restricted)
    
    # Three-point line
    # NBA three-point line is 23.75 feet from the hoop (22 feet in corners)
    # Arc portion
    three_point_arc = Arc((0, 0), 47.5, 47.5, theta1=0, theta2=180, linewidth=2, color=line_color)
    ax.add_patch(three_point_arc)
    
    # Three-point line straight sections (corners)
    # The arc starts at about 14 feet from center on each side
    corner_three_left = Rectangle((-25, -0.75), 0.1, 14, linewidth=2, edgecolor=line_color, facecolor=line_color)
    corner_three_right = Rectangle((25, -0.75), 0.1, 14, linewidth=2, edgecolor=line_color, facecolor=line_color)
    ax.add_patch(corner_three_left)
    ax.add_patch(corner_three_right)
    
    # Half-court line (top of our visible court)
    half_court = Rectangle((-25, 47 - 0.75), 50, 0.1, linewidth=2, edgecolor=line_color, facecolor=line_color)
    ax.add_patch(half_court)
    
    # Side lines
    left_line = Rectangle((-25, -0.75), 0.1, 47.75, linewidth=2, edgecolor=line_color, facecolor=line_color)
    right_line = Rectangle((25, -0.75), 0.1, 47.75, linewidth=2, edgecolor=line_color, facecolor=line_color)
    ax.add_patch(left_line)
    ax.add_patch(right_line)
    
    # Center court circle (partial, at half court)
    center_circle = Circle((0, 47 - 0.75), radius=6, linewidth=2, color=line_color, fill=False)
    ax.add_patch(center_circle)
    
    # Set axis limits and properties
    ax.set_xlim(-30, 30)
    ax.set_ylim(-5, 50)
    ax.set_aspect('equal')
    ax.axis('off')


def draw_shot_chart(figure, canvas, shot_data, team_name, season, error_msg=None):
    """Draw the shot chart with data visualization."""
    figure.clear()
    ax = figure.add_subplot(111)
    
    # Draw the court
    draw_basketball_court(ax)
    
    if error_msg:
        # Show error message
        ax.text(0, 25, f"Error loading data:\n{error_msg}", 
               ha='center', va='center', fontsize=12, color='#f38ba8',
               bbox=dict(boxstyle='round', facecolor='#1e1e2e', edgecolor='#f38ba8', linewidth=2))
    elif shot_data and shot_data.get('shot_area'):
        # Visualize shot data on the court
        shot_areas = shot_data['shot_area']
        
        # Define approximate court positions for each shot area
        # Format: area_name -> (x, y) center position on court
        area_positions = {
            'Restricted Area': (0, 3),
            'In The Paint (Non-RA)': (0, 10),
            'Mid-Range': (0, 18),
            'Left Corner 3': (-22, 3),
            'Right Corner 3': (22, 3),
            'Above the Break 3': (0, 25),
            'Backcourt': (0, 47)
        }
        
        # Get FG% for color mapping
        max_fgpct = 0
        min_fgpct = 1
        for area in shot_areas:
            fg_pct = area.get('FG_PCT', 0)
            if fg_pct:
                max_fgpct = max(max_fgpct, fg_pct)
                min_fgpct = min(min_fgpct, fg_pct)
        
        # Plot each area
        for area in shot_areas:
            area_name = area.get('GROUP_VALUE', '')
            fgm = area.get('FGM', 0)
            fga = area.get('FGA', 0)
            fg_pct = area.get('FG_PCT', 0)
            
            if area_name in area_positions and fga > 0:
                x, y = area_positions[area_name]
                
                # Color based on FG% (better shooting = more blue/green)
                if fg_pct >= 0.40:
                    color = '#a6e3a1'  # Green for good shooting
                    alpha = 0.7
                elif fg_pct >= 0.35:
                    color = '#89b4fa'  # Blue for average
                    alpha = 0.6
                else:
                    color = '#f38ba8'  # Red for poor shooting
                    alpha = 0.5
                
                # Size based on attempts
                size = min(fga * 30, 2000)  # Scale but cap the size
                
                # Plot circle for this area
                ax.scatter(x, y, s=size, c=color, alpha=alpha, edgecolors='#cdd6f4', linewidth=2)
                
                # Add text label with stats
                label_text = f"{area_name}\n{fgm}/{fga} ({fg_pct:.1%})"
                ax.text(x, y, label_text, ha='center', va='center', 
                       fontsize=8, fontweight='bold', color='#1e1e2e',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.8, edgecolor='#cdd6f4'))
        
        # Add legend
        legend_text = (
            f"{team_name} - {season}\n"
            f"Circle size = attempts\n"
            f"Green = Good FG% (≥40%)\n"
            f"Blue = Average FG% (35-40%)\n"
            f"Red = Below Average FG% (<35%)"
        )
        ax.text(-28, 42, legend_text, fontsize=9, color='#cdd6f4',
               bbox=dict(boxstyle='round', facecolor='#181825', edgecolor='#89b4fa', linewidth=2, alpha=0.9),
               verticalalignment='top')
    else:
        # No data available
        ax.text(0, 25, "No shot location data available for this season", 
               ha='center', va='center', fontsize=12, color='#cdd6f4',
               bbox=dict(boxstyle='round', facecolor='#181825', edgecolor='#89b4fa', linewidth=2))
    
    # Title
    ax.set_title(f"{team_name} Shot Locations - {season}", 
                fontsize=14, fontweight='bold', color='#cdd6f4', pad=10)
    
    figure.tight_layout(pad=1.5)
    canvas.draw()
