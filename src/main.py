#!/usr/bin/env python3

import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtGui import QFontMetrics, QFont
from PyQt6.QtCore import QSize
from main_menu import MainMenu
from player_list import PlayerListApp
from team_list import TeamListApp
from league_leaders import LeagueLeadersPage
from styles import MAIN_STYLESHEET


if __name__ == '__main__':
    app = QApplication(sys.argv)
    from PyQt6.QtGui import QIcon
    import os
    
    # Set the application icon for taskbar and all windows
    # When bundled with PyInstaller, use sys._MEIPASS to find resources
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        icon_path = os.path.join(sys._MEIPASS, 'assets', 'bball_new.ico')
    else:
        # Running as script
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/bball_new.ico')
    
    app.setWindowIcon(QIcon(icon_path))

    # Apply modern stylesheet
    app.setStyleSheet(MAIN_STYLESHEET)

    # Get base unit for relative sizing
    font = QFont()
    font.setPointSize(14)
    metrics = QFontMetrics(font)
    base_unit = metrics.height()

    stacked_widget = QStackedWidget()

    # Create pages
    main_menu = MainMenu(stacked_widget)
    player_list = PlayerListApp(stacked_widget)
    league_leaders = LeagueLeadersPage(stacked_widget)
    team_list = TeamListApp(stacked_widget)

    # Add pages to stack
    stacked_widget.addWidget(main_menu)         # index 0
    stacked_widget.addWidget(player_list)       # index 1
    stacked_widget.addWidget(league_leaders)   # index 2
    stacked_widget.addWidget(team_list)        # index 3

    # Configure and show window with relative sizing
    stacked_widget.setCurrentIndex(0)
    stacked_widget.setWindowTitle('Basketball App')
    # Set window icon explicitly
    stacked_widget.setWindowIcon(QIcon(icon_path))
    # Use relative sizing: ~28em width x ~35em height
    stacked_widget.resize(QSize(int(base_unit * 28), int(base_unit * 35)))
    stacked_widget.show()

    sys.exit(app.exec())

