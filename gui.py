
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem,
    QPushButton, QSizePolicy
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, QSize
import os, sys

class FolderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.tab()
    
    def tab(self):
        layout = QVBoxLayout()
        self.table = QTableWidget(3, 4)
        self.table.setHorizontalHeaderLabels(['Folder Name', 'Status', 'Date Locked', 'Actions'])

        self.table.setItem(0, 0, QTableWidgetItem('Alice'))
        self.table.setItem(0, 1, QTableWidgetItem('Développeur'))
        
        self.table.setItem(1, 0, QTableWidgetItem('Bob'))
        self.table.setItem(1, 1, QTableWidgetItem('Designer'))
        
        self.table.setItem(2, 0, QTableWidgetItem('Charlie'))
        self.table.setItem(2, 1, QTableWidgetItem('Manager'))

        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table)
        self.setLayout(layout)

class AddFolderBtn(QPushButton):
    def __init__(self, icon: QIcon, label: str, parent=None):
        super().__init__(label, parent)
        self.setCheckable(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 16))
        self.setFixedHeight(42)
        #self.setMaximumWidth(700)
        self.setIcon(icon)
        self.setIconSize(QSize(24, 24))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vaultix - Your Folder, Your Fortress")
        self.setMinimumSize(700, 700)
        self._build_()

    @staticmethod
    def _font_(size: int = 13, weight=QFont.Weight.Normal, family: str = "Segoe UI") -> QFont:
        font = QFont(family, size)
        font.setWeight(weight)
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        return font
    
    def _build_(self):
        root = QWidget()
        root.setObjectName('root')
        self.setCentralWidget(root)
        
        title_lbl = QLabel('Vaultix')
        title_lbl.setFont(self._font_(size=16, weight=QFont.Weight.Bold))
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        icon_lbl=QLabel()
        if os.path.exists(icon_path):
            icon_lbl.setPixmap(QIcon(icon_path).pixmap(30, 30))

        container = QHBoxLayout()
        container.setSpacing(2)
        container.addWidget(icon_lbl, alignment=Qt.AlignmentFlag.AlignTop)
        container.addWidget(title_lbl, alignment=Qt.AlignmentFlag.AlignTop)
        container.setContentsMargins(10, 10, 10, 10)
        container.addStretch(2)

        table = FolderTab()
        wrapper = QWidget()
        wrapper.setLayout(container)

        presentation = QVBoxLayout()
        presentation.addWidget(wrapper)
        presentation.addWidget(table)
        
        btn_icon_path = os.path.join(os.path.dirname(__file__), "assets", "add.png")
        btn_icon= QIcon(btn_icon_path) if os.path.exists(btn_icon_path) else QIcon()
        button = AddFolderBtn(btn_icon, 'Lock New Folder...')

        maker = QLabel('v1.0.1 Made with ❤️ by Dany-py')
        maker.setFont(self._font_(size=10, weight=QFont.Weight.Normal))

        presentation.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        presentation.addWidget(maker, alignment=Qt.AlignmentFlag.AlignRight)
        presentation.setContentsMargins(50, 0, 50, 20)
        presentation.setSpacing(0)

        root.setLayout(presentation)

def main():
    app = QApplication(sys.argv)

    icon_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()