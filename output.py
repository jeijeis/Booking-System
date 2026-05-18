import sys
from PySide6.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout,
    QPushButton, QHBoxLayout, QApplication
)
from PySide6.QtCore import Qt


class SystemMessageOverlay(QWidget):
    def __init__(self, previous_window=None, message="System message"):
        super().__init__()

        self.previous_window = previous_window

        self.setWindowTitle("System Message")
        self.resize(1000, 600)

        # ================= GRAY OVERLAY =================
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(120, 120, 120, 160);
            }
        """)

        # ================= CENTER CONTAINER =================
        self.container = QFrame(self)
        self.container.setFixedSize(420, 220)

        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 230);
                border: 1px solid rgba(0, 0, 0, 20);
                border-radius: 16px;
            }
        """)

        self.container.move(
            (self.width() - self.container.width()) // 2,
            (self.height() - self.container.height()) // 2
        )

        # ================= LAYOUT =================
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(10)

        # ================= TOP BAR =================
        top_bar = QHBoxLayout()

        title = QLabel("System Message")
        title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            color: #222;
        """)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 16px;
                color: #444;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        close_btn.clicked.connect(self.go_back)

        top_bar.addWidget(title)
        top_bar.addStretch()
        top_bar.addWidget(close_btn)

        # ================= MESSAGE =================
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet("""
            font-size: 13px;
            color: rgba(0, 0, 0, 180);
        """)

        # ================= OK BUTTON =================
        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(35)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a78c2;
            }
        """)
        ok_btn.clicked.connect(self.go_back)

        # ================= BUILD =================
        layout.addLayout(top_bar)
        layout.addStretch()
        layout.addWidget(message_label)
        layout.addStretch()
        layout.addWidget(ok_btn)

    # ================= BACK NAVIGATION =================
    def go_back(self):
        if self.previous_window:
            self.previous_window.show()
        self.hide()
