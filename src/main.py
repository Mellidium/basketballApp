#!/Users/kevinwhitney/Documents/basketballApp/.venv/bin/python

import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from main_menu import MainMenu
from player_list import PlayerListApp
from league_leaders import LeagueLeadersPage


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    
    # Create pages
    main_menu = MainMenu(stacked_widget)
    player_list = PlayerListApp(stacked_widget)
    league_leaders = LeagueLeadersPage(stacked_widget)
    
    # Add pages to stack
    stacked_widget.addWidget(main_menu)         # index 0
    stacked_widget.addWidget(player_list)       # index 1
    stacked_widget.addWidget(league_leaders)   # index 2
    
    # Configure and show window
    stacked_widget.setCurrentIndex(0)
    stacked_widget.setWindowTitle('Basketball App')
    stacked_widget.resize(400, 500)
    stacked_widget.show()
    
    sys.exit(app.exec())

