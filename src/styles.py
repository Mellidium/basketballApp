"""
Modern styling for the Basketball App
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontMetrics, QFont

def get_scale_factor():
    """Get the DPI scale factor for the current screen"""
    app = QApplication.instance()
    if app:
        screen = app.primaryScreen()
        return screen.logicalDotsPerInch() / 96.0  # 96 DPI is the standard baseline
    return 1.0

def get_base_unit():
    """Get base unit for scaling (em units based on font size)"""
    font = QFont()
    font.setPointSize(14)
    metrics = QFontMetrics(font)
    return metrics.height()  # Use font height as base unit

# Main application stylesheet - using em/ex units for relative sizing
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
        padding: 0.7em 1.4em;
        border-radius: 0.4em;
        font-weight: bold;
        font-size: 1em;
        min-height: 1.4em;
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
        font-size: 1em;
        padding: 0.3em;
    }
    
    QTableWidget {
        background-color: #181825;
        alternate-background-color: #1e1e2e;
        color: #cdd6f4;
        gridline-color: #313244;
        border: 1px solid #313244;
        border-radius: 0.6em;
        selection-background-color: #89b4fa;
        selection-color: #1e1e2e;
    }
    
    QTableWidget::item {
        padding: 0.6em;
        border: none;
    }
    
    QTableWidget::item:selected {
        background-color: #89b4fa;
        color: #1e1e2e;
    }
    
    QHeaderView::section {
        background-color: #313244;
        color: #cdd6f4;
        padding: 0.7em;
        border: none;
        font-weight: bold;
        font-size: 0.95em;
    }
    
    QHeaderView::section:hover {
        background-color: #45475a;
    }
    
    QScrollBar:vertical {
        background-color: #1e1e2e;
        width: 0.85em;
        border-radius: 0.4em;
    }
    
    QScrollBar::handle:vertical {
        background-color: #45475a;
        border-radius: 0.4em;
        min-height: 1.4em;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #585b70;
    }
    
    QScrollBar:horizontal {
        background-color: #1e1e2e;
        height: 0.85em;
        border-radius: 0.4em;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #45475a;
        border-radius: 0.4em;
        min-width: 1.4em;
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
        border-radius: 0.6em;
        background-color: #181825;
        padding: 0.6em;
    }
    
    QTabBar::tab {
        background-color: #313244;
        color: #cdd6f4;
        padding: 0.7em 1.4em;
        border-top-left-radius: 0.4em;
        border-top-right-radius: 0.4em;
        margin-right: 0.15em;
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
        border-radius: 0.4em;
        padding: 0.6em 0.85em;
        min-width: 10em;
        font-size: 1em;
    }
    
    QComboBox:hover {
        border: 1px solid #89b4fa;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 2.1em;
    }
    
    QComboBox::down-arrow {
        image: none;
        border-left: 0.35em solid transparent;
        border-right: 0.35em solid transparent;
        border-top: 0.35em solid #cdd6f4;
        margin-right: 0.6em;
    }
    
    QComboBox QAbstractItemView {
        background-color: #313244;
        color: #cdd6f4;
        selection-background-color: #89b4fa;
        selection-color: #1e1e2e;
        border: 1px solid #45475a;
        border-radius: 0.4em;
        padding: 0.3em;
    }
    
    QProgressDialog {
        background-color: #1e1e2e;
    }
    
    QLineEdit {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #45475a;
        border-radius: 0.4em;
        padding: 0.6em 0.85em;
        font-size: 1em;
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
