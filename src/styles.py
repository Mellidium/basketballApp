"""
Modern styling for the Basketball App
"""

# Main application stylesheet
MAIN_STYLESHEET = """
    QWidget {
        background-color: #1e1e2e;
        color: #cdd6f4;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        font-size: 14px;
    }
    
    QMainWindow {
        background-color: #1e1e2e;
    }
    
    QPushButton {
        background-color: #89b4fa;
        color: #1e1e2e;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 14px;
        min-height: 20px;
    }
    
    QPushButton:hover {
        background-color: #b4befe;
    }
    
    QPushButton:pressed {
        background-color: #74c7ec;
    }
    
    QPushButton:disabled {
        background-color: #45475a;
        color: #6c7086;
    }
    
    QLabel {
        color: #cdd6f4;
        font-size: 14px;
        padding: 4px;
    }
    
    QTableWidget {
        background-color: #181825;
        alternate-background-color: #1e1e2e;
        color: #cdd6f4;
        gridline-color: #313244;
        border: 1px solid #313244;
        border-radius: 8px;
        selection-background-color: #89b4fa;
        selection-color: #1e1e2e;
    }
    
    QTableWidget::item {
        padding: 8px;
        border: none;
    }
    
    QTableWidget::item:selected {
        background-color: #89b4fa;
        color: #1e1e2e;
    }
    
    QHeaderView::section {
        background-color: #313244;
        color: #cdd6f4;
        padding: 10px;
        border: none;
        font-weight: bold;
        font-size: 13px;
    }
    
    QHeaderView::section:hover {
        background-color: #45475a;
    }
    
    QScrollBar:vertical {
        background-color: #1e1e2e;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #45475a;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #585b70;
    }
    
    QScrollBar:horizontal {
        background-color: #1e1e2e;
        height: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #45475a;
        border-radius: 6px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #585b70;
    }
    
    QScrollBar::add-line, QScrollBar::sub-line {
        border: none;
        background: none;
    }
    
    QDialog {
        background-color: #1e1e2e;
    }
    
    QTabWidget::pane {
        border: 1px solid #313244;
        border-radius: 8px;
        background-color: #181825;
        padding: 8px;
    }
    
    QTabBar::tab {
        background-color: #313244;
        color: #cdd6f4;
        padding: 10px 20px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
        font-weight: 500;
    }
    
    QTabBar::tab:selected {
        background-color: #89b4fa;
        color: #1e1e2e;
        font-weight: bold;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #45475a;
    }
    
    QComboBox {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #45475a;
        border-radius: 6px;
        padding: 8px 12px;
        min-width: 150px;
        font-size: 14px;
    }
    
    QComboBox:hover {
        border: 1px solid #89b4fa;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #cdd6f4;
        margin-right: 8px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #313244;
        color: #cdd6f4;
        selection-background-color: #89b4fa;
        selection-color: #1e1e2e;
        border: 1px solid #45475a;
        border-radius: 6px;
        padding: 4px;
    }
    
    QProgressDialog {
        background-color: #1e1e2e;
    }
    
    QLineEdit {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #45475a;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
    }
    
    QLineEdit:focus {
        border: 1px solid #89b4fa;
    }
"""

# Matplotlib graph styling
def get_graph_style():
    """Return matplotlib style parameters for graphs"""
    return {
        'figure.facecolor': '#1e1e2e',
        'axes.facecolor': '#181825',
        'axes.edgecolor': '#45475a',
        'axes.labelcolor': '#cdd6f4',
        'axes.titlecolor': '#cdd6f4',
        'axes.grid': True,
        'grid.color': '#313244',
        'grid.linestyle': '--',
        'grid.alpha': 0.5,
        'text.color': '#cdd6f4',
        'xtick.color': '#cdd6f4',
        'ytick.color': '#cdd6f4',
        'line.color': '#89b4fa',
        'line.linewidth': 2.5,
        'lines.markersize': 8,
        'font.size': 11,
        'font.family': 'sans-serif',
    }

def apply_graph_style(fig, ax):
    """Apply modern styling to a matplotlib figure and axes"""
    fig.patch.set_facecolor('#1e1e2e')
    ax.set_facecolor('#181825')
    ax.spines['bottom'].set_color('#45475a')
    ax.spines['top'].set_color('#45475a')
    ax.spines['right'].set_color('#45475a')
    ax.spines['left'].set_color('#45475a')
    ax.tick_params(colors='#cdd6f4', which='both')
    ax.xaxis.label.set_color('#cdd6f4')
    ax.yaxis.label.set_color('#cdd6f4')
    ax.title.set_color('#cdd6f4')
    ax.grid(True, alpha=0.3, linestyle='--', color='#45475a')
