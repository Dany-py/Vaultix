
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem,
    QPushButton, QSizePolicy, QDialog,
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, QSize
import os, sys
from secret import lock_folder
from verify import restore_folder
from database import load_data

class AddFolderBtn(QPushButton):
    def __init__(self, icon: QIcon, label: str, parent=None):
        super().__init__(label, parent)
        self.setCheckable(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 16))
        self.setFixedHeight(42)
        self.setIcon(icon)
        self.setIconSize(QSize(24, 24))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

class Modal(QDialog):
    def __init__(self, lbl: str, btn_lbl: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter your folder path")
        self.resize(300, 150)

        self.path_input = QLineEdit()
        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.error_lbl = QLabel("")
        self.error_lbl.setStyleSheet("color: red;")
        self.error_lbl.setVisible(False)

        if lbl == 'Lock new folder' and btn_lbl == 'Lock this path':
            self.cf_pwd_input = QLineEdit()
            self.cf_pwd_input.setEchoMode(QLineEdit.EchoMode.Password)

        if lbl == 'Lock new folder' and btn_lbl == 'Lock this path':
            self.path_input.setPlaceholderText('Paste or write the path you want to keep secret:')
            self.pwd_input.setPlaceholderText('Lock password')
            self.cf_pwd_input.setPlaceholderText('Confirm password')
        else:
            self.path_input.setPlaceholderText('Paste or write the path you want to restore:')
            self.pwd_input.setPlaceholderText('Locked password')
            
        layout = QVBoxLayout()
        label = QLabel(lbl)
        button = QPushButton(btn_lbl)
        button.clicked.connect(self.accept)

        layout.addWidget(label)
        layout.addWidget(self.error_lbl)
        layout.addWidget(self.path_input)
        layout.addWidget(self.pwd_input)

        if lbl == 'Lock new folder' and btn_lbl == 'Lock this path':
            layout.addWidget(self.cf_pwd_input)

        layout.addWidget(button)
        self.setLayout(layout)
    
    def get_input_text(self, input: QLineEdit):
        return input.text()
    
    def show_error(self, message: str):
        self.error_lbl.setText(message)
        self.error_lbl.setVisible(True)
    
    def clear_error(self):
        self.error_lbl.setText("")
        self.error_lbl.setVisible(False)

class FolderTab(QWidget):
    def __init__(self, on_unlock=None):
        super().__init__()
        self.data = load_data()
        self.on_unlock = on_unlock  # callback vers MainWindow.open_unlock_modal
        self.table = QTableWidget(len(self.data), 5)
        self.row = self.table.rowCount()
        self.col = self.table.columnCount()
        self.tab()
    
    def tab(self):
        layout = QVBoxLayout()
        self.table.setHorizontalHeaderLabels(['Folder', 'Status', 'Date Locked', 'Updated At', 'Actions'])

        for i in range(self.row):
            row_data = self.data[i]
            for j in range(len(row_data)):
                tab_data = row_data[j]
                if isinstance(tab_data, str):
                    self.table.setItem(i, j, QTableWidgetItem(tab_data))
                elif isinstance(tab_data, int) and tab_data > 0:
                    self.table.setItem(i, j, QTableWidgetItem('Locked'))

            unlock_btn = QPushButton("Unlock")
            unlock_btn.clicked.connect(lambda checked, row=i: self._on_unlock_click(row))
            self.table.setCellWidget(i, 4, unlock_btn)

        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def _on_unlock_click(self, row: int):
        if self.on_unlock:
            self.on_unlock(row)

    def add_tab_item(self, data: list):
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.table.setItem(i, j, QTableWidgetItem(str(data[i][j])))

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
        
        title_lbl = QLabel('Welcome to Vaultix...')
        title_lbl.setFont(self._font_(size=16, weight=QFont.Weight.Bold))
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        icon_lbl=QLabel()
        if os.path.exists(icon_path):
            icon_lbl.setPixmap(QIcon(icon_path).pixmap(30, 30))

        container = QHBoxLayout()
        container.addWidget(icon_lbl, alignment=Qt.AlignmentFlag.AlignTop)
        container.addWidget(title_lbl, alignment=Qt.AlignmentFlag.AlignTop)
        container.setContentsMargins(10, 10, 10, 10)

        table = FolderTab(on_unlock=self.open_unlock_modal)
        wrapper = QWidget()
        wrapper.setLayout(container)

        presentation = QVBoxLayout()
        presentation.addWidget(wrapper)
        presentation.addWidget(table)
        
        btn_icon_path = os.path.join(os.path.dirname(__file__), "assets", "add.png")
        btn_icon= QIcon(btn_icon_path) if os.path.exists(btn_icon_path) else QIcon()
        button = AddFolderBtn(btn_icon, 'Lock New Folder...')
        button.clicked.connect(self.open_lock_modal)

        maker = QLabel('v1.0.1 Made with ❤️ by Dany-py')
        maker.setFont(self._font_(size=10, weight=QFont.Weight.Normal))

        presentation.addWidget(button)
        presentation.addWidget(maker, alignment=Qt.AlignmentFlag.AlignRight)
        presentation.setContentsMargins(20, 0, 20, 20)
        presentation.setSpacing(0)

        root.setLayout(presentation)

    def open_lock_modal(self):
        dialogue = Modal('Lock new folder', 'Lock this path', self)
        
        while True:
            if dialogue.exec() != QDialog.DialogCode.Accepted:
                break

            path_input = dialogue.get_input_text(dialogue.path_input)
            pwd_input = dialogue.get_input_text(dialogue.pwd_input)
            cf_pwd_input = dialogue.get_input_text(dialogue.cf_pwd_input)

            success, message = lock_folder(
                path=path_input,
                pwd=pwd_input,
                cf_pwd=cf_pwd_input
            )

            if success:
                dialogue.clear_error()
                break
            else:
                dialogue.show_error(message)

    def open_unlock_modal(self, row: int = None):
        dialogue = Modal('Unlock folder', 'Unlock this path', self)

        while True:
            if dialogue.exec() != QDialog.DialogCode.Accepted:
                break
        
            path_input = dialogue.get_input_text(dialogue.path_input)
            pwd_input  = dialogue.get_input_text(dialogue.pwd_input)

            success, message = restore_folder(path=path_input, pwd=pwd_input)

            if success:
                dialogue.clear_error()
                break
            else:
                dialogue.show_error(message)

def gui():
    app = QApplication(sys.argv)

    icon_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    gui()