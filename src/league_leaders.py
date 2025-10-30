from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, 
    QTableWidget, QTableWidgetItem, QProgressDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from nbaData import get_league_leaders


class LeagueLeadersWorker(QThread):
    """Worker thread for loading league leaders data."""
    finished = pyqtSignal(list)
    
    def __init__(self, stat_category):
        super().__init__()
        self.stat_category = stat_category
    
    def run(self):
        """Fetch league leaders data in background thread."""
        leaders_data = get_league_leaders(self.stat_category)
        self.finished.emit(leaders_data)


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
        
        # Stat category buttons
        stats_label = QLabel('Select a stat category:')
        layout.addWidget(stats_label)
        
        # Create button grid for stat categories
        button_grid = QHBoxLayout()
        self.stat_categories = {
            'PTS': 'Points',
            'REB': 'Rebounds',
            'AST': 'Assists',
            'STL': 'Steals',
            'BLK': 'Blocks',
            'FG_PCT': 'FG%',
            'FG3_PCT': '3P%',
            'FT_PCT': 'FT%'
        }
        
        # Create buttons for each stat category
        for stat_abbr, stat_name in self.stat_categories.items():
            btn = QPushButton(stat_name)
            btn.clicked.connect(lambda checked, s=stat_abbr: self.load_leaders(s))
            button_grid.addWidget(btn)
        
        layout.addLayout(button_grid)
        
        # Table widget for displaying leaders
        self.table = QTableWidget()
        self.table.setMinimumHeight(400)
        layout.addWidget(self.table)
        
        self.setLayout(layout)

    def load_leaders(self, stat_category):
        """Load and display league leaders for the specified stat category."""
        # Show loading dialog
        self.loading_dialog = QProgressDialog("Loading league leaders...", None, 0, 0, self)
        self.loading_dialog.setWindowTitle("Please Wait")
        self.loading_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.loading_dialog.setCancelButton(None)
        self.loading_dialog.setMinimumDuration(0)
        self.loading_dialog.show()
        
        # Store the stat category for later use
        self.current_stat = stat_category
        
        # Create and start worker thread
        self.worker = LeagueLeadersWorker(stat_category)
        self.worker.finished.connect(self.display_leaders)
        self.worker.start()
    
    def display_leaders(self, leaders_data):
        """Display the loaded leaders data in the table."""
        # Close loading dialog
        if hasattr(self, 'loading_dialog'):
            self.loading_dialog.close()
        
        if not leaders_data:
            self.table.setRowCount(1)
            self.table.setColumnCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("No data available"))
            return
        
        # Display the top 10 leaders
        num_leaders = min(10, len(leaders_data))
        leaders_data = leaders_data[:num_leaders]
        
        # Set up table
        self.table.setRowCount(num_leaders)
        
        # Define columns to display
        display_columns = ['RANK', 'PLAYER', 'TEAM', 'GP', 'MIN', self.current_stat]
        self.table.setColumnCount(len(display_columns))
        self.table.setHorizontalHeaderLabels(display_columns)
        
        # Populate table
        for i, leader in enumerate(leaders_data):
            for j, col in enumerate(display_columns):
                value = leader.get(col, '')
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
        
        self.table.resizeColumnsToContents()

    def go_back(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(0)
        else:
            self.close()
