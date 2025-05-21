# Fichier: Synchro_qt_made/main_qt.py
# Description: Point d'entrée de l'application d'interface graphique Qt.

import sys
from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow # Importer notre classe de fenêtre principale

if __name__ == "__main__":
    # Créer l'instance de l'application Qt
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre principale
    main_win = MainWindow()
    main_win.show()

    # Démarrer la boucle d'événements de l'application
    sys.exit(app.exec())
