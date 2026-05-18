from PySide6.QtWidgets import (
    QApplication, QWidget, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect
from PySide6.QtGui import QPixmap, QPainter
import sys
import json
import os


# ================= BACKGROUND =================
class BackgroundFrame(QFrame):
    def __init__(self, image_path):
        super().__init__()
        self.pixmap = QPixmap(image_path)

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.pixmap.isNull():
            painter.fillRect(self.rect(), Qt.gray)
            return

        scaled = self.pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2

        painter.drawPixmap(x, y, scaled)


# ================= MAIN WINDOW =================
class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(900, 500)
        self.setWindowTitle("Reservation System")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= TOP BAR =================
        top_bar = QFrame()
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet(
            "background:#d0d0d0; border-bottom:1px solid #aaa;")

        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(15, 0, 15, 0)

        home = QLabel("HOME")
        home.setStyleSheet("color:black; font-weight:bold;")

        title = QLabel("RESERVATION SYSTEM")
        title.setStyleSheet("color:black; font-weight:bold; font-size:14px;")

        self.menu_btn = QPushButton("≡")
        self.menu_btn.setFixedSize(60, 47)
        self.menu_btn.setStyleSheet("""
            font-size: 28px;
            color: black;
            background: transparent;
            border: none;
        """)
        self.menu_btn.clicked.connect(self.toggle_menu)

        top_layout.addWidget(home)
        top_layout.addStretch()
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(self.menu_btn)

        main_layout.addWidget(top_bar)

        # ================= CENTER AREA =================
        self.center = QFrame()
        self.center.setStyleSheet("background: transparent;")
        main_layout.addWidget(self.center)

        # ================= BACKGROUND =================
        self.bg = BackgroundFrame("picbg.jpg")
        self.bg.setParent(self.center)
        self.bg.setGeometry(0, 0, 900, 400)
        self.bg.lower()

        # ================= OVERLAY =================
        self.overlay = QFrame(self.center)
        self.overlay.setGeometry(0, 0, 900, 400)
        self.overlay.setStyleSheet("background-color: rgba(0,0,0,38);")
        self.overlay.raise_()

        # ================= HERO BOX =================
        self.hero_box = QFrame(self.center)
        self.hero_box.setStyleSheet("""
            background-color: rgba(0, 0, 0, 75);
            border-radius: 18px;
        """)

        hero_layout = QVBoxLayout(self.hero_box)
        hero_layout.setContentsMargins(20, 10, 20, 10)
        hero_layout.setSpacing(0)
        hero_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        text1 = QLabel("Take a journey")
        text2 = QLabel("Into the world of an")
        text3 = QLabel("incredible destinations.")

        for t in (text1, text2, text3):
            t.setStyleSheet(
                "color: white; font-size: 32px; background: transparent;")

        text1.setStyleSheet(
            "color: white; font-size: 38px; font-weight: bold; background: transparent;")
        text2.setStyleSheet(
            "color: white; font-size: 26px; background: transparent;")
        text3.setStyleSheet(
            "color: white; font-size: 26px; background: transparent;")

        hero_layout.addWidget(text1)
        hero_layout.addWidget(text2)
        hero_layout.addWidget(text3)

        # ================= BOTTOM BAR =================
        bottom = QFrame()
        bottom.setFixedHeight(110)
        bottom.setStyleSheet("background:#d9d9d9; border-top:1px solid #aaa;")

        bottom_layout = QHBoxLayout(bottom)
        bottom_layout.setContentsMargins(20, 15, 20, 15)

        def input_box(ph):
            i = QLineEdit()
            i.setPlaceholderText(ph)
            i.setFixedHeight(40)
            i.setStyleSheet("""
                background:#bfbfbf;
                color:black;
                border-radius:10px;
                padding-left:10px;
            """)
            return i

        self.name_input = input_box("Full name")
        self.phone_input = input_box("Phone Number")
        self.email_input = input_box("Email")

        bottom_layout.addWidget(self.name_input)
        bottom_layout.addWidget(self.phone_input)
        bottom_layout.addWidget(self.email_input)

        submit = QPushButton("SIGN UP")
        submit.clicked.connect(self.save_user)
        submit.setFixedSize(120, 40)
        submit.setStyleSheet("""
            background:#41A67E;
            color:black;
            border-radius:17px;
        """)
        bottom_layout.addWidget(submit)

        main_layout.addWidget(bottom)
        print("Saving to:", os.getcwd())

        # ================= MENU =================
        self.menu = QFrame(self)
        self.menu.setFixedWidth(200)
        self.menu.setFixedHeight(self.height() - 60)
        self.menu.setStyleSheet("background:#eeeeee;")

        menu_layout = QVBoxLayout(self.menu)
        for t in ["Home", "Reservations", "Settings"]:
            btn = QPushButton(t)
            btn.setStyleSheet("color:black;")
            menu_layout.addWidget(btn)

        menu_layout.addStretch()

        self.anim = QPropertyAnimation(self.menu, b"geometry")
        self.menu_open = False
        self.menu.move(self.width(), 60)

    # ================= RESIZE =================
    def resizeEvent(self, event):
        self.bg.setGeometry(0, 0, self.center.width(), self.center.height())
        self.overlay.setGeometry(
            0, 0, self.center.width(), self.center.height())

        self.hero_box.adjustSize()
        self.hero_box.move(50, self.center.height() // 3)

        self.menu.setFixedHeight(self.height() - 60)

        if self.menu_open:
            self.menu.move(self.width() - self.menu.width(), 60)
        else:
            self.menu.move(self.width(), 60)

        super().resizeEvent(event)

    # ================= MENU =================
    def toggle_menu(self):
        open_x = self.width() - self.menu.width()
        closed_x = self.width()

        if not self.menu_open:
            self.anim.setStartValue(
                QRect(closed_x, 60, 200, self.height() - 60))
            self.anim.setEndValue(QRect(open_x, 60, 200, self.height() - 60))
        else:
            self.anim.setStartValue(QRect(open_x, 60, 200, self.height() - 60))
            self.anim.setEndValue(QRect(closed_x, 60, 200, self.height() - 60))

        self.anim.setDuration(250)
        self.anim.start()
        self.menu_open = not self.menu_open

    # ================= SAVE USER =================
    def save_user(self):

        print("Saving to:", os.getcwd())

        user_data = {
            "name": self.name_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text()
        }

        try:
            path = os.path.join(os.path.dirname(__file__), "database.json")
            print("JSON PATH:", path)
            db = json.load(file)
        except:
            db = {"users": [], "reservations": []}

        print("Before append:", db)

        db["users"].append(user_data)

        print("After append:", db)

        with open(path, "w") as file:
            json.dump(db, file, indent=4)

        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()

        print("User Saved!")


# ================= RUN =================
app = QApplication(sys.argv)
window = HomePage()
window.show()
app.exec()
