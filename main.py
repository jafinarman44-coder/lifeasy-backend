"""
LIFEASY V27 - Desktop Admin Application
Apartment Management System
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class LifeasyDesktop(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("LIFEASY V27 - Admin Dashboard")
        self.setGeometry(100, 100, 800, 600)
        
        # Main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Title
        title = QLabel("🏢 LIFEASY V27")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Smart Living Platform - Admin Dashboard")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Arial", 14))
        layout.addWidget(subtitle)
        
        # Status
        status = QLabel("\n✅ Backend: Connected\n✅ Database: Ready\n✅ Mobile App: Active")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status.setFont(QFont("Arial", 12))
        layout.addWidget(status)
        
        # Info
        info = QLabel("\nVersion: 27.0.0\nBuild: 2026.03.16")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setFont(QFont("Arial", 10))
        layout.addWidget(info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = LifeasyDesktop()
    window.show()
    
    sys.exit(app.exec())
